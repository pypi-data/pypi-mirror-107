from os.path import exists
import pandas as pd
from .config import arbc

# Questionnaire Notes
# A,C,D,F,G identical
# B (AR Experience) B1.4, 1.5 missing in F2Fl; F2F.B1.4 -> AR.B1.6
# E (HMD comfort) E1.2 - 1.6 missing in F2F; E1.20 - 1.23 exclusive ARAss
# F2F.E1.2 = AR.E1.7 -> field numeration past E1.2 differs!

CODE = {'Age': 'A1.2', 'Gender': 'A1.1', 'AR-Experience': 'B1.4',
        'Occupation': 'A1.10',
        'Seating/Comfort': 'E1.1', 'HMD/Impair': 'E1.2', 'HMD/Notice5Min': 'E1.3',
        'HMD/Notice10Min': 'E1.4', 'HMD/Notice15Min': 'E1.5', 'HMD/Comfort': 'E1.6',
        'Sound/Use': 'E1.22', 'Sound/Rate': 'E1.23',
        'Radar/Use': 'E1.20', 'Radar/Rate': 'E1.21', 'Fun': 'G1.1',
        'Role': 'D1.1', 'Role/Identify': 'D1.2', 'Role/Balance': 'D1.3',
        'Role/Defence': 'D1.4', 'Role/Arguments':'D1.5', 'Negotiation/Difference': 'D1.7',
        'Task/Understanding': 'F1.1', 'Task/Difficulty': 'F1.2', 'Task/Duration': 'F1.8'}


# Remapping for F2F
code_diff = {'B1.4': 'B1.6', 'B1.5': 'B1.7'}
for i in range(2, 15):
    code_diff['E1.{0}'.format(i)] = 'E1.{0}'.format(i+5)

LIKERT_GOOD = ['very good', 'good', 'rather good', 'rather bad', 'bad', 'very bad']
LIKERT_AMOUNT = ['very often', 'often', 'frequently', 'occasionally', 'hardly', 'never']
LIKERT_DOMINANT = ['very dominant', 'dominant', 'rather dominant', 'rather inferior', 'inferior', 'very inferior']
LIKERT_FUN = ['much fun', 'fun', 'some fun', 'no fun']
LIKERT_DURATION = ['much longer', 'longer', 'a bit longer', 'a bit shorter', 'shorter', 'much shorter']
LIKERT_BEHAVIOUR = ['very similar', 'similar', 'rather similar', 'rather different', 'different', 'very different']
LIKERT_COMFORT = ['very pleasant', 'pleasant', 'rather pleasant', 'rather unpleasant', 'unpleasant', 'very unpleasant']
LIKERT_IMPAIR = ['none', 'occasional', 'slight', 'middling', 'strong', 'very strong']
LIKERT_NOTICE = ['not noticed', 'hardly', 'occasionally', 'constantly', 'strongly']

FEEDBACK_PATH = "{0}/feedback.csv".format(arbc.stage2())


def load_feedback():

    if not exists(FEEDBACK_PATH):
        feedback = _load_questionnaire()
        feedback.to_csv(FEEDBACK_PATH)
    else:
        feedback = pd.read_csv(FEEDBACK_PATH, index_col=0)
    return feedback


def _load_questionnaire():

    df = pd.DataFrame()

    for i in range(1, 5):
        tmp = pd.read_csv('{0}/feedback/study{1}.csv'.format(arbc.extra(), i),
                          index_col=0, skip_blank_lines=True)
        # remap F2F fields
        if i == 2:
            tmp.rename(index=code_diff, inplace=True)
            tmp = tmp[~tmp.index.duplicated(keep='first')]

        tmp = tmp[pd.notnull(tmp.index)]
        df = pd.concat([df, tmp], axis=1)

    # Drop triade data from pre-study
    df = df.drop([u'301.T.A', u'301.T.B', u'301.T.C', u'302.T.A',
                  u'302.T.B', u'302.T.C'], axis=1)
    df = df[pd.notnull(df.index)]  # filter empty lines
    return df
