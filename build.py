'''
生成 c42 码表
'''

import shutil
import json
from os.path import exists
from os import makedirs

def strB2Q(ustring):
    '''
    将半角转换为全角
    '''
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 32:
            inside_code = 12288
        elif 32 <= inside_code <= 126:
            inside_code += 65248
        rstring += chr(inside_code)
    return rstring

with open('config/c_42.dict.meta.yaml') as c42MetaFile:
    c42Meta = c42MetaFile.read()
with open('config/c_42a.dict.meta.yaml') as c42aMetaFile:
    c42aMeta = c42aMetaFile.read()

with open('assets/brevity.dat') as brevityFile:
    brevity = [line.strip('\r\n').split('\t') for line in brevityFile]

componentKey = {}
componentName = {}
with open('assets/keymap.dat') as keymapFile:
    for line in keymapFile:
        component, key, name = line.strip('\r\n').split('\t')
        componentKey[component] = key
        componentName[component] = name if name else component
with open('assets/specialty.dat') as specialtyFile:
    specialty = [line.strip().split() for line in specialtyFile]

div = []
fullCode = []
charSet = {}
qd = {}
with open('assets/decomposition.dat') as decompositionFile:
    for line in decompositionFile:
        char, s1, s2, s3, py, isPartial = line.strip('\r\n').split('\t')
        if isPartial == '0':
            PY = strB2Q(py.upper())
            diva = (componentName[s1] + componentName[s2] + componentName[s3] + PY)[:3]
            quanma = (componentKey[s1] + componentKey[s2] + componentKey[s3] + py)[:3]
            div.append((char, diva))
            fullCode.append((char, quanma))
            qd[char] = quanma
        charSet[char] = []

if not exists('build'): makedirs('build')
if not exists('build/opencc'): makedirs('build/opencc')

with open('build/c_42.dict.yaml', 'w') as c42Dict:
    c42Dict.write(c42Meta)
    for char, code in brevity:
        c42Dict.write('%s\t%s\n' % (char, code))
        c42Dict.write('　\t%s\n' % code)

with open('build/c_42a.dict.yaml', 'w') as c42aDict:
    key = 'abcdefghijklmnopqrstuvwxyz;'
    all3 = [x + y + z for x in key for y in key for z in key]
    c42aDict.write(c42aMeta)
    c3 = []
    hasBrevityCharList = [char for char, code in brevity]
    hasSpecialtyCharList = [char for char, code in specialty]
    for char, code in fullCode:
        c3.append(code)
        if char in hasBrevityCharList or char in hasSpecialtyCharList:
            c42aDict.write('%s\t~%s\n' % (char, code))
        else:
            c42aDict.write('%s\t%s\n' % (char, code))
    for code in [x for x in all3 if x not in c3]:
        c42aDict.write('　\t~%s\n' % code)
    for char, code in specialty:
        c42aDict.write('%s\t%s\n' % (char, code))

with open('build/opencc/brevity.txt', 'w') as filterBrevity:
    brevityCharOnly = [(x[0], x[1]) for x in brevity if len(x[0]) == 1 and x[0] != '　']
    for char, code in brevityCharOnly:
        if code != qd[char][:2]:
            if code[-1] in ',./':
                filterBrevity.write('%s\t~%s\n' % (char, code))
            else:
                filterBrevity.write('%s\t~~%s\n' % (char, code))
        else:
            filterBrevity.write('%s\t%s\n' % (char, code))

with open('build/opencc/brevity2.txt', 'w') as filterBrevityWord:
    brevityWordOnly = [(x[0], x[1]) for x in brevity if len(x[0]) == 2]
    for char, code in brevityWordOnly:
        filterBrevityWord.write('%s\t%s\n' % (char, code))

with open('build/opencc/division.txt', 'w') as filterDivision:
    for char, code in div:
        filterDivision.write('%s\t%s\n' % (char, code))

with open('assets/wordFrequencies.dat') as f:
    wordFreqList = [line.strip().split() for line in f]

for word, freq in wordFreqList:
    char = word[0]
    if len(charSet.get(char, [])) < 5:
        charSet[char].append(word)

with open('build/opencc/phrase.txt', 'w') as filterPhrase:
    for char, phraseList in charSet.items():
        if phraseList:
            filterPhrase.write('%s\t%s %s\n' % (char, char, ' '.join(phraseList)))

for name in ('c_42.schema', 'c_42a.schema', 'symbols_for_c'):
    shutil.copyfile('config/%s.yaml' % name, 'build/%s.yaml' % name)
for name in ('brevity', 'brevity2', 'division', 'emoji'):
    shutil.copyfile('config/%s.json' % name, 'build/opencc/%s.json' % name)
for name in ('emoji_category', 'emoji_word'):
    shutil.copyfile('config/%s.txt' % name, 'build/opencc/%s.txt' % name)
