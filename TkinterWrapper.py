#Tkinter Wrapper
#Made by Jack Carmichael
#10/6/16
"""
===================================================================================
Object--------------------Parameters--------------Inheritance
Tkinter Wrapper
    -Window()             -name                   -object
    -DialogBox()          -parent_window,name     -Window
    -WindowMenu()         -window                 -object
    -WindowMenuCascade()  -window                 -object
    -GroupWidgetActions() -none                   -object
    -WindowFrame()        -window                 -GroupWidgetActions
    -WindowButton()       -window,name,action     -GroupWidgetActions
    -WindowLabel()        -window,name            -GroupWidgetActions
    -WindowEntry()        -window                 -GroupWidgetActions
    -WindowListbox()      -window                 -GroupWidgetActions
    -WindowScrollbar()    -window,x_or_y          -GroupWidgetActions
    -WindowCanvas()       -window,width,height    -GroupWidgetActions
===================================================================================
NOTES:
    -MUST DO: Move canvas to its own mudule, and import it here. Its to powerfull
    -Might redesign it so the class inherit from the tkinter widget they represent
"""

from tkinter import *
import tkinter as tk

def print_all():
    class_list=[Window,DialogBox,WindowMenu,WindowMenuCascade,WindowFrame,WindowButton,
                WindowLabel,WindowEntry,WindowListbox,WindowScrollbar,WindowCanvas]
    print("TkinterWrapper classes and coresponding functions:")
    print("NOTE - this list only includes classes avialble for use")
    for _class in class_list:
        print("{0}".format(str(_class)))
        for item in _class.available_methods:
            print("\t{0}".format(item))


class Window(object):
    available_methods=["-> __init__(window name)","-> resize(x,y)","-> bind_action(key, action)",
                       "-> start_mainloop()","-> remove_min_max_buttons(True/False)",
                       "-> resizable(width, height)","-> destroy_window()","-> get_window()"]
    def __init__(self, name):
        self.window=Tk()
        self.window.title(name)

    def resize(self, x, y):
        size_string="{0}x{1}".format(x, y)
        self.window.geometry(size_string)

    def bind_action(self, key, action):
        self.window.bind(key, action)

    def start_mainloop(self):
        self.window.mainloop()

    def remove_min_max_buttons(self, min_max):
        if min_max==True:
            self.window.attributes("-toolwindow", 1)
        else:
            self.window.attributes("-toolwindow", 0)

    def resizable(self, width, height):
        self.window.resizable(width=width, height=height)
            
    def destroy_window(self):
        #self.window.quit()
        self.window.destroy()

    def get_window(self):
        return self.window


class DialogBox(Window):
    available_methods=["-> __init__(parent_window,window_name)","-> All others are same as Window class"]
    def __init__(self,parent_window,name):
        self.window=Toplevel(parent_window)
        self.window.title(name)

    def destroy_window(self,_quit):
        if _quit==True:
            self.window.quit()
        self.window.destroy()


class WindowMenu(object):
    available_methods=["-> __init__(window)","-> add_cascade_to_menu(cascade_name,cascade)",
                       "-> delete_cascade(index_of_cascade)"]
    def __init__(self, window):
        self.menu_bar=Menu(window)
        window.config(menu=self.menu_bar)

    def add_cascade_to_menu(self, name, cascade):
        self.menu_bar.add_cascade(label=name, menu=cascade)

    def delete_cascade(self, index):
        self.menu_bar.delete(index)


class WindowMenuCascade(object):
    available_methods=["-> __init(window,tearoff)","-> add_item_to_cascade(name,action)",
                       "-> add_separator()","-> get_cascade()"]
    def __init__(self, window, tearoff):
        self.window=window
        self.menu_bar=Menu(self.window)
        self.cascade=Menu(self.window, tearoff=tearoff)

    def add_item_to_cascade(self, name, action):
        self.cascade.add_command(label=name, command=action)

    def add_separator(self):
        self.cascade.add_separator()

    def get_cascade(self):
        return self.cascade
        
        
class GroupWidgetActions(object):
    def __init__(self):
        pass

    def destroy_widget(self, widget):
        widget.destroy()

    def attach_scrollbar(self,widget,x_or_y,scrollbar):
        if x_or_y.upper()=="X":
            widget.configure(xscrollcommand=scrollbar.set)
        elif x_or_y.upper()=="Y":
            widget.configure(yscrollcommand=scrollbar.set)

    def pack_widget(self, widget, position, pad_x, pad_y):
        if position.upper()=="LEFT":
            widget.pack(padx=pad_x, pady=pad_y,side=LEFT)
        elif position.upper()=="RIGHT":
            widget.pack(padx=pad_x, pady=pad_y,side=RIGHT)
        elif position.upper()=="TOP":
            widget.pack(padx=pad_x, pady=pad_y,side=TOP)
        elif position.upper()=="BOTTOM":
            widget.pack(padx=pad_x, pady=pad_y,side=BOTTOM)


