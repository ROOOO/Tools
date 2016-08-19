# coding: utf-8

__author__ = 'King'

import os
import re

class Atlases:
    def __init__(self, path):
        self.projPath = path or os.path.join(os.getcwd())
        self.files = []
        self.paths = []

    def run(self):
        for dirPath, dirNames, fileNames in os.walk(self.projPath):
            for fileName in fileNames:
                if os.path.splitext(fileName)[1] == '.prefab':
                    # print os.path.join(str(dirPath), str(fileName))
                    # print dirPath
                    self.paths.append(os.path.join(str(dirPath), str(fileName)))

    def search(self, name):
        for prefab in self.paths:
            file = open(prefab, 'r+')
            text = file.read()
            items = re.findall(re.compile(r'\.name.*?value:\s(.*?)\n', re.S), text)
            for item in items:
                # print item
                if item == name:
                    print prefab

import sys
if __name__ == '__main__':
    t = Atlases(sys.argv[1])
    t.run()
    if len(sys.argv) == 3:
        t.search(str(sys.argv[2]))

