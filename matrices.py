from typing import List, Tuple

import pandas as pd

from weapon import Weapon


def appl(r):
    pass

    return r >= 12, \
           r >= 13, \
           r >= 14, \
           r >= 15, \
           r >= 16, \
           r >= 17, \
           r >= 18, \
           r >= 19, \
           r >= 20, \
           r >= 21, \
           r >= 22


def appl2(r):
    return r['damage'] if r['attack'] >= 12 else pd.NA, \
        r['damage'] if r['attack'] >= 13 else pd.NA, \
        r['damage'] if r['attack'] >= 14 else pd.NA, \
        r['damage'] if r['attack'] >= 15 else pd.NA, \
        r['damage'] if r['attack'] >= 16 else pd.NA, \
        r['damage'] if r['attack'] >= 17 else pd.NA, \
        r['damage'] if r['attack'] >= 18 else pd.NA, \
        r['damage'] if r['attack'] >= 19 else pd.NA, \
        r['damage'] if r['attack'] >= 20 else pd.NA, \
        r['damage'] if r['attack'] >= 21 else pd.NA, \
        r['damage'] if r['attack'] >= 22 else pd.NA


def compute_matrices(result: pd.DataFrame) -> (pd.DataFrame, pd.DataFrame):
    attack_matrix = pd.DataFrame()
    damage_matrix = pd.DataFrame()
    attack_matrix['12'], attack_matrix['13'], attack_matrix['14'], attack_matrix['15'], \
        attack_matrix['16'], attack_matrix['17'], attack_matrix['18'], attack_matrix['19'], \
        attack_matrix['20'], attack_matrix['21'], attack_matrix['22'] \
        = zip(*result['attack'].apply(appl))

    damage_matrix['12'], damage_matrix['13'], damage_matrix['14'], damage_matrix['15'], \
        damage_matrix['16'], damage_matrix['17'], damage_matrix['18'], damage_matrix['19'], \
        damage_matrix['20'], damage_matrix['21'], damage_matrix['22'] \
        = zip(*result.apply(appl2, axis=1))

    # for ac in acs:
    #     attack_matrix[str(ac)] = result['attack'] >= ac
    #     damage_matrix[str(ac)] = result.apply(lambda x: x['damage'] if x['attack'] >= ac else pd.NA, axis=1)
    return attack_matrix.T, damage_matrix.T


def summarize_attack_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df['hit %'] = matrix.sum(axis=1) / len(matrix.columns)
    return df


def summarize_damage_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    df = pd.DataFrame()
    df['avg dmg'] = matrix.mean(axis=1)
    # df['min'] = matrix.min(axis=1)
    # df['max'] = matrix.max(axis=1)

    return df


def show_matrices(result: pd.DataFrame):
    attack_matrix, damage_matrix = compute_matrices(result)
    pd.options.display.float_format = '{:.2f}'.format
    summary = summarize_attack_matrix(attack_matrix).join(summarize_damage_matrix(damage_matrix))
    summary.index.name = 'AC'
    output = summary.reset_index().to_string(index=False, formatters={
        'hit %': '{:.1%}'.format,
        'avg dmg': '{:.1f}'.format,
    })

    print(output)
