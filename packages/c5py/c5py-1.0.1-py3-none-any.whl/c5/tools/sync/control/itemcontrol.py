import os.path

from ..model import itemmodel as im
from ..gui import main_view, cvtools
from .videotools import prepare_videos, get_syncs
from ..tools import layoutcontainer, moviecontainer
from ..tools.audiocontainer import AudioContainer, extract_audio_sample
import threading
import time
import logging
import json

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# Python3 does not contain cmp
try:
    cmp(1, 2)
except NameError:
    def cmp(a, b):
        return (a > b) - (a < b)


class DispatcherThread(threading.Thread):

    MERGE = 0
    SYNC = 1
    CREATE = 2

    def __init__(self, controller):
        threading.Thread.__init__(self)
        self.tasks = []
        self.is_running = True
        self.controller = controller
        self._is_busy = False

    def stop(self):
        self.is_running = False

    def add_task(self, task_nr):
        self.tasks.append(task_nr)

    def run(self):
        while self.is_running:
            if len(self.tasks) > 0:
                self._is_busy = True
                task = self.tasks.pop(0)
                if task == DispatcherThread.MERGE:
                    logger.info("Process task 'Merge'")
                    self.controller._merge_files()
                elif task == DispatcherThread.SYNC:
                    logger.info("Process task 'Sync'")
                    self.controller._detect_syncs()
                elif task == DispatcherThread.CREATE:
                    logger.info("Process task 'Create'")
                    self.controller._create_movies()
                self._is_busy = False
                logger.info("Finished task")
            else:
                time.sleep(1)

    def is_busy(self):
        return self._is_busy


