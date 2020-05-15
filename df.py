import os
import sys

from os.path import join, getsize

if len(sys.argv) == 2:
    targetPath = sys.argv[1]
else:
    targetPath = os.getcwd()

errorPaths = []  # 错误文件路径


def getdirsize(dir):
    size = 0

    for root, dirs, files in os.walk(dir):
        try:
            size += sum([getsize(join(root, name)) for name in files])
        except OSError as ex:
            errorPaths.append(ex)
    return size


def humanSize(size):
    if size > 1024 * 1024 * 1024:
        return str(round(size / (1024 * 1024 * 1024), 2)) + "GB"
    elif size > 1024 * 1024:
        return str(round(size / (1024 * 1024), 2)) + "MB"
    elif size > 1024:
        return str(round(size / 1024, 2)) + "KB"
    else:
        return str(size) + "B"


try:
    with os.scandir(targetPath) as entries:
        print("已用\t\t类型\t\t文件路径")
        print("-" * 90)
        totalSize = 0
        for entry in entries:
            size = 0
            if entry.is_file():
                size = getsize(entry.path)
            else:
                size = getdirsize(entry.path)
            totalSize += size
            sizeHuman = humanSize(size)
            totalHumanSize = humanSize(totalSize)
            print(sizeHuman, end="")
            if len(sizeHuman) < 3:
                print("", end="\t\t")
            elif len(sizeHuman) < 8:
                print("", end="\t\t")
            else:
                print("", end="\t")

            if entry.is_file():
                print("文件", end="\t\t")
            else:
                print("目录", end="\t\t")
            print(entry.path)
        print("-" * 90)
        print("总计：%s" % totalHumanSize)
        print("-" * 90)
        if len(errorPaths) > 0:
            print("错误文件列表：")
            for i in errorPaths:
                print(i)
except FileNotFoundError:
    print("系统找不到指定的路径：%s" % targetPath)
