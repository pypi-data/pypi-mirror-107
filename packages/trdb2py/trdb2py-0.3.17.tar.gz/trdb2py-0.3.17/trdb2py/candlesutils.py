# -*- coding:utf-8 -*-
import trdb2py.trading2_pb2
import numpy as np


def calcCandlesSimilarity(candles0: trdb2py.trading2_pb2.Candles, candles1: trdb2py.trading2_pb2.Candles):
    if len(candles0.candles) != len(candles1.candles):
        raise ValueError

    arr0 = []
    arr1 = []

    for candle in candles0.candles:
        arr0.append(candle.close - candle.open)

    for candle in candles1.candles:
        arr1.append(candle.close - candle.open)

    arr = []
    for i in range(len(arr0)):
        arr.append(arr1[i] / arr0[i])

    return np.mean(arr)


def calcCandlesSimilarity_LowLevel(candles0: trdb2py.trading2_pb2.Candles, candles1: trdb2py.trading2_pb2.Candles):
    if len(candles0.candles) != len(candles1.candles):
        raise ValueError

    arr0 = []
    arr1 = []

    for candle in candles0.candles:
        if candle.close > candle.open:
            arr0.append(1.0)
        elif candle.close < candle.open:
            arr0.append(-1.0)
        else:
            arr0.append(0.0)

    for candle in candles1.candles:
        if candle.close > candle.open:
            arr1.append(1.0)
        elif candle.close < candle.open:
            arr1.append(-1.0)
        else:
            arr1.append(0.0)

    nums = 0
    for i in range(len(arr0)):
        if (arr0[i] > 0 and arr1[i] >= 0) or (arr0[i] < 0 and arr1[i] <= 0) or (arr1[i] > 0 and arr0[i] >= 0) or (arr1[i] < 0 and arr0[i] <= 0):
            nums = nums + 1

    return nums / len(arr0)
