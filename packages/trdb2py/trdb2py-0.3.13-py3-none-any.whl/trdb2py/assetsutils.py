# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2
import numpy as np
from trdb2py.trdb2 import getAssetCandles3
from trdb2py.candlesutils import calcCandlesSimilarity


def calcAssetsSimilarity(cfg: dict, asset0: str, asset1: str, tsStart: int, tsEnd: int):
    candles0 = getAssetCandles3(cfg, asset0, tsStart, tsEnd)
    candles1 = getAssetCandles3(cfg, asset1, tsStart, tsEnd)

    return calcCandlesSimilarity(candles0, candles1)


def calcAssetsSimilarity2(cfg: dict, names: list, assets: list, tsStart: int, tsEnd: int):
    arr = []
    for asset0 in assets:
        list = []
        for asset1 in assets:
            if asset0 == asset1:
                list.append(1.0)
            else:
                cs = calcAssetsSimilarity(cfg, asset0, asset1, tsStart, tsEnd)
                list.append(cs)

        arr.append(list)

    return arr
