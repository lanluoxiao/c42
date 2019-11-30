# 词频，一词一行
f = open('wordFreq.txt', encoding='utf-8', mode='r')
wordFreqList = [line.strip('\r\n').split('\t') for line in f]
f.close()
wordFreqList = sorted(wordFreqList, key=lambda x: float(x[1]), reverse=True)
# 字集，一字一行
f = open('charSet.txt', encoding='utf-8', mode='r')
charDict = {line.strip('\r\n'): [] for line in f}
f.close()
# 添加联想词
for word, freq in wordFreqList:
    char = word[0]
    if len(charDict.get(char, [])) < 5:
        charDict[char].append(word)
# 生成 Rime 格式的联想词
f = open('associative.txt', encoding='utf-8', mode='w')
for char, phraseList in charDict.items():
    if phraseList:
        f.write(char + '\t' + char + ' ')
        f.write(' '.join(phraseList) + '\n')
f.close()