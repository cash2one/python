# -*- encoding: utf-8 -*-
import re

re_sub_p=re.compile(u'回复|#.+?#|@.+[\s:]|\[.+?\]|@.+$|//|\s+?')

t=u"这个有点6//@橘子好吃不分酸甜://@美图秀秀:一直以为外国人不P图是崇尚自然美，原来是没有美图手机[哈哈]"

print re.sub(re_sub_p,'',t)