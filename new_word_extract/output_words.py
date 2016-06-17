# -*- encoding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def load_dict(filename):
    dict = {}
    fp = open(filename)
    for line in fp:
        line = line.strip('\n')
        item = line.split('\t')
        if len(item) == 2:
            dict[item[0]] = float(item[1])
    return dict


def compute_prob(str, dict):
    p = 1.0
    for w in str:
        w = w.encode('utf-8')
        if w in dict:
            p *= dict[w]
    return p


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


def find_compact_substr(dict):
    fp = open("D:/spider/weibo/handle/result_1.txt")
    str_freq = {}
    for line in fp:
        line = line.decode('utf-8')
        items = line.split('\t')
        if len(items) < 4:
            continue
        substr = items[0]
        freq = float(items[1])
        left_ent = float(items[2])
        right_ent = float(items[3])
        p = compute_prob(substr, dict)
        freq_ratio = freq / p
        if freq_ratio > 5.0 \
                and left_ent > 2 \
                and right_ent > 2 \
                and len(substr) >= 2 \
                and not is_ascii(substr):
            print "%s\t%f" % (substr, freq)


if __name__ == "__main__":
    dict = load_dict('D:/spider/weibo/handle/result_2.txt')
    find_compact_substr(dict)
