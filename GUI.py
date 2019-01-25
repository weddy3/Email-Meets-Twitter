# -*- coding: utf-8 -*-
"""
Created on Wed Jan 16 17:03:18 2019

@author: eddyw
"""

from tkinter import*

root = Tk()

root.title("Email Meets Python")

fromAddress = Label(root, text = "From:")
toAddress = Label(root, text = "To:")
CCAddress = Label(root, text = "CC:")
subject=Label(root,text= "Subject:")
body= Label(root, text = "Body:")

fromAddressEntry = Entry(root)
toAddressEntry = Entry(root)
CCAddressEntry = Entry(root)
subjectLabelEntry = Entry(root)
bodyLabelEntry=Entry(root)

fromAddress.grid(row = 1)
toAddress.grid(row = 2)
CCAddress.grid(row=3)
subject.grid(row=4)
body.grid(row=5)

fromAddressEntry.grid(row = 1, column = 1)
toAddressEntry.grid(row = 2, column = 1)
CCAddressEntry.grid(row=3,column=1)
subjectLabelEntry.grid(row=4,column=1)
bodyLabelEntry.grid(row=5,column=1)

sendButton = Button(root, text = "Send E-mail", fg = "blue")
sendButton.grid(row=6,columnspan=2)

root.mainloop()

