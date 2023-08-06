import unicodedata
import re
from functools import partial
import xml.etree.ElementTree as Tree
import numpy as np
from os.path import dirname, join

from c5.config import arbc, ConfigLoader, FILE_NAMES
from os.path import exists
from c5.data import sequences_to_frames

CA_FULL_DT = np.dtype({'names': ['timestamp', 'start', 'duration', 'tier', 'content'],
                       'formats': [np.uint64, np.uint, np.uint, np.object, np.object]})

# compatibility (Python 2/3) wrapper for unicode function
try:
    type(unicode)

    def _to_ascii(data):
        return unicodedata.normalize('NFKD', unicode(data)).encode('ascii', 'ignore')
except NameError:
    def _to_ascii(data):
        return unicodedata.normalize('NFKD', data).encode('ascii', 'ignore').decode('ascii')


def _import_eaf(eaf_file):
    tree = Tree.parse(eaf_file)
    root = tree.getroot()
    times_xml = root.find('TIME_ORDER')
    times = {}

    media = [join(dirname(eaf_file), f.attrib.get('RELATIVE_MEDIA_URL', f.attrib['MEDIA_URL']))
             for f in root.find('HEADER').findall('MEDIA_DESCRIPTOR')]
    offset = max([int(f.attrib.get('TIME_ORIGIN', 0))
                  for f in root.find('HEADER').findall('MEDIA_DESCRIPTOR')])

    for child in times_xml.iter('TIME_SLOT'):
        times[child.attrib['TIME_SLOT_ID']] = int(child.attrib['TIME_VALUE'])

    data = []

    for tier_xml in root.findall('TIER'):
        tier_id = tier_xml.attrib['TIER_ID']
        for anno in tier_xml.iter('ANNOTATION'):
            meta = anno[0]
            time_start = times[meta.attrib['TIME_SLOT_REF1']]
            time_end = times[meta.attrib['TIME_SLOT_REF2']]
            duration = time_end - time_start
            text = meta[0].text if meta[0].text else ""
            data.append([tier_id, '', time_start, time_end, duration, text])
    return data, media, offset


def _convert_elan(elan_data, start_time, offset):
    new_data = []
    for x in elan_data:
        event = (int(x[2]) + start_time + offset, int(x[2]) + offset, int(x[4]), x[0], x[5])
        new_data.append(event)
    new_data = np.array(new_data, CA_FULL_DT)

    # sorting the data by timestamps (not sure if wanted)
    new_data = np.sort(new_data, axis=0)
    return new_data


class ElanReader(object):
    def __init__(self, file_path, trial_id=None):
        if exists(file_path) is False:
            if trial_id is None:
                raise IOError("File %s does not exist and trial_id has not been "
                              "passed to retrieve path." % file_path)
            if file_path not in FILE_NAMES:
                raise AttributeError("Cannot find annotation data with tag %s" % file_path)
            file_path = arbc.stage1.trial(trial_id).file(file_path)()
            start_time = ConfigLoader(trial_id).get('trial.start')
        else:
            start_time = 0
        data, self.media, offset = _import_eaf(file_path)
        self.data = _convert_elan(data, start_time, offset)
        self._init_tiers()

    def _init_tiers(self):
        tiers = np.unique(self.data['tier'])
        for tier in tiers:
            func = _to_ascii(tier)
            func = re.sub(r'\s+', '_', str(func)).replace('-', '_')
            setattr(self, func, partial(self._query, tier))

    def _query(self, tier):
        return self.data[self.data['tier'] == tier]

    @staticmethod
    def to_pandas(data, closed='right'):
        return sequences_to_frames(data, closed=closed)
