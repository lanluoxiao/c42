'''
更新联想词
'''

from os.path import expanduser
import sys
import fileinput

path = expanduser('~/Library/Rime/opencc/phrase.txt')
argList = sys.argv[1].split()
newPhrase = argList[0]
targetChar = newPhrase[0]
if len(argList) == 1:
    position = 1
else:
    position = int(argList[1]) - 1

found = False

for line in fileinput.input(path, inplace=True):
    char, phrases = line.strip().split('\t')
    if char == targetChar:
        phraseList: list = phrases.split()
        if newPhrase in phraseList:
            n = phraseList.index(newPhrase)
            phraseList[n] = phraseList[position]
            phraseList[position] = newPhrase
        else:
            phraseList.insert(position, newPhrase)
            phraseList = phraseList[:6]
        print(f'{char}\t{" ".join(phraseList)}')
        found = True
    else:
        print(line, end='')

if not found:
    with open(path, 'a') as f:
        f.write(f'{targetChar}\t{targetChar} {newPhrase}\n')
