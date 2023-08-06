"""  Fast access to conversion and processing capabilities of c5py. """


import argparse
import logging
import os

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def start_app(args=None):
    """ Application runner function. Will be initiated by ``c5helper``.

    Parameters
    ----------
    args : list, optional
        A dictionary containing service configuration parameters (method, method arguments). If not
        passed, the command line arguments `sys.argv` will be used.

    Examples
    --------
    This method is the start up hook for the application `c5helper` which is installed as part of the c5py package.\
    The following command fill convert the recorded Kinect data into comma separated values (CSV):

    >>> # convert data of trial 101 into CSV
    >>> c5helper convert artkp 101
    >>> # convert data of all trials into CSV
    >>> c5helper convert artkp all

    For `c5helper` to work, the corpus environment has to be set up. This involves the availability of (raw) ARbC data
    and the correct settings of the environment variables ``C5_RAW_PATH`` (path to raw data),\
    ``C5_STAGE1_PATH`` (path to preprocessed corpus data) and ``C5_STAGE2_PATH`` (output path).
    """

    logging.basicConfig()
    level = logging.DEBUG if any(d in os.environ for d in ['Debug', 'DEBUG', 'debug']) else logging.INFO
    logger.setLevel(level)

    parser = argparse.ArgumentParser(description='c5py command line tool')
    subparsers = parser.add_subparsers(title='action',
                                       description='valid action',
                                       help='add action --help to get further info', dest='action')
    convert_parser = subparsers.add_parser('convert')
    convert_parser.add_argument('data', help='data set to be converted',
                                choices=['artkp', 'brix', 'kinect'])
    convert_parser.add_argument('trial', help='trial to be converted. "all" converts all trials')

    args = parser.parse_args(args)

    if args.data == 'artkp':
        from ..raw.artkp import start_app
        start_app(['convert', args.trial])