class WindowFrame(GroupWidgetActions):
    available_methods=["-> __init(window)","-> pack_frame(position,pad_x,pad_y)","-> resize_frame(x,y)","-> bind_action(key,action)",
                       "-> destroy_all_child_widgets()","-> configure_border(relief,borderwidth)","-> destroy()","-> get_frame()"]
    def __init__(self, window):
        self.frame=Frame(window)
    
    def pack_frame(self, position, pad_x, pad_y):
        super(WindowFrame, self).pack_widget(self.frame, position, pad_x, pad_y)

    def resize_frame(self, x, y):
        self.frame.configure(width=x)
        self.frame.configure(height=y)

    def bind_action(self, key, action):
        self.frame.bind(key, action)
        self.frame.focus_set()

    def configure_border(self,relief,borderwidth):
        self.frame.configure(relief=relief)
        self.frame.configure(borderwidth=borderwidth)

    def destroy_all_child_widgets(self):
        for child_widget in self.frame.winfo_children():
            child_widget.destroy()

    def destroy(self):
        super(WindowFrame, self).destroy_widget(self.frame)

    def get_frame(self):
        return self.frame

        
class WindowButton(GroupWidgetActions):
    available_methods=["-> __init(window,name_action)","-> set_position(row,column,pad_x,pad_y)",
                       "-> configure_text(new_text)","-> configure_action(new_action)","-> insert_image(image_location)",
                       "-> configure_colors(foreground,background)","-> pack_button(position,pad_x,pad_y)","-> destroy()"]
    def __init__(self, window, name, action):
        self.button_text=StringVar()
        self.button_text.set(name)
        self.button=Button(window,text=name,command=action,font='times 10',cursor='hand2',bd=2,\
                           textvariable=self.button_text)

    def set_position(self,row,column,pad_x,pad_y):
        self.button.grid(row=row,column=column, padx=pad_x, pady=pad_y)

    def configure_text(self, new_text):
        self.button.text=new_text
        self.button_text.set(new_text)

    def configure_action(self, new_action):
        self.button.configure(command=new_action)

    def insert_image(self,image_location):
        self.image=PhotoImage(file="{0}".format(image_location))
        self.button.configure(image=self.image)
        self.button.image=self.image    #the image is saved here so garbage collection dosent delete it

    def configure_colors(self,foreground,background):
        self.button.configure(fg=foreground)
        self.button.configure(bg=background)

    def pack_button(self, position, pad_x, pad_y):
        super(WindowButton, self).pack_widget(self.button, position, pad_x, pad_y)

    def destroy(self):
        super(WindowButton, self).destroy_widget(self.button)


class WindowLabel(GroupWidgetActions):
    available_methods=["-> __init(window,name)","->configure_colors(foreground,background,font)",
                       "-> configure_text(new_text)","-> set_position(row,column,pad_x,pad_y)",
                       "-> pack_label(position,pad_x,pad_y)","-> destroy()"]
    def __init__(self, window, name):
        self.label=Label(window,text=name,font="Times 10",fg="White",bg="Black")

    def configure_colors(self, foreground, background, font):
        self.label.configure(foreground=foreground)
        self.label.configure(background=background)
        self.label.configure(font=font)

    def configure_text(self, text):
        self.label.configure(text=text)

    def set_position(self,row,column,pad_x,pad_y):
        self.label.grid(row=row,column=column, padx=pad_x, pady=pad_y)

    def pack_label(self, position, pad_x, pad_y):
        super(WindowLabel, self).pack_widget(self.label, position, pad_x, pad_y)

    def destroy(self):
        super(WindowLabel, self).destroy_widget(self.label)


class WindowEntry(GroupWidgetActions):
    available_methods=["-> __init(window)","-> configure_size(width)","-> configure_font(font,bd)",
                      "-> configure_position(row,column,pad_x,pad_y)","-> configure_entry_text(new_text)",
                      "-> attach_scrollbar(scrollbar)","-> select_range(start,end)","-> pack_entry(position,pad_x,pad_y)",
                      "-> destroy()","-> get_entry()","-> get_entry_widget()"]
    def __init__(self, window):
        self.entry_text=StringVar()
        self.entry=Entry(window,font="Times 10",bd=2, textvariable=self.entry_text)
        self.entry.focus()

    def configure_size(self,width):
        self.entry.configure(width=width)

    def configure_font(self,font,bd):
        self.entry.configure(font=font)
        self.entry.configure(bd=bd)

    def configure_position(self,row,column,pad_x,pad_y):
        self.entry.grid(row=row,column=column, padx=pad_x, pady=pad_y)

    def configure_entry_text(self, new_text):
        self.entry_text.set(new_text)

    def attach_scrollbar(self,scrollbar):
        super(WindowEntry, self).attach_scrollbar(self.entry,"X",scrollbar)

    def select_range(self, start, end):
        if end==END:
            end=len(self.entry_text.get())
        if start>=0 and end<=len(self.entry_text.get()):
            self.entry.select_range(start, end)

    def pack_entry(self,position, pad_x, pad_y):
        super(WindowEntry, self).pack_widget(self.entry,position,pad_x,pad_y)

    def destroy(self):
        super(WindowEntry, self).destroy_widget(self.entry)

    def get_entry(self):
        return self.entry.get()
    def get_entry_widget(self):
        return self.entry


