# -*- encoding: utf-8 -*-
import jieba
import sys
import jieba.analyse
import re

reload(sys)
sys.setdefaultencoding('utf8')

jieba.analyse.set_stop_words('d:/spider/weibo/handle/stop_words.txt')

jieba.set_dictionary("d:/spider/weibo/handle/user_dictionary.txt")


def _dict(path):
    with open(path, 'r')as f:
        d_t = f.read()
    return dict(tuple(map(
            lambda x: (x.split(',')[1], x.split(',')[2]), filter(
                    lambda y: 1 if y else 0, d_t.split('\n')[1:]
            ))))


def _ad_pattern(d):
    # 统一编译re正则表达式
    s = set()
    for i in d.items():
        try:
            s.add(re.compile(i[0]))
        except re.error:
            pass
    return s


_ad_dict = _ad_pattern(_dict(path='d:/spider/weibo/handle/if_ad.csv'))
_sentiment_dict = _dict(path='d:/spider/weibo/handle/keyword_category.csv')


def if_ad(_text):
    """
    对传入字符串进行广告微博差别，返回1为广告，0为非广告
    :param _text:
    """
    text = str(_text)
    for each in _ad_dict:
        if re.findall(each, text):
            return 1
    return 0


def checking_sentiment(_text):
    """
    对传入字符串进行情感词提取，及情感极性判别
    返回tuple类型，分别为
    （正面词汇，下面词汇数量，负面词汇，负面词汇数量，情感极性差别）
    :param _text:
    """

    def good_or_bad(lg, lb, score_ok):
        gi = len(lg)
        bi = len(lb)
        if gi == 0 and bi == 0:
            return 0
        elif gi == 0 and bi != 0:
            return -1
        elif gi != 0 and bi == 0:
            return 1
        elif abs(gi - bi) <= score_ok:
            return 0
        elif gi > bi - score_ok:
            return 1
        else:
            return -1

    g = list()  # 正面
    b = list()  # 负面
    fenchi = jieba.lcut(_text)

    for c in fenchi:
        chi = c.encode('utf8')
        if _sentiment_dict.get(chi) == '1':
            g.append(chi)
        elif _sentiment_dict.get(chi) == '-1':
            b.append(chi)
    return ' '.join(g), len(g), ' '.join(b), len(b), good_or_bad(g, b, 1)


if __name__ == "__main__":
    t = u"该简历人员，公司背景很好，但是从经历看，更多的是运维和研发，不太适合产品经理的角色，更适合明松或研发的职位"
    print checking_sentiment(t)
