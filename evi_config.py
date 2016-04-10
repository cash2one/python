import os

# install setuptools
os.system("cd C:\python_dev\setuptools-20.6.7\setuptools-20.6.7")
os.system("python setup.py install")
# install pip
os.system("cd C:\python_dev\pip-8.1.1\pip-8.1.1")
os.system("python setup.py install")
# add path to system evi_path
os.system("set path=C:\Python27\Scripts;%path%")
#install module
os.system("pip install pymysql")
os.system("pip install pyquery")
os.system("pip install paramiko")
os.system("pip install requests")