from os.path import exists
from c5.config import arbc, FILE_NAMES, get_config
from c5.data import frames_to_sequences
import numpy as np
import pandas as pd

from .reader import CA_FULL_DT

# compatibility (Python 2/3) wrapper for unicode function
try:
    type(unicode)
except NameError:
    unicode = str


class ElanWriter(object):
    def __init__(self, file_path, trial_id=None):
        from bs4 import BeautifulSoup
        if exists(file_path) is False:
            if trial_id is None:
                raise IOError("File %s does not exist and trial_id has not been"
                              "passed to retrieve path." % file_path)
            if file_path not in FILE_NAMES:
                raise AttributeError("Cannot find annotation data with tag %s" % file_path)
            file_path = arbc.stage1.trial(trial_id).file(file_path)()
        self.soup = BeautifulSoup(open(file_path), "xml")
        self.root = self.soup.ANNOTATION_DOCUMENT
        self.timestamps = self.root.TIME_ORDER
        self.offset = max([int(f.get('TIME_ORIGIN', 0))
                           for f in self.root.HEADER.findAll('MEDIA_DESCRIPTOR')])

    def add_tier(self, data, tier_id, type_ref="default-lt"):
        data = data.copy()
        data['start'] -= self.offset  # consider media offset
        if self.soup.find('TIER', {'TIER_ID': tier_id}) is not None:
            raise ValueError("A tier with ID %s already exists" % tier_id)

        if self.soup.find('LINGUISTIC_TYPE', {'LINGUISTIC_TYPE_ID': type_ref}) is None:
            new_type_ref = self.soup.new_tag('LINGUISTIC_TYPE', GRAPHIC_REFERENCES="false",
                                             LINGUISTIC_TYPE_ID=type_ref, TIME_ALIGNABLE="true")
            self.root.append(new_type_ref)

        new_tier = self.soup.new_tag("TIER", ANNOTATOR="c5py Generator", DEFAULT_LOCALE="de",
                                     LINGUISTIC_TYPE_REF=type_ref, TIER_ID=tier_id)
        time_ids = [int(tag['TIME_SLOT_ID'][2:]) for tag in self.soup.find_all('TIME_SLOT')]
        last_time_id = sorted(time_ids)[-1]
        anno_ids = [int(tag['ANNOTATION_ID'][1:])
                    for tag in self.soup.find_all('ALIGNABLE_ANNOTATION')]
        last_anno_id = sorted(anno_ids)[-1]

        for _, row in data.iterrows():
            last_anno_id += 1
            for time in [row.start, row.start + row.duration]:
                last_time_id += 1
                new_time_slot = self.soup.new_tag('TIME_SLOT', TIME_SLOT_ID='ts%d' % last_time_id,
                                                  TIME_VALUE=str(time))
                self.timestamps.append(new_time_slot)
            new_annoation = self.soup.new_tag('ALIGNABLE_ANNOTATION',
                                              ANNOTATION_ID="a%d" % last_anno_id,
                                              TIME_SLOT_REF1="ts%d" % (last_time_id - 1),
                                              TIME_SLOT_REF2="ts%d" % last_time_id)
            new_content = self.soup.new_tag('ANNOTATION_VALUE')
            new_content.append(str(row.content))
            new_annoation.append(new_content)
            new_tier.append(new_annoation)
        self.root.HEADER.find('PROPERTY',
                              {'NAME': "lastUsedAnnotationId"}).string = unicode(last_anno_id)
        self.root.append(new_tier)

    def remove_tier(self, tier_id):
        tier = self.soup.find('TIER', {'TIER_ID': tier_id})
        if tier is None:
            raise ValueError("There is no tier with ID %s!" % tier_id)
        return tier.extract()

    def save(self, file_name):
        with open(file_name, "wb") as eaf_file:
            eaf_file.write(self.soup.prettify("utf-8"))

    @staticmethod
    def to_elan(data, column, filename=None):
        if isinstance(data, np.ndarray):
            data = pd.DataFrame.from_records(data)
        config, trial_id = get_config(data.timestamp[0])
        ts = data.timestamp.copy()
        value = data[column].copy()
        seqs = frames_to_sequences(value, ts, value.dtype)
        res = np.empty(seqs.shape[0], dtype=CA_FULL_DT)
        res['timestamp'] = seqs['start']
        res['start'] = seqs['start']
        if config is not None:
            res['start'] -= config.get('trial.start')
        # to be consistent with data loaded from elan files
        res['tier'] = column
        res['duration'] = seqs['duration']
        res['content'] = seqs[column]
        res = pd.DataFrame(res)
        res.set_index('timestamp', inplace=True, verify_integrity=True)
        if filename is not None:
            res.to_csv(filename)
        return res
