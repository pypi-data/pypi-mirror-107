import sys

from PyQt5 import QtWidgets
from os.path import exists
import os

from .control import itemcontrol
from .control.xmlwrapper import XMLWrapper
from .model import itemmodel
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# rename 'raw_input' in Python2
try:
    input = raw_input
except NameError:
    pass


def start_app():
    level = logging.DEBUG if any(d in os.environ for d in ['Debug', 'DEBUG', 'debug']) else logging.INFO
    logging.basicConfig(level=level)

    if len(sys.argv) != 2:
        print("""Exactly ONE argument is required.
Usage: c5sync path/to/config.xml
config.xml will be created in case it does not exist.
""")
        sys.exit(1)
    if not exists(sys.argv[1]):
        print("{0} does not exist. Will be initialized from default config.".format(sys.argv[1]))
        import pkg_resources
        from shutil import copy
        data_path = pkg_resources.resource_filename("c5", "tools/sync/data")
        copy("{0}/c5.xml".format(data_path), sys.argv[1])

    a_model = itemmodel.ModelItem()
    wrapper = XMLWrapper(a_model)
    wrapper.load_model(sys.argv[1])

    logger.info("Initialize QtWidget.")
    app = QtWidgets.QApplication(sys.argv)
    controller = itemcontrol.ItemController(a_model)
    controller.detect_syncs()
    # controller._create_movies()
    do_run = True
    try:
        while do_run is True:
            controller.gui.show()
            app.exec_()
            del controller.gui
            inp = input("console mode. q <enter> to quit. everything else restarts gui: ")
            if inp == "q":
                do_run = False
            else:
                controller.restart_gui()
    except Exception as e:
        print("Caught Error:", e)
    finally:
        wrapper.save_model(sys.argv[1])
        print("kill controller")
        controller.dispatcher.stop()


if __name__ == '__main__':
    start_app()