class ItemController:
    def __init__(self, model):
        self.model = model
        self.gui = main_view.MainWindow(self.model)
        self.gui.set_listener(self)
        self.dispatcher = DispatcherThread(self)
        self.dispatcher.start()

    def restart_gui(self):
        self.gui = main_view.MainWindow(self.model)
        self.gui.set_listener(self)
        if self.dispatcher.is_busy():
            self.gui.set_busy()

    def gui_shutdown(self):
        self.gui = None

    def add_file(self, container, file_path):
        container.add_file(file_path)

    def remove_file(self, container, a_file):
        container.remove_file(a_file)

    def create_set(self, set_name, layout_name):
        new_set = im.SetItem(set_name)
        new_set.set_layout(self.model.get_layout(layout_name))
        self.model.add_set(new_set)
        new_set.update_status()

    def set_layout(self, set_name, layout_name):
        self.model.get_set(set_name).set_layout(self.model.get_layout(layout_name))

    def merge_files(self):
        logger.debug("Schedule task 'Merge'")
        self.dispatcher.add_task(DispatcherThread.MERGE)
        if self.gui is not None:
            self.gui.set_busy()

    def _merge_files(self):
        for set_name in self.model.get_set_names():
            a_set = self.model.get_set(set_name)
            for container_name in a_set.get_layout().get_container_names():
                container = a_set.get_container(container_name)
                if container.get_status() == 0:
                    file_list = []
                    destination = os.path.join(self.model.get_path(), str(a_set.get_name() + "_" + container.get_name() + ".mp4").replace(" ", "_"))
                    for idx in range(container.get_file_count()):
                        file_list.append(container.get_file(idx).get_path())
                    container.set_status(1)
                    result = prepare_videos(file_list, destination)
                    if result is True:
                        container.set_status(2)
                    else:
                        container.set_status(0)
                elif container.get_status() < 0:
                    logger.warn("WARNING %s of %s IS NOT VALID! "
                                "Most likely a file is missing." % (container_name, set_name))

    def sync_video(self, container):
        logger.debug("Syncing container...")
        video = os.path.join(self.model.get_path(),
                             str(container.parent().get_name() + "_" + container.get_name() + ".mp4").replace(" ", "_"))
        container.path = video
        container.set_status(3)

        if len(container.get_used_events()) != 2:
            logger.debug("No events available. Starting detection step.")
            events = get_syncs(video)
            for key, value in events.items():
                container.add_sync_event(key, value)
            use = sorted(events, cmp=lambda x, y: cmp(events[x], events[y]), reverse=True)[:2]
            container.set_used_events(sorted(use))
        logger.debug("Creating thumbnails...")
        video_widget = cvtools.CVVideo()
        video_widget.set_capture(video)
        video_widget.save_images(container.get_sync_events().keys(), self.model.get_path())
        container.set_status(4)

    def sync_audio(self, audio, initial_guess=None, force_exact_time=False):
        if audio.container is None:
            print("create container")
            container = AudioContainer(audio.get_path())
            AudioContainer.prepare()
            container.init(cut_factor=2)
            if audio.get_status() < 4:
                container.detect_signal()
                audio.set_events(container.get_sync_times())
            audio.container = container
        if force_exact_time is True and initial_guess is not None:
            audio.set_sync(initial_guess)
            audio.container.set_used_sync(initial_guess)
        elif initial_guess is None:
            try:
                evts = audio.get_events()
                idx = (evts.index(audio.get_sync()) + 1) % len(evts)
            except ValueError:
                idx = 0
            audio.set_sync(audio.get_events()[idx])
            audio.container.set_used_sync(audio.get_events()[idx])
            self.gui.ui.audioSyncLabel.setText(str(audio.get_sync()))
        else:
            times = audio.get_events()
            diff = map(lambda x: abs(initial_guess - x), times)
            idxmin = diff.index(sorted(diff)[0])
            audio.set_sync(times[idxmin])
            audio.container.set_used_sync(audio.get_events()[0])
        audio.set_status(4)
        extract_audio_sample(audio.get_path(), audio.get_sync(), 10, audio.get_path() + ".sync.wav")

    def detect_syncs(self):
        logger.debug("Schedule task 'Sync'")
        self.dispatcher.add_task(DispatcherThread.SYNC)
        if self.gui is not None:
            self.gui.set_busy()

    def _detect_syncs(self):
        for set_name in self.model.get_set_names():
            a_set = self.model.get_set(set_name)
            for container_name in a_set.get_layout().get_container_names():
                container = a_set.get_container(container_name)
                if container.get_status() in [2, 3]:
                    self.sync_video(container)
                elif container.get_status() < 2:
                    logger.warn("WARNING %s of %s IS NOT PREPARED!" % (container_name, set_name))

            for audio in a_set.get_audios():
                self.sync_audio(audio)

    def is_busy(self):
        return self.dispatcher.is_busy()

    def create_movies(self):
        logger.debug("Schedule task 'Create'")
        self.dispatcher.add_task(DispatcherThread.CREATE)
        if self.gui is not None:
            self.gui.set_busy()

    def _create_movies(self):
        for set_name in self.model.get_set_names():
            a_set = self.model.get_set(set_name)
            slayout =  a_set.get_layout()
            path = str(self.model.get_path() + "/" + set_name+".mp4").replace(" ", "_")
            vid = layoutcontainer.LayoutContainer(str(path), slayout.get_width(), slayout.get_height(),
                                                  delete_temp=True)

            for container_name in a_set.get_layout().get_container_names():
                container = a_set.get_container(container_name)
                clayout = slayout.get_container(container_name)
                path = str(self.model.get_path() + "/" + set_name+"_"+container_name + ".mp4").replace(" ","_")
                part = moviecontainer.MovieContainer(str(path))
                part.setImageFormat("png")
                part.setSize(clayout.get_width(), clayout.get_height())
                part.setCrop(0, 0, 0, 0)
                part.set_sync_frames(container.get_used_events())
                vid.addMovie(part, clayout.get_pos_x(), clayout.get_pos_y())
                if container_name == slayout.get_ref_name():
                    print("Reference is " + container_name)
                    vid.setReference(part)
                if clayout.use_audio() is True:
                    part.useAudio()

            for audio in a_set.get_audios():
                if audio.container is None:
                    audio.container = AudioContainer(audio.get_path())
                    AudioContainer.prepare()
                    audio.container.set_used_sync(audio.get_sync())
                vid.addAudio(audio.container)

            vid.generate(jobs=4)
            vid.clear()
            with open("{0}/{1}.json".format(self.model.get_path(), set_name.replace(" ", "_")), 'w') as f:
                json.dump(a_set.get_meta_data(), f, sort_keys=True, indent=4, separators=(',', ': '))
            del vid
