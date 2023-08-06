# -*- coding: utf-8 -*-

import subprocess
from tempfile import mkdtemp
import pickle
import shutil
import shlex
import logging
import glob
import re
from os.path import exists, basename, dirname
from os import mkdir, getuid, getgid
import numpy as np

from ..config import arbc

_LOGGER = logging.getLogger(__name__)
_LOGGER.addHandler(logging.NullHandler())


# Splits have to follow the pattern `[(train_set, test_set)]`
# where each set consists of `[(folder_name, class)]`.
def generate_file_list(feature, classes, test_regex=None, train_regex=None, shuffle=True):
    feature_dir = "{0}/{1}".format(arbc.stage2(), feature)
    files = glob.glob(feature_dir + "/frames/*/")
    train_split = []
    test_split = []
    for f in files:
        sample_name = basename(dirname(f))
        cla = None
        for idx, cls in enumerate(classes):
            if sample_name.endswith(cls):
                cla = idx
                break
        if cla is not None:
            if test_regex is not None and re.match(test_regex, sample_name):
                test_split.append((sample_name, cla))
            else:
                if train_regex is None or (re.match(train_regex, sample_name)
                                           and sample_name not in [f[0] for f in test_split]):
                    train_split.append((sample_name, cla))
    try:
        temp_dir = mkdtemp(prefix='c5py_' + feature + "_")
        with open(temp_dir + '/splits.pkl', 'wb') as f:
            pickle.dump([(train_split, test_split)], f, protocol=2)
        cmd = 'python /tsn_caffe/tools/build_file_list.py /tmp/tsn/splits.pkl'
        if shuffle:
            cmd += ' --shuffle'
        _run_in_docker(cmd, feature_dir, extra_mounts={'/tmp/tsn': temp_dir})
    finally:
        shutil.rmtree(temp_dir)


def extract_features(feature, num_gpu=1, num_worker=2, sample_ext='avi'):
    feature_dir = "{0}/{1}".format(arbc.stage2(), feature)
    cmd = ('python /tsn_caffe/tools/build_of.py /generated/videos /generated/frames '
           '--num_gpu {0} --num_worker {1} --ext {2} --new_width 340 --new_height 256'.format(
        num_gpu, num_worker, sample_ext))
    _run_in_docker(cmd, feature_dir)


def train_network(feature, modality, num_class=5, engine='pytorch', num_gpu=1, batch_size=8, iter_size=None,
                  model=None, kinetics=False):
    if modality not in ['rgb', 'flow']:
        raise ValueError("Only 'rgb' or 'flow' are valid modality options.")

    if engine == 'caffe':
        cmd = 'python /tsn_caffe/tools/train_tsn.py {0} --num_gpu {1} --batch_size {2}'.format(
            modality, num_gpu, batch_size)
        if iter_size is not None:
            cmd += ' --iter_size ' + str(iter_size)
        if model is not None:
            cmd += ' --snapshot /generated/models/' + model
        if kinetics:
            cmd += ' --kinetics'
    elif engine == 'pytorch':
        cmd = 'bash /tsn_pytorch/train_{0}.sh {1} {2} {3}'.format(
            modality, num_class, num_gpu, batch_size)
        if model is not None:
            cmd += ' --resume /generated/models/' + model
    else:
        raise ValueError("Passed engine should be 'caffe' or 'pytorch'")
    feature_dir = "{0}/{1}".format(arbc.stage2(), feature)
    _run_in_docker(cmd, feature_dir)


def eval_network(feature, modality, model, num_class, num_gpu=1, num_worker=2, test_segments=6):
    if modality not in ['rgb', 'flow']:
        raise ValueError("Only 'rgb' or 'flow' are valid modality options.")
    feature_dir = "{0}/{1}".format(arbc.stage2(), feature)
    if model.endswith('.caffemodel'):
        cmd = 'python /tsn_caffe/tools/eval_net.py {0} {1} --num_gpu {2} --num_worker {3}'.format(modality, model, num_gpu,
                                                                                                  num_worker)
    elif model.endswith('.pth') or model.endswith('.pth.tar'):
        cmd = 'bash /tsn_pytorch/test_{0}.sh {1} {2} {3} {4}'.format(modality, num_class, model, num_gpu, test_segments)
    else:
        raise ValueError("Model needs to be a pth file or caffemodel")
    _run_in_docker(cmd, feature_dir)


# based on the eval_score function from the original temporal segment network implementation
# found at https://github.com/yjxiong/temporal-segment-networks
def eval_scores(score_files, score_weights, crop_agg='mean'):
    from sklearn.metrics import confusion_matrix
    npz_files = [np.load(x, encoding='latin1', allow_pickle=True) for x in score_files]
    if len(score_weights) != len(npz_files):
        raise ValueError("Score file and weight mismatch. Only {} weight specifed for a total of {} score files."
                         .format(len(score_weights), len(npz_files)))

    score_list = [f['scores'][:, 0] for f in npz_files]
    label_list = [f['labels'] for f in npz_files]
    # labels and classification results need to be sorted since caffe result order is not stable
    label_order = [np.argsort(f['labels']) for f in npz_files]

    # score_aggregation
    agg_score_list = []
    for i, score_vec in enumerate(score_list):
        agg_score_vec = [getattr(np, crop_agg)(x, axis=1).mean(axis=0) for x in score_vec]
        agg_score_list.append(np.array(agg_score_vec)[label_order[i]])

    final_scores = np.zeros_like(agg_score_list[0])
    for i, agg_score in enumerate(agg_score_list):
        final_scores += agg_score * score_weights[i]

    # results
    pred = np.argmax(final_scores, axis=1)
    cf = confusion_matrix(sorted(label_list[0]), pred).astype(float)

    cls_cnt = cf.sum(axis=1)
    cls_hit = np.diag(cf)
    cls_acc = cls_hit / cls_cnt
    acc = np.mean(cls_acc)
    return acc, cls_acc, cf


def _run_in_docker(cmd, feature_dir, run_as_root=False, extra_mounts=None, extra_args=None):
    _check_feature_dir(feature_dir)
    extra_args = [] if extra_args is None else extra_args
    extra_mounts = {} if extra_mounts is None else extra_mounts
    docker_cmd_base = ('docker run --runtime=nvidia --shm-size 6G '
                       '--mount type=bind,source={0},target=/generated '
                       '{1} {2} '
                       '-ti --rm aleneum/tsn-c5 {3}')
    extra_mounts_str = ''
    for k, v in extra_mounts.items():
        extra_mounts_str += ' --mount type=bind,source={0},target={1} '.format(v, k)
    if not run_as_root:
        extra_args.append('-u {0}:{1}'.format(getuid(), getgid()))
        if exists('/etc/passwd'):
            extra_args.append('-v /etc/group:/etc/group:ro -v /etc/passwd:/etc/passwd:ro')
    cmd = shlex.split(docker_cmd_base.format(feature_dir, extra_mounts_str, ' '.join(extra_args), cmd))
    _LOGGER.info(' '.join(cmd))
    subprocess.check_call(cmd)


def _check_feature_dir(feature_dir):
    for i in ['frames', 'videos', 'models', 'data']:
        if not exists(feature_dir + '/' + i):
            mkdir(feature_dir + '/' + i)
