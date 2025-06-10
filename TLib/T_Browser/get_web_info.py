from tkinter import *
from tkinter.ttk import *
from win32con import CF_UNICODETEXT
from WebBrowserInfo import *
from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardData, CloseClipboard

window = Tk()
window.title("Edge浏览器信息查看")
window.geometry("800x300")
tab = Notebook(window)
hf = Frame(window)
tableColumns = ("序号", "网址", "标题", "访问次数", "最后访问时间")
tableSize = (40, 375, 150, 60, 150)
tableAnchor = (CENTER, W, CENTER, CENTER, CENTER)
tableValues = [list(i.values()) for i in
               History(edge_path).get_history()]
s1 = Scrollbar(hf, orient=VERTICAL)
tv = Treeview(hf, columns=tableColumns, height=15, show='headings', selectmode="browse", yscrollcommand=s1.set)
for i, s, a in zip(tableColumns, tableSize, tableAnchor):
    tv.heading(column=i, text=i, anchor=a)
    tv.column(i, minwidth=40, width=s, anchor=a)
for data in tableValues:
    tv.insert('', 'end', value=data)
s1.pack(side=RIGHT, fill=BOTH)
s1.config(command=tv.yview)


def copy(event):
    if str(event.widget) == ".!frame.!treeview":
        table = event.widget
        for item in table.selection():
            table.selection_remove(item)

        row = table.identify_row(event.y)
        col = int(str(table.identify_column(event.x)).replace('#', ''))
        text = table.item(row, 'value')[col - 1]
        print("已复制")
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(CF_UNICODETEXT, text)
        CloseClipboard()


tv.bind("<Double-1>", copy)
tv.pack(side=TOP, fill=BOTH)

bf = Frame(window)
tableValues = BookMark(edge_path).get_bookmarks()
s11 = Scrollbar(bf, orient=VERTICAL)
s21 = Scrollbar(bf, orient=HORIZONTAL)
tv1 = Treeview(bf, columns=("网址",), height=15, show='tree headings', selectmode="browse", yscrollcommand=s11.set,
               xscrollcommand=s21.set)
tv1.heading(column="#0", text="名称", anchor=W)
tv1.column("#0", minwidth=40, width=350, anchor=W)
tv1.heading(column="#1", text="网址", anchor=W)
tv1.column("#1", minwidth=40, width=425, anchor=W)
tree = {"": ""}


def add(s=tableValues, p=""):
    for k, i in s.items():
        if type(i) == str:
            tv1.insert(tree[p], END, text=k, values=(i,))
        else:
            tree[k] = tv1.insert(tree[p], END, text=k)
            add(i, k)


add()

s11.pack(side=RIGHT, fill=BOTH)
s11.config(command=tv1.yview)
s21.pack(side=BOTTOM, fill=BOTH)
s21.config(command=tv1.xview)


def copy(event):
    if str(event.widget) == ".!frame2.!treeview":
        table = event.widget
        for item in table.selection():
            table.selection_remove(item)

        row = table.identify_row(event.y)
        col = int(str(table.identify_column(event.x)).replace('#', ''))
        text = table.item(row, 'value')[col - 1]
        print("已复制")
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(CF_UNICODETEXT, text)
        CloseClipboard()


tv1.bind("<Double-1>", copy)
tv1.pack(side=TOP, fill=BOTH)

pf = Frame(window)
tableColumns = ("源站点", "作用站点", "用户名", "密码", "创建时间", "最后使用时间")
tableSize = (150, 150, 150, 150, 150, 150)
tableAnchor = (W, W, CENTER, CENTER, CENTER, CENTER)
tableValues = [list(i.values()) for i in
               Password(edge_path, edge_pwd_path).get_passwords()]
s12 = Scrollbar(pf, orient=VERTICAL)
s22 = Scrollbar(pf, orient=HORIZONTAL)
tv2 = Treeview(pf, columns=tableColumns, height=15, show='headings', selectmode="browse", yscrollcommand=s12.set,
               xscrollcommand=s22.set)
for i, s, a in zip(tableColumns, tableSize, tableAnchor):
    tv2.heading(column=i, text=i, anchor=a)
    tv2.column(i, minwidth=40, width=s, anchor=a)
for data in tableValues:
    tv2.insert('', 'end', value=data)
s12.pack(side=RIGHT, fill=BOTH)
s12.config(command=tv2.yview)
s22.pack(side=BOTTOM, fill=BOTH)
s22.config(command=tv2.xview)


def copy(event):
    if str(event.widget) == ".!frame3.!treeview":
        table = event.widget
        for item in table.selection():
            table.selection_remove(item)

        row = table.identify_row(event.y)
        col = int(str(table.identify_column(event.x)).replace('#', ''))
        text = table.item(row, 'value')[col - 1]
        print("已复制")
        OpenClipboard()
        EmptyClipboard()
        SetClipboardData(CF_UNICODETEXT, text)
        CloseClipboard()


tv2.bind("<Double-1>", copy)
tv2.pack(side=TOP, fill=BOTH)

tab.add(hf, text='历史记录')
tab.add(bf, text='收藏夹')
tab.add(pf, text='密码')
tab.pack(side=TOP, fill=BOTH)
window.mainloop()
