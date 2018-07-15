#User Error Message
#Made by Jack Carmichael
#11/26/16
"""
=========================================================================
Object---------------------Parameters---------------Inheritance
UserErrorMessage
    -UserErrorMessage()     -window,name            -object
=========================================================================
"""

from tkinter import *
import tkinter as tk

__name__="UserErrorMessage"

class UserErrorMessage(object):
    error_shown=False
    def __init__(self, window, name):
        self.counter=0
        self.gradient_array=[]
        self.window=window
        self.setup_label(name)
        self.setup_dummy_frame()
        self.setup_gradient_array()
        self.display_error()

    def setup_label(self,name):
        self.error_message=Label(self.window,text=name,font="Times 10",fg="White",bg="Black")

    def setup_dummy_frame(self):
        dummy_frame=Frame(self.window)
        dummy_frame.pack(side=TOP)

    def setup_gradient_array(self):
        for x in range(0,99):
            if x%2==0:
                self.gradient_array.append("grey{0}".format(x))

    def display_error(self):
        if UserErrorMessage.error_shown==False:
            UserErrorMessage.error_shown=True
            self.error_message.pack(padx=0,pady=0,side=BOTTOM)
            self.show_gradient()

    def show_gradient(self):
        self.error_message.configure(foreground='white')
        self.error_message.configure(background=self.gradient_array[self.counter])
        self.counter+=1
        if self.counter<len(self.gradient_array):
            self.window.after(50, self.show_gradient)
        else:
            self.error_message.destroy()
            UserErrorMessage.error_shown=False
