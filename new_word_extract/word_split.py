# -*- encoding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')
import re
import math

re_sub_p = re.compile(u'[，,。；？（）、～~！!&;)(^　\s+]|[a-zA-Z0-9]')


def compute_entropy(word_list):
    wdict = {}
    tot_cnt = 0
    for w in word_list:
        if w not in wdict:
            wdict[w] = 0
        wdict[w] += 1
        tot_cnt += 1
    ent = 0.0
    for k, v in wdict.items():
        p = 1.0 * v / tot_cnt
        ent -= p * math.log(p)
    return ent


def count_substr_freq():
    # fp = open("./video.corpus")
    with open('d:/spider/weibo/handle/jd_comment.txt', 'r')as f:
        fp = f.read()
    str_freq = {}
    str_left_word = {}
    str_right_word = {}
    tot_cnt = 0
    for line in fp.split('\n'):
        # line = line.strip('\n')
        st = re.sub(re_sub_p, '', line.decode('utf8'))
        l = len(st)
        for i in range(l):
            for t in range(1, 10, 1):
                w = st[i:i + t + 1]
                if not i == 0:
                    left_word = st[i - 1]
                else:
                    left_word = '^'
                if not i == l - 1:
                    try:
                        right_word = st[i + t + 1]
                    except:
                        right_word = '%'
                else:
                    right_word = '%'
                str_freq[w] = 1 if not str_freq.get(w) else str_freq.get(w) + 1
                if not w in str_left_word:
                    str_left_word[w] = [left_word]
                str_left_word[w].append(left_word)
                if not w in str_right_word:
                    str_right_word[w] = [left_word]
                str_right_word[w].append(right_word)
            tot_cnt += 1

    def write_txt(t):
        with open('D:/spider/weibo/handle/result_1.txt', 'w')as f:
            f.write(t)

    res = list()
    for k, v in str_freq.items():
        if v >= 1:
            left_ent = compute_entropy(str_left_word[k])
            right_ent = compute_entropy(str_right_word[k])
            if right_ent > 1 and left_ent > 1 and v > 50:
                t="%s\t%f\t%f\t%f\t%d" % (k, v * 1.0 / tot_cnt, left_ent, right_ent, v)
                res.append(t)
                try:
                    print t
                except:
                    pass

    write_txt('\n'.join(res))


if __name__ == "__main__":
    count_substr_freq()
