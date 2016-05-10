# coding:utf8
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')

res = list()


def category_last(put_in_string):
    help_if_string_or_dict = lambda d: True if type(d) == dict else False

    if help_if_string_or_dict(put_in_string):
        dict_file = put_in_string
    else:
        try:
            dict_file = json.loads(put_in_string)
        except Exception, e:
            print e.message
            return None
    for i in dict_file.items():

        if help_if_string_or_dict(i[1]):
            category_last(i[1])
        elif type(i[1]) == list and i[1]:
            category_last(i[1][0])
        else:
            if not i[0] in res:
                res.append(i[0])


def main(t):
    # t=
    category_last(t)
    # for item in res:
    #     print item
    return ' '.join(res)
