# -*- encoding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def count_freq(path):
    word_freq = {}
    with open(path,'r')as f:
        fp=f.read()
    tot_cnt = 0.0
    for line in fp.split('\n'):
        line = line.split('\t')
        if len(line) < 2:
            continue
        st = line[0].decode('utf-8')
        freq = float(line[1])
        for w in st:
            if w not in word_freq:
                word_freq[w] = 0.0
            word_freq[w] += freq
            tot_cnt += freq
    res=list()
    while True:
        try:
            x, y = word_freq.popitem()
            if x:
                freq = y * 1.0 / tot_cnt
                t="%s\t%f" % (x, freq)
                res.append(t)
                print t
            else:
                break
        except:
            break

    def write_txt(t):
        with open('D:/spider/weibo/handle/result_2.txt', 'w')as f:
            f.write(t)

    write_txt('\n'.join(res))

if __name__ == "__main__":
    count_freq('D:/spider/weibo/handle/result_1.txt')
