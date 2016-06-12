# coding:utf8

from Tkinter import *
import ttk
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
            # print e.message
            res.append("FUNCTION EXCEPTION !")
            return None
    for i in dict_file.items():
        if help_if_string_or_dict(i[1]):
            category_last(i[1])
        elif type(i[1]) == list:
            if type(i[1][0])==dict:
                category_last(i[1][0])
            else:
                if not i[0] in res:
                    res.append(i[0])
                continue
        else:
            if not i[0] in res:
                res.append(i[0])


def func_main(t):
    category_last(t)
    return ' \n'.join(res)


def GUI_main():
    def calculate():
        try:
            value = func_main(input_string.get())
            return_value.set(value)
        except ValueError:
            pass

    def reset():
        return_value.set('')
        input_string.set('')
        global res
        res = list()

    root = Tk()
    root.title("Extract final category from JSON file ; Author MingSong ; Version 1.0.0")

    mainframe = ttk.Frame(root)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    input_string = StringVar()
    return_value = StringVar()

    feet_entry = ttk.Entry(mainframe, width=50, textvariable=input_string)
    feet_entry.grid(column=1, row=2)

    ttk.Entry(mainframe, textvariable=return_value, width=50).grid(column=2, row=2)
    ttk.Label(mainframe, text='Input:').grid(column=1, row=1, sticky=(W,))
    ttk.Label(mainframe, text='Output:').grid(column=2, row=1, sticky=(W,))
    ttk.Button(mainframe, text="Extract", command=calculate).grid(column=1, row=3)
    ttk.Button(mainframe, text="Reset", command=reset).grid(column=2, row=3)

    for child in mainframe.winfo_children():
        child.grid_configure(padx=1, pady=1)

    feet_entry.focus()
    root.bind('<Return>', calculate)

    root.mainloop()


if __name__ == "__main__":
    GUI_main()

# for test
# {"1": 2, "b": "c", "d": {"2": 1, "Y": 3}}
