#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on:2016/1/28 14:07
# Project:my_ocr
# Author:yangmingsong

import urllib2
import cStringIO
import base64
from PIL import Image
import numpy
import cv2
import pytesseract


# using this function(pic2stc) to extract text from picture,x should be given as picture url
# for test,(base64 code, encoded by picture)
# x=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAAUCAIAAABwJOjsAAACcklEQVRIie2UMWjiUB
#   zGX9QOikMHNxcpgnONWLU6WKWgYhXsWNw6KC5KoYNLHbplEaSgqIsQiq4uFQotgjqIWlwUaaCICmqEJlDQqO+G3N
#   lcmxy3XL2h35T/996XX16+EARCCLYh0Vao3+DtgDEMs9vtBwcHZ2dnT09PG7/ZbGIYxjAMN9bv9y8vL4+OjkwmUy
#   AQGA6HrN/tdoPBoMViMZvNoVDo5eVFkAx/6f7+nqZpiqKurq7sdjtrHh8fOxwOFEXf3t4gR7lcrlAoUBRFkmQoFP
#   L7/RBCmqatVms8HqdpejabRaNRj8cDBQQ+W7VaTa/XMwwDIez1eq1W6zN4tVptriuVCoqiDMN0Oh0URUmS3Ph6vZ
#   67k6uPHY9Go9vbW5/PJ5FIAABqtZq/IdF7kCTJ3d1diUSyt7enVCpvbm6Wy+Xr62s2m3U6ndyd/B1Xq1WdTud2ux
#   EECYfDgt38ruVyieO41+sFAOzs7KTTaYIgHA6Hy+XSaDTRaFQo+A42Go31ej2fz4/H41gs9pfg6+trkUh0fn7Oju
#   Vy+fn5+fT09PDwsFgsNhoNweTnt//w8MDthrdjVhiGeTyeyWTCjhRFGY3Gu7u7zerJyYnQx8VTAIIgYrFYqJuNEo
#   lEtVpNp9MKhYJ1+v3+YrHQarXsaDabB4PBer3mjf+8O0EQpVJpPp+PRqNMJmOz2f5MTSaTj4+PqVRqQwUAqFQquV
#   yeyWRomp5OpziO7+/vCx0AgRACAIbD4cXFBUEQMpnMZrNFIhGpVAoA0Ol0HwL1ep3XL5fLUqm03W5jGNbtdmUymc
#   FgiEQi3CfjAX+9/oN/9Tf4H+sHXsTdPl96bGoAAAAASUVORK5CYII=

def pic2str(x, lang=None):
    if 'http' == x[:4]:
        res = urllib2.urlopen(x)
        t = cStringIO.StringIO(res.read())
        res.close()
    elif 'base64' in x:
        res = x.split('base64,')[1]
        t = cStringIO.StringIO(base64.decodestring(res))
    else:
        return None
    image = Image.open(t)
    t = numpy.asarray(image)
    # 转换灰度图
    gray = cv2.cvtColor(t, cv2.COLOR_BGR2GRAY)
    # 二值化
    temp = int(t.max() / 2)
    thd, image_b = cv2.threshold(gray, temp, 255, cv2.THRESH_BINARY)
    c, r = image_b.shape
    image_b = cv2.resize(image_b, (r * 2, c * 2))
    flag, image_a = cv2.imencode('.jpeg', image_b)
    if flag:
        image_ok = Image.open(cStringIO.StringIO(image_a.tostring()))
        if not lang:
            return pytesseract.image_to_string(image_ok)
        else:
            return pytesseract.image_to_string(image_ok, lang=lang)
    else:
        return None
