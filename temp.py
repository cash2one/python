# coding:utf8
from tkinter import *
from tkinter import ttk
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


def func_main(t):
    category_last(t)
    return ' \n'.join(res)


def GUI_main():
    def calculate(*args):
        try:
            value = func_main(input_string.get())
            return_value.set(value)
        except ValueError:
            pass


    root = Tk()
    root.title("Extract title from JSON file")

    mainframe = ttk.Frame(root, padding="60 8 60 8")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    input_string = StringVar()
    return_value = StringVar()

    feet_entry = ttk.Entry(mainframe, width=40, textvariable=input_string)
    feet_entry.grid(column=1, row=1, sticky=(N, S))

    ttk.Entry(mainframe, textvariable=return_value, width=40).grid(column=2, row=1, sticky=(N, S))
    ttk.Button(mainframe, text="Extract", command=calculate).grid(column=1, row=2, sticky=W)

    for child in mainframe.winfo_children(): child.grid_configure(padx=2, pady=2)

    feet_entry.focus()
    root.bind('<Return>', calculate)

    root.mainloop()

if __name__=="__main__":
    GUI_main()