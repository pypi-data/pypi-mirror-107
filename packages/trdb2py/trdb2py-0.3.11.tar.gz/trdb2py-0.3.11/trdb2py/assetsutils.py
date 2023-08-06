# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2
import numpy as np
from trdb2py.trdb2 import getAssetCandles3
from trdb2py.candlesutils import calcCandlesSimilarity


def calcAssetsSimilarity(cfg: dict, asset0: str, asset1: str, tsStart: int, tsEnd: int):
    candles0 = getAssetCandles3(cfg, asset0, tsStart, tsEnd)
    candles1 = getAssetCandles3(cfg, asset1, tsStart, tsEnd)

    return calcCandlesSimilarity(candles0, candles1)