class WindowListbox(GroupWidgetActions):
    available_methods=["-> __init__(window)","-> insert_text(new_text,line)","-> configure_size(width,height)",
                       "-> delete_text(start_line,end_line)","-> pack_listbox(position,pad_x,pad_y)","-> destroy()",
                       "-> get_text_from_index(index)","-> attach_scrollbar(x_or_y,scrollbar)","-> get_current_selection()",
                       "-> get_listbox()"]
    def __init__(self, window):
        self.listbox=Listbox(window)
        self.listbox.focus()

    def insert_text(self,new_text,line):
        temp=""
        for character in new_text:
            if character=="\n":
                self.listbox.insert(line,"{0}".format(temp))
                temp=""
            else:
                temp+=character

    def configure_size(self,width,height):
        self.listbox.configure(width=width)
        self.listbox.configure(height=height)

    def delete_text(self,start_line,end_line):
        self.listbox.delete(start_line,end_line)

    def pack_listbox(self, position, pad_x, pad_y):
        super(WindowListbox, self).pack_widget(self.listbox,position,pad_x,pad_y)

    def destroy(self):
        super(WindowListbox, self).destroy_widget(self.listbox)

    def get_text_from_index(self,index):
        if index!=():
            return self.listbox.get(index)

    def attach_scrollbar(self,x_or_y,scrollbar):
        super(WindowListbox, self).attach_scrollbar(self.listbox,x_or_y.upper(),scrollbar)

    def get_current_selection(self):
        return self.listbox.curselection()
    def get_listbox(self):
        return self.listbox


class WindowScrollbar(GroupWidgetActions):
    available_methods=["-> __init__(window,x_or_y)","-> attach_scrollbar_to_widget(widget)",
                       "-> pack_scrollbar(position,pad_x,pad_y)","-> destroy()","-> get_scrollbar()"]
    def __init__(self,window,x_or_y):
        self.x_or_y=x_or_y.upper()
        self.make_scrollbar(window)

    def make_scrollbar(self,window):
        if self.x_or_y=="X":
            self.scrollbar=Scrollbar(window,orient=HORIZONTAL)
        elif self.x_or_y=="Y":
            self.scrollbar=Scrollbar(window,orient=VERTICAL)

    def attach_to_widget(self,widget):
        if self.x_or_y=="X":
            self.scrollbar.configure(command=widget.xview)
        elif self.x_or_y=="Y":
            self.scrollbar.configure(command=widget.yview)

    def pack_scrollbar(self,position,pad_x,pad_y):
        if self.x_or_y=="Y":
            self.scrollbar.pack(side=position,padx=pad_x,pady=pad_y,fill=Y)
        elif self.x_or_y=="X":
            self.scrollbar.pack(side=position,padx=pad_x,pady=pad_y,fill=X)

    def destroy(self):
        self.scrollbar.destroy()
        
    def get_scrollbar(self):
        return self.scrollbar


class WindowCanvas(GroupWidgetActions):
    available_methods=["-> __init__(frame,width,height)","-> pack_canvas(position,pad_x,pad_y)",
                       "-> configure_size(width,height)","-> add_rectangle(corner1,corner2,corner3,corner4,fill)"]
    def __init__(self,frame,width,height):
        self.canvas=Canvas(frame,width=width,height=height)

    def pack_canvas(self,position,pad_x,pad_y):
        super(WindowCanvas, self).pack_widget(self.canvas,position,pad_x,pad_y)

    def configure_size(self,width,height):
        self.canvas.configure(height=height)
        self.canvas.configure(width=width)

    def add_rectangle(self,corner1,corner2,corner3,corner4,fill):
        self.canvas.create_rectangle(corner1,corner2,corner3,corner4,fill=fill)

    def add_text(self,x,y,text,color,font):
        self.canvas.create_text(x,y,text=text,fill=color,font=font)

    def delete_all_contents(self):
        self.canvas.delete(ALL)


if __name__=="__main__":
    print_all()

