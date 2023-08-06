import sys
import argparse
from pkg_resources import resource_filename, Requirement
from os.path import exists
import webbrowser
import logging
import pandas as pd
import numpy as np

from .twistedviewer import serve_app
from ..config import arbc, MARKER_IDS
from ..data import stage2_cached

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def _show_viewer(browser, call):
    browser.open_new(call)


def start_app(args=None):
    """
    Initializes the C5 data viewer.
    IMPORTANT: The data viewer expects the ARbC corpus to be present and configured.

    Parameters
    ----------
    args : dict, optional
        A dictionary containing service configuration parameters (file, port, local). If not
        passed, the command line arguments `sys.argv` will be used.

    Examples
    --------
    This method is the start up hook for the application `c5viewer` which is installed as part of
    the c5py package.

    >>> c5viewer --tid 106 --port 9000

    Alternatively, it can be called programmatically with

    >>> from c5.tools.dataviewer import start_app
    >>> star_app({'tid': 106, 'port':9000})
    """

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('matplotlib').setLevel(level=logging.WARNING)
    if args is None:
        parser = argparse.ArgumentParser()
        parser.add_argument('-i', '--tid', type=int, help='trial id')
        parser.add_argument('-p', '--port', type=int, help='webserver port')
        parser.add_argument('-s1', '--stage1', help='data root for ARbC stage 1')
        parser.add_argument('-s2', '--stage2', help='data root for ARbC stage 2')
        args = parser.parse_args(sys.argv[1:])

    if not args.tid:
        print("no trial id passed")
        parser.print_help()
        return

    args.port = args.port if args.port is not None else 8080
    if not args.stage1:
        args.stage1 = arbc.stage1()
    if not args.stage2:
        args.stage2 = arbc.stage2()

    if not exists(args.stage1):
        print("Corpus stage 1 path {0} does not exist".format(args.stage1))
        return

    args.serve_path = resource_filename("c5", "/viewer")
    url_params = "?tid={0}".format(args.tid)

    speech_path = arbc.stage2.speech_activity_trial(format_string=False).format(tid=args.tid)
    vis_path = arbc.stage2.object_visibility_trial(format_string=False).format(tid=args.tid)
    kinect_nego_video_path = arbc.stage2.kinect_nego_video(format_string=False).format(tid=args.tid)

    if not exists(speech_path):
        from ..derived.speech import generate_speech_activity, erode_speech_activity
        print("Did not find speech data. Will generate them now. Please be patient...")
        db = stage2_cached(arbc.stage2.speech_activity)(generate_speech_activity)(compression=False)
        e = stage2_cached(arbc.stage2.speech_activity_eroded)(erode_speech_activity)(db=db, thresh=1000)[args.tid]
        e[['speech1', 'speech2']] = e[['speech1', 'speech2']] * 1
        e.to_csv(speech_path, columns=['speech1', 'speech2', 'timestamp'])
    if not exists(vis_path):
        from ..sensors import collect_marker_data
        from ..derived.visibility import generate_visual_attention
        print("Did not find visibility data. Will generate them now. Please be patient...")
        movement = stage2_cached(arbc.stage2.marker_data)(collect_marker_data)()[args.tid]
        visibility = stage2_cached(arbc.stage2.object_visibility)(generate_visual_attention)()[args.tid]
        x = pd.DataFrame(visibility.timestamp)
        # print "\n".join(movement.columns.tolist())
        for mid in MARKER_IDS:
            l = visibility['visible_m{0}_hmd1'.format(mid)] * 2
            r = visibility['visible_m{0}_hmd2'.format(mid)] * 2
            r[r > 0] += 1
            sx = movement['s_x_m{0}_cam3'.format(mid)]
            sy = movement['s_y_m{0}_cam3'.format(mid)]
            dx = movement['delta_m{0}_cam3'.format(mid)]
            remove = dx > 1000
            sx.loc[remove] = np.nan
            sy.loc[remove] = np.nan
            x = x.assign(**{'s_x_m{0}'.format(mid): sx,
                            's_y_m{0}'.format(mid): sy,
                            'visible_m{0}'.format(mid): l + r})
        x.to_csv(vis_path)
    if not exists(kinect_nego_video_path):
        print("Did not find Kinect data. Will generate them now. Please be patient...")
        from ..sensors import KinectLoader
        kl = KinectLoader(args.tid)
        kl.to_video(kinect_nego_video_path)

    server = serve_app(args)
    call = "http://localhost:" + str(args.port) + "/" + url_params
    try:
        browser = webbrowser.get()
        server.callInThread(_show_viewer, browser, call)
    except webbrowser.Error as e:
        print(e)
        print("Open your browser and go to: {0}".format(call))

    server.run()


if __name__ == '__main__':
    start_app()
