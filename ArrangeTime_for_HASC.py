#!/usr/bin/env python
# coding: utf-8

"""
__doc__
HASC Corpusの加速度,角速度ファイルの時間とデータ数を揃えるプログラム
"""
import csv
import glob
import os
import shutil
import sys
import numpy as np

print(__doc__)
__author__ = "Haruyuki Ichino"
__version__ = "0.1"
__date__ = "2016/06/26"

# データ格納ディレクトリ
inputDir = './data/'
# 結果の出力ディレクトリ
outputDir = './output/'

# ==========================================================
# 関数
# ==========================================================

def createDir(dir_path):
    """
    概要: 指定のディレクトリがなければ作成する関数
    """
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

def removeZeroLine(data):
    while data[0, 1] == 0:  # 一番上のx軸の値
        data = np.delete(data, 0, axis=0)

    return data

def removeHeaderLine_until_startTime(data, startTime):
    while (startTime-data[0, 0]) > 0.05 and data[0, 0] < startTime:  # 一番上のx軸の値
        data = np.delete(data, 0, axis=0)

    return data

# ==========================================================
# 準備
# ==========================================================

# 入力HASCデータの調査
# dataディレクトリの存在確認
if not os.path.isdir(inputDir):
    print("dataディレクトリが存在してないで")
    sys.exit(1)

# 出力ディレクトリの作成
createDir(outputDir)


# ==========================================================
# データの読み込み & 処理
# ==========================================================

# 行動ディレクトリでの処理
activities = os.listdir(inputDir)
for activity in activities:
    # .DS_Storeのチェック
    if activity == ".DS_Store":
        continue

    activityDir = inputDir + activity + '/'

    # ディレクトリじゃない場合はスキップ
    if not os.path.isdir(activityDir):
        continue

    # 出力ディレクトリに行動ディレクトリを作成
    output_action_dir = outputDir + activity + '/'
    createDir(output_action_dir)

    # 被験者別の処理
    persons = os.listdir(activityDir)
    for person in persons:
        # .DS_Storeのチェック
        if person == ".DS_Store":
            continue

        personDir = activityDir + person + '/'

        # ディレクトリじゃない場合はスキップ
        if not os.path.isdir(personDir):
            continue

        # 出力ディレクトリにpersonディレクトリを作成
        output_person_dir = output_action_dir + person + '/'
        createDir(output_person_dir)

        print("============================================")
        print(person)
        print("============================================")

        # 各ファイルリストの作成
        accFiles = glob.glob(personDir + '*acc*')
        gyroFiles = glob.glob(personDir + '*gyro*')
        magFiles = glob.glob(personDir + '*mag*')
        metaFiles = glob.glob(personDir + '*meta*')
        labelFiles = glob.glob(personDir + '*label*')

        # metaファイルとlabelファイルのコピー
        for metaFile in metaFiles:
            shutil.copy(metaFile, output_person_dir)
        for labelFile in labelFiles:
            shutil.copy(labelFile, output_person_dir)

        # 各加速度ファイルにアクセス
        for accFile_temp in accFiles:
            # print(accFile)
            hascID = accFile_temp.split("/")[4].split("-")[0]
            print(hascID)

            # 各HASC-IDのファイルにアクセス
            accFile = personDir + hascID + "-acc.csv"
            gyroFile = personDir + hascID + "-gyro.csv"
            # print(accFile)
            # print(gyroFile)

            # csvファイルからデータの読み込み
            accData = np.loadtxt(accFile, delimiter=",")
            gyroData = np.loadtxt(gyroFile, delimiter=",")
            print("acc:(行,列) =" + str(accData.shape) + ", ", end="")
            print("gyro(行,列) =", gyroData.shape)
            accLines_org = accData.shape[0]
            gyroLines_org = gyroData.shape[0]

            # 最初の0が続く部分を削除
            accData = removeZeroLine(accData)
            gyroData = removeZeroLine(gyroData)
            # print("(行,列) =", accData.shape)
            # print("(行,列) =", gyroData.shape)

            # 最も遅いスタート時間の取得
            startTime = max(accData[0, 0], gyroData[0, 0])
            # print(startTime)

            # スタート時間を揃える
            accData = removeHeaderLine_until_startTime(accData, startTime)
            gyroData = removeHeaderLine_until_startTime(gyroData, startTime)
            # print("(行,列) =", accData.shape)
            # print("(行,列) =", gyroData.shape)

            minLines = min(accData.shape[0], gyroData.shape[0])
            # print(minLines)

            # 長さを揃える
            accData = accData[:minLines, :]
            gyroData = gyroData[:minLines, :]
            # print("データ調節後:(行,列) =", accData.shape)
            # print("(行,列) =", gyroData.shape)

            # 削除したデータ量の計算
            accLines_after = accData.shape[0]
            gyroFiles_after = gyroData.shape[0]
            deleteLines_acc = accLines_org - accLines_after
            deleteLines_gyro = gyroLines_org - gyroFiles_after

            print("accの削除行数: %d (%.2f％), " % (deleteLines_acc, deleteLines_acc/accLines_org*100), end="")
            print("gyroの削除行数: %d (%.2f％)" % (deleteLines_gyro, deleteLines_gyro/gyroLines_org*100))
            print()

            # 調節後のファイルの出力
            np.savetxt(output_person_dir+hascID+"-acc.csv", accData, delimiter=",")
            np.savetxt(output_person_dir+hascID+"-gyro.csv", gyroData, delimiter=",")

            # 各同HASC-IDファイルの処理の終了

        # 各person処理の終了
    # 各行動への処理の終了


