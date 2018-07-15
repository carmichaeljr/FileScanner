#File Scanner
#Made by Jack Carmichael
"""
===================================================================================
Object--------------------Parameters--------------------Inheritance
 -AppWindow()             -void                           -object
 -FileInfo()              -frame                          -object
 -CurrentFileInfo()       -frame                          -object
 -AcanGui()               -file_listboxes,progress_bar    -object
 -ProgressBar()           -frame,length,height            -TkinterWrapper.WindowCanvas
 -Scan()                  -directory,scan_gui             -object
 -FIleType()              -file_extension,file_consensus  -object
 -FileTypeEditor()        -parrent_window,edit_type       -object
 -SetDirWindow()          -parent_window                  -object
 -DirectoryListbox()      -frame,companion_text_entry     -TkinterWrapper.WindowListbox
 -ComputerDirectory()     -void                           -object
 -SavedInfo()             -void                           -object
===================================================================================
Still to do:
    -bind left click event with filetype listboxes. Options are to add to file type list
"""

import os
import time
from functools import partial
import UserErrorMessage
import TkinterWrapper
import FileWrapper

ALAPHABET="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
UP_TRIANGLE="{0}".format('\u25B2')
DOWN_TRIANGLE="{0}".format('\u25BC')
LEFT_TRIANGLE="{0}".format('\u25C0')
RIGHT_TRIANGLE="{0}".format('\u25B6')
SMALL_RIGHT_TRIANGLE="{0}".format('\u25B8')

#SPLIT UP! Make information frame a class and call update methods on it
class AppWindow(object):
    def __init__(self):
        self.app_window=TkinterWrapper.Window("File Scanner")
        self.update_scan_flags(False,False,False)
        self.__setup_window()
        self.__setup_menu()
        self.__setup_frames()
        self.update_frames()
        self.app_window.start_mainloop()

    def __setup_window(self):
        self.app_window.remove_min_max_buttons(False)
        self.app_window.resizable(False,False)

    def __setup_menu(self):
        self.menu=TkinterWrapper.WindowMenu(self.app_window.get_window())
        self.file_cascade=TkinterWrapper.WindowMenuCascade(self.app_window.get_window(),False)
        self.file_cascade.add_item_to_cascade("Quit",self.app_window.destroy_window)
        self.edit_cascade=TkinterWrapper.WindowMenuCascade(self.app_window.get_window(),False)
        self.edit_cascade.add_item_to_cascade("Known-Good Filetypes",partial(self.add_known_file_type,"KnownGood"))
        self.edit_cascade.add_item_to_cascade("Known-Bad Filetypes",partial(self.add_known_file_type,"KnownBad"))
        self.menu.add_cascade_to_menu("File",self.file_cascade.get_cascade())
        self.menu.add_cascade_to_menu("Edit",self.edit_cascade.get_cascade())

    def __setup_frames(self):
        self.process_information_frame=TkinterWrapper.WindowFrame(self.app_window.get_window())
        self.found_files_frame=TkinterWrapper.WindowFrame(self.app_window.get_window())
        self.current_file_frame=TkinterWrapper.WindowFrame(self.app_window.get_window())
        for item in [[self.process_information_frame,"top"],[self.current_file_frame,"top"],[self.found_files_frame,"top"]]:
            item[0].pack_frame(item[1],0,0)
        self.file_information_frame=FileInfo(self.found_files_frame.get_frame())
        self.current_file_information_frame=CurrentFileInfo(self.current_file_frame)

    def update_frames(self):
        self.process_information_frame.destroy_all_child_widgets()
        self.update_process_information_frame()
        self.file_information_frame.update_frame(self.directory_set,self.process_running,self.scan_finished)
        self.current_file_information_frame.update_frame(self.process_running)

    def update_process_information_frame(self):
        if self.process_running==False and self.directory_set==False and self.scan_finished==False:
            self.update_process_information_frame_for_idle("Please select a folder to scan.","Set Search Folder",self.open_dir_selection_dialogbox)
        elif self.process_running==False and self.directory_set==True and self.scan_finished==False:
            self.update_process_information_frame_for_idle("Set to scan: {0}".format(saved_information.get_directory_to_scan()),"Scan",self.commence_scan)
            self.add_button_to_process_information_frame("Change Folder To Scan",self.open_dir_selection_dialogbox)
        elif self.process_running==True and self.directory_set==True and self.scan_finished==False:
            self.update_process_information_frame_for_task()
        elif self.process_running==False and self.directory_set==False and self.scan_finished==True:
            self.update_process_information_frame_for_idle("Scan Completed","Scan Something Else",self.open_dir_selection_dialogbox)

    def update_process_information_frame_for_idle(self,top_text,button_text,button_action):
        label=TkinterWrapper.WindowLabel(self.process_information_frame.get_frame(),"{0}".format(top_text))
        label.configure_colors("dodgerblue2","grey95","times 11")
        label.pack_label("top",0,0)
        self.add_button_to_process_information_frame(button_text,button_action)
    def add_button_to_process_information_frame(self,button_text,button_action):
        button=TkinterWrapper.WindowButton(self.process_information_frame.get_frame(),"{0}".format(button_text),button_action)
        button.pack_button("top",0,1)

    def update_process_information_frame_for_task(self):
        top_text=TkinterWrapper.WindowLabel(self.process_information_frame.get_frame(),"Scanning....")
        top_text.configure_colors("grey20","grey95","times 14")
        top_text.pack_label("top",0,0)
        top_text=TkinterWrapper.WindowLabel(self.process_information_frame.get_frame(),"Scanning:  {0}".format(saved_information.get_directory_to_scan()))
        top_text.configure_colors("dodgerblue2","grey95","times 10")
        top_text.pack_label("top",0,0)
        self.progress_bar=Progressbar(self.process_information_frame.get_frame(),400,30)

    def add_known_file_type(self,type_consensus):
        dialog_box=FileTypeEditor(self.app_window.get_window(),type_consensus)

    def open_dir_selection_dialogbox(self):
        directory_selection=SetDirWindow(self.app_window.get_window())
        if directory_selection.get_saved_directory!="":
            saved_information.set_directory_to_scan(directory_selection.get_saved_directory())
            self.update_scan_flags(True,False,False)
            self.update_frames()

    def commence_scan(self):
        self.update_scan_flags(True,True,False)
        self.update_frames()
        scan_gui=ScanGUI(self.file_information_frame.get_listboxes(),self.progress_bar,self.current_file_information_frame)
        self.scan=Scan(saved_information.get_directory_to_scan(),scan_gui)
        self.scan.start()
        scan_gui.start_checking_for_selection()
        self.update_scan_flags(False,False,True)
        self.update_frames()

    def update_scan_flags(self,directory_set_flag,process_running_flag,scan_finished_flag):
        self.process_running=process_running_flag
        self.directory_set=directory_set_flag
        self.scan_finished=scan_finished_flag


class FileInfo(object):
    def __init__(self,frame):
        self.frame=frame
        self.__setup_file_types_frames()

    def __setup_file_types_frames(self):
        self.ok_files_frame=TkinterWrapper.WindowFrame(self.frame)
        self.bad_files_frame=TkinterWrapper.WindowFrame(self.frame)
        self.unknown_files_frame=TkinterWrapper.WindowFrame(self.frame)
        for frame in [[self.ok_files_frame,"left"],[self.bad_files_frame,"left"],[self.unknown_files_frame,"left"]]:
            frame[0].pack_frame(frame[1],0,0)

    def update_frame(self,directory_set,process_running,scan_finished):
        self.destroy_all_widgets(scan_finished)
        if (process_running==False or directory_set==False) and scan_finished!=True:
            for item in [[self.ok_files_frame,"Ok"],[self.bad_files_frame,"Potentialy Harmfull"],[self.unknown_files_frame,"Unknown"]]:
                item[0].configure_border("ridge",2)
                self.insert_file_explaning_note(item[0],item[1])
        elif process_running==True and directory_set==True:
            self.listboxes=[]
            self.update_file_frame_for_task(self.ok_files_frame.get_frame(),"Ok")
            self.update_file_frame_for_task(self.bad_files_frame.get_frame(),"Potentialy Harmfull")
            self.update_file_frame_for_task(self.unknown_files_frame.get_frame(),"Unknown")

    def destroy_all_widgets(self,scan_finished):
        if scan_finished!=True:
            for frame in [self.ok_files_frame,self.bad_files_frame,self.unknown_files_frame]:
                frame.destroy_all_child_widgets()

    def insert_file_explaning_note(self,frame,text):
        information_label=TkinterWrapper.WindowLabel(frame.get_frame(),"{0} files will be\nshown here after a scan".format(text))
        information_label.configure_colors("grey50","grey95","times 10")
        information_label.pack_label("top",0,2)

    def update_file_frame_for_task(self,frame,text):
        label=TkinterWrapper.WindowLabel(frame,"{0} Files:".format(text))
        label.configure_colors("grey60","grey95","times 12")
        label.pack_label("top",0,0)
        self.setup_textbox_frame(frame)
        self.setup_textbox_x_scrollbar_frame(frame)

    def setup_textbox_frame(self,file_frame):
        frame=TkinterWrapper.WindowFrame(file_frame)
        frame.pack_frame("top",0,0)
        listbox=TkinterWrapper.WindowListbox(frame.get_frame())
        listbox.pack_listbox("left",0,0)
        listbox.configure_size(40,30)
        scrollbar=TkinterWrapper.WindowScrollbar(frame.get_frame(),"y")
        scrollbar.attach_to_widget(listbox.get_listbox())
        listbox.attach_scrollbar("y",scrollbar.get_scrollbar())
        scrollbar.pack_scrollbar("left",0,0)
        self.listboxes.append(listbox)

    def setup_textbox_x_scrollbar_frame(self,file_frame,):
        frame=TkinterWrapper.WindowFrame(file_frame)
        frame.pack_frame("top",0,0)
        scrollbar=TkinterWrapper.WindowScrollbar(frame.get_frame(),"x")
        scrollbar.attach_to_widget(self.listboxes[len(self.listboxes)-1].get_listbox())
        self.listboxes[len(self.listboxes)-1].attach_scrollbar("x",scrollbar.get_scrollbar())
        scrollbar.pack_scrollbar("top",0,0)        

    def get_listboxes(self):
        return self.listboxes


class CurrentFileInfo(object):
    def __init__(self,frame):
        self.frame=frame
        self.__setup_dummy_frame()
        self.setup_frames()
        self.make_labels()

    def __setup_dummy_frame(self):
        dummy_frame=TkinterWrapper.WindowFrame(self.frame.get_frame())
        dummy_frame.pack_frame("top",0,0)

    def setup_frames(self):
        self.top_frame=TkinterWrapper.WindowFrame(self.frame.get_frame())
        self.bottom_frame=TkinterWrapper.WindowFrame(self.frame.get_frame())
        for frame,position in [[self.top_frame,"top"],[self.bottom_frame,"top"]]:
            frame.pack_frame(position,0,0)

    def make_labels(self):
        self.file_fraction=TkinterWrapper.WindowLabel(self.top_frame.get_frame(),"")
        self.file_fraction.configure_colors("grey40","grey95","times 11")
        self.current_file=TkinterWrapper.WindowLabel(self.bottom_frame.get_frame(),"Current File:")
        self.current_file.configure_colors("grey40","grey95","times 10")
        self.file_entry=TkinterWrapper.WindowEntry(self.bottom_frame.get_frame())
        self.file_entry.configure_size(115)

    def update_frame(self,process_running):
        if process_running==True:
            self.file_fraction.pack_label("top",0,0)
            self.current_file.pack_label("left",0,0)
            self.file_entry.pack_entry("left",0,0)
        else:
            self.top_frame.destroy()
            self.bottom_frame.destroy()
            self.setup_frames()
            self.make_labels()

    def update_file_fraction(self,numerator,denominator):
        self.file_fraction.configure_text("{0} out of {1} files scanned".format(numerator,denominator))
    def update_current_file(self,current_file_directory):
        self.file_entry.configure_entry_text("{0}".format(current_file_directory))


class ScanGUI(object):
    def __init__(self,file_listboxes,progress_bar,current_info):
        self.file_listboxes=file_listboxes
        self.progress_bar=progress_bar
        self.current_file_information=current_info
        self.selections=[["",""],["",""],["",""]]
        self.listbox_being_used=[False,False,False]

    def update_file_lists(self,files):
        self.file_list=files
        self.check_for_selection()
        for x in range(0,3):
            if self.listbox_being_used[x]==False:
                self.file_listboxes[x].delete_text(0,"end")
        for file in files:
            if (file.get_file_consensus()=="KnownGood" and self.listbox_being_used[0]==False) or\
               (file.get_file_consensus()=="KnownBad" and self.listbox_being_used[1]==False) or\
               (file.get_file_consensus()=="Unknown" and self.listbox_being_used[2]==False):
                self.add_item_to_listbox(file.get_file_consensus(),file.get_file_extension(),file.get_number_of_files())

    def add_item_to_listbox(self,item_consensus,item_name,number_of_item):
        if item_consensus=="KnownGood":
            self.file_listboxes[0].insert_text("{0} {1:4s} Files ({2})\n".format(RIGHT_TRIANGLE,item_name,number_of_item),"end")
        elif item_consensus=="KnownBad":
            self.file_listboxes[1].insert_text("{0} {1:4s} Files ({2})\n".format(RIGHT_TRIANGLE,item_name,number_of_item),"end")
        elif item_consensus=="Unknown":
            self.file_listboxes[2].insert_text("{0} {1:4s} Files ({2})\n".format(RIGHT_TRIANGLE,item_name,number_of_item),"end")

    def update_progress_bar(self,percentage,part,total_parts):
        self.progress_bar.update(percentage,part,total_parts)

    def update_current_information(self,numerator,denominator,current_file_directory):
        self.current_file_information.update_file_fraction(numerator,denominator)
        self.current_file_information.update_current_file(current_file_directory)

    def start_checking_for_selection(self):
        self.check_for_selection()
        #This is not a good solution, better way to check every 250ms?
        self.file_listboxes[0].get_listbox().after(250,self.start_checking_for_selection)

    def check_for_selection(self):
        for x in range(0,3):
            self.selections[x][0]=self.file_listboxes[x].get_current_selection()
            self.selections[x][0]=self.file_listboxes[x].get_text_from_index(self.selections[x][0])
        for x in range(0,3):
            if self.selections[x][0]!=self.selections[x][1] and self.selections[x][0]!=None:
                print("Selection in listbox {0} has changed to: {1}".format(x,self.selections[x][0]))
                self.selection_actions(x)
                self.selections[x][1]=self.selections[x][0]

    def selection_actions(self,listbox):
        if RIGHT_TRIANGLE in self.selections[listbox][0]:
            self.show_file_type_places(self.selections[listbox][0],listbox)
        elif LEFT_TRIANGLE in self.selections[listbox][0]:
            self.go_back_to_file_type_list(listbox)
        elif SMALL_RIGHT_TRIANGLE in self.selections[listbox][0]:
            self.open_file_explorer(self.selections[listbox][0])

    def show_file_type_places(self,selection,listbox):
        self.listbox_being_used[listbox]=True
        print("Selection: "+selection)
        for file in self.file_list:
            if file.get_file_extension()==self.get_file_extension_from_selection(selection):
                self.insert_file_places(file,listbox)

    def get_file_extension_from_selection(self,selection):
        file_extension=""
        for x in range(2,len(selection)):
            if selection[x]!=" " and selection[x]!="(" and selection[x]!=")":
                file_extension+=selection[x]
            else:
                return file_extension

    def insert_file_places(self,file_type,listbox):
        self.file_listboxes[listbox].delete_text(0,"end")
        self.add_directional_information(listbox)
        for item in file_type.get_file_type_locations():
            self.file_listboxes[listbox].insert_text("{0} {1}\n".format(SMALL_RIGHT_TRIANGLE,item),"end")

    def add_directional_information(self,listbox):
        self.file_listboxes[listbox].insert_text("{0} Back to File List\n".format(LEFT_TRIANGLE),"end")
        self.file_listboxes[listbox].insert_text("{0} {1} Files\n".format(DOWN_TRIANGLE,self.get_file_extension_from_selection\
                                                                          (self.selections[listbox][0])),"end")

    def go_back_to_file_type_list(self,listbox):
        self.listbox_being_used[listbox]=False
        self.file_listboxes[listbox].delete_text(0,"end")
        for file in self.file_list:
            if file.get_file_consensus()=="KnownGood" and listbox==0:
                self.add_item_to_listbox("KnownGood",file.get_file_extension(),file.get_number_of_files())
            elif file.get_file_consensus()=="KnownBad" and listbox==1:
                self.add_item_to_listbox("KnownBad",file.get_file_extension(),file.get_number_of_files())
            elif file.get_file_consensus()=="Unknown" and listbox==2:
                self.add_item_to_listbox("Unknown",file.get_file_extension(),file.get_number_of_files())

    def open_file_explorer(self,file_location):
        file_location=file_location[2:len(file_location):1]
        for x in range(len(file_location)-1,0,-1):
            if file_location[x]=="\\":
                file_location=file_location[0:x:1]
                break
        os.startfile(r"{0}".format(file_location))


class Progressbar(TkinterWrapper.WindowCanvas):
    def __init__(self,frame,length,height):
        self.length=length
        self.height=height
        self.percentage=0
        self.rectangle_point=0
        super(Progressbar, self).__init__(frame,self.length,height)
        super(Progressbar, self).pack_canvas("top",0,0)

    def update(self,percentage,part,total_parts):
        self.percentage=percentage
        super(Progressbar, self).delete_all_contents()
        self.update_part(part,total_parts)
        self.update_rectangle()
        self.update_text()
        self.canvas.update()

    def update_part(self,part,total_parts):
        super(Progressbar, self).add_text(self.length/2,6,"Part {0} of {1}".format(part,total_parts),"grey10","times 9")

    def update_rectangle(self):
        super(Progressbar, self).add_rectangle(2,13,self.length,self.height,"lightblue")
        if self.percentage=="GoThrough":
            self.calculate_go_through_rectangle()
            super(Progressbar, self).add_rectangle(self.rectangle_point,13,self.rectangle_point+100,self.height,"cornflowerblue")
        else:
            self.rectangle_point=self.length*self.percentage
            super(Progressbar, self).add_rectangle(2,13,self.rectangle_point,self.height,"cornflowerblue")

    def calculate_go_through_rectangle(self):
        if self.rectangle_point>=self.length:
            self.rectangle_point=0
        else:
            self.rectangle_point+=0.05
            
    def update_text(self):
        if type(self.percentage).__name__!='str':
            if self.percentage<=0.95:
                super(Progressbar, self).add_text(370,self.height-8,"{0}%".format(int(self.percentage*100)),"grey10","times 14")
            else:
                super(Progressbar, self).add_text(370,self.height-8,"{0}%".format(int(self.percentage*100)),"grey80","times 14")

        
class Scan(object):
    def __init__(self,directory,scan_gui):
        self.scan_directory=directory
        self.scan_gui=scan_gui
        self.set_scan_variables()
        self.known_good_filetypes=saved_information.get_known_good_filetypes()
        self.known_bad_filetypes=saved_information.get_known_bad_filetypes()
        
    def set_scan_variables(self):
        self.current_directory=""
        self.scaned_files=0
        self.file_extensions=[]
        self.file_type_object_list=[]
                
    def start(self):
        self.set_scan_variables()
        self.set_number_of_files()
        for root, dirs, files in os.walk("{0}".format(self.scan_directory), topdown=True):
            for name in files:
                self.current_directory="{0}\\{1}".format(root,name)
                self.scan_file(root,name)
                self.update_scan_gui(2)

    def set_number_of_files(self):
        print(self.scan_directory)
        self.number_of_files=0
        for root, dirs, files in os.walk("{0}".format(self.scan_directory), topdown=True):
            self.number_of_files+=len(files)
            self.update_scan_gui(1)
        print("Number of files: {0}".format(self.number_of_files))

    def scan_file(self,root,file):
        file_name,file_extension=os.path.splitext("{0}".format(file))
        self.append_file_type(file_extension)
        self.update_file_type_object_list(root,file_extension,file_name)
        self.scaned_files+=1

    def append_file_type(self,file_extension):
        if file_extension not in self.file_extensions:
            self.file_extensions.append(file_extension)

    def update_file_type_object_list(self,file_path,file_extension,file_name):
        for item in self.file_type_object_list:
            if item.get_file_extension()==file_extension:
                item.add_file_to_list("{0}\\{1}".format(file_path,file_name))
                break
        else:
            self.check_file_type_and_add_to_list(file_path,file_extension,file_name)

    def check_file_type_and_add_to_list(self,file_path,file_extension,file_name):
        if file_extension in self.known_good_filetypes:
            initilizer="KnownGood"
        elif file_extension in self.known_bad_filetypes:
            initilizer="KnownBad"
        else:
            initilizer="Unknown"
        new_file_type=FileType(file_extension,initilizer)
        new_file_type.add_file_to_list("{0}\\{1}".format(file_path,file_name))
        self.file_type_object_list.append(new_file_type)

    def update_scan_gui(self,part):
        if part==1:
            percent="GoThrough"
        elif part==2:
            percent=self.scaned_files/self.number_of_files
            self.scan_gui.update_current_information(self.scaned_files,self.number_of_files,self.current_directory)
        self.scan_gui.update_progress_bar(percent,part,2)
        self.scan_gui.update_file_lists(self.file_type_object_list)


class FileType(object):
    def __init__(self,file_extension,file_consensus):
        self.file_extension=file_extension
        self.file_consensus=file_consensus
        self.file_type_locations=[]

    def get_file_extension(self):
        return self.file_extension
    def get_file_consensus(self):
        return self.file_consensus
    def get_number_of_files(self):
        return len(self.file_type_locations)
    def get_file_type_locations(self):
        return self.file_type_locations
    
    def add_file_to_list(self,file_path):
        self.file_type_locations.append("{0}{1}".format(file_path,self.file_extension))

    def print_information(self):
        print("File extenstion: {0}".format(self.file_extension))
        for item in self.file_type_locations:
            print("  -> {0}".format(item),end="")
            print("\t{0:7s} Consensus: {1}".format("",self.file_consensus))
            

class FileTypeEditor(object):
    def __init__(self,parrent_window,edit_type):
        self.edit_type=edit_type
        self.set_file_type_list()
        self.window=TkinterWrapper.DialogBox(parrent_window,"Edit {0} File Types".format(edit_type))
        self.__setup_window()
        self.__setup_frames()
        self.__setup_left_frame()
        self.__setup_right_frame()
        self.__setup_bottom_frame()
        self.update_listbox_text()

    def set_file_type_list(self):
        if self.edit_type=="KnownGood":
            self.file_type_list=saved_information.get_known_good_filetypes()
        elif self.edit_type=="KnownBad":
            self.file_type_list=saved_information.get_known_bad_filetypes()
        self.delete_list=[]
        self.append_list=[]
            
    def __setup_window(self):
        self.window.remove_min_max_buttons(True)
        self.window.resizable(False,False)
        self.window.bind_action("<Return>",self.add_file_type)

    def __setup_frames(self):
        self.top_frame=TkinterWrapper.WindowFrame(self.window.get_window())
        self.bottom_frame=TkinterWrapper.WindowFrame(self.window.get_window())
        self.left_frame=TkinterWrapper.WindowFrame(self.top_frame.get_frame())
        self.right_frame=TkinterWrapper.WindowFrame(self.top_frame.get_frame())
        for item in [[self.top_frame,"top"],[self.left_frame,"left"],[self.right_frame,"right"],
                     [self.bottom_frame,"bottom"]]:
            item[0].pack_frame(item[1],1,0)
        self.left_frame.configure_border("ridge",2)

    def __setup_right_frame(self):
        self.file_type_listbox=TkinterWrapper.WindowListbox(self.right_frame.get_frame())
        self.file_type_listbox.configure_size(20,10)
        self.file_type_listbox.pack_listbox("left",0,0)
        y_scrollbar=TkinterWrapper.WindowScrollbar(self.right_frame.get_frame(),"y")
        y_scrollbar.attach_to_widget(self.file_type_listbox.get_listbox())
        self.file_type_listbox.attach_scrollbar("y",y_scrollbar.get_scrollbar())
        y_scrollbar.pack_scrollbar("left",0,0)

    def __setup_left_frame(self):
        self.insert_explanitory_label(self.left_frame.get_frame(),"Enter File Extension to Add:")
        self.__setup_entry_frame()
        self.insert_explanitory_label(self.left_frame.get_frame(),"Select a File Extension to Delete")
        self.insert_button(self.left_frame.get_frame(),"Delete",self.delete_file_type,"top")
        self.error_frame=TkinterWrapper.WindowFrame(self.left_frame.get_frame())
        self.error_frame.pack_frame("top",0,0)
        
    def __setup_entry_frame(self):
        entry_frame=TkinterWrapper.WindowFrame(self.left_frame.get_frame())
        entry_frame.pack_frame("top",0,0)
        self.file_type_entry=TkinterWrapper.WindowEntry(entry_frame.get_frame())
        self.file_type_entry.configure_size(20)
        self.file_type_entry.pack_entry("left",0,2)
        self.insert_button(entry_frame.get_frame(),"Add",self.add_file_type,"left")

    def __setup_bottom_frame(self):
        self.insert_button(self.bottom_frame.get_frame(),"Cancel",partial(self.window.destroy_window,False),"left")
        self.insert_button(self.bottom_frame.get_frame(),"Save",self.save_all_file_types_and_exit,"left")

    def insert_explanitory_label(self,frame,text):
        label=TkinterWrapper.WindowLabel(frame,text)
        label.configure_colors("dodgerblue2","grey95","times 11")
        label.pack_label("top",0,10)

    def insert_button(self,frame,button_text,button_action,side):
        button=TkinterWrapper.WindowButton(frame,button_text,button_action)
        button.pack_button(side,2,2)

    def add_file_type(self,*args):
        new_file_type=self.file_type_entry.get_entry()
        if len(new_file_type)>0 and new_file_type[0]=="." and (new_file_type not in self.file_type_list):
            self.file_type_list.append(new_file_type)
            self.append_list.append(new_file_type)
            self.update_listbox_text()
            self.file_type_entry.configure_entry_text("")
        else:
            user_error=UserErrorMessage.UserErrorMessage(self.error_frame.get_frame(),"Please enter a valid file type")
            self.file_type_entry.select_range(0,"end")
            
    def delete_file_type(self):
        selection=self.file_type_listbox.get_current_selection()
        selection=self.file_type_listbox.get_text_from_index(selection)
        if selection!=None:
            for x in range(0,len(self.file_type_list)):
                if self.file_type_list[x]==selection:
                    self.delete_list.append(self.file_type_list[x])
                    del(self.file_type_list[x])
                    break
            self.update_listbox_text()
        else:
            user_error=UserErrorMessage.UserErrorMessage(self.error_frame.get_frame(),"Please select a file to delete")
        
    def update_listbox_text(self):
        self.file_type_listbox.delete_text(0,"end")
        for item in self.file_type_list:
            self.file_type_listbox.insert_text("{0}\n".format(item),"end")

    def save_all_file_types_and_exit(self):
        for item in self.delete_list:
            saved_information.delete_file_type(self.edit_type,item)
        for item in self.append_list:
            saved_information.add_file_type(self.edit_type,item)
        self.window.destroy_window(False)

            
class SetDirWindow(object):
    def __init__(self,parent_window):
        self.window=TkinterWrapper.DialogBox(parent_window,"Choose Folder")
        self.directory_to_search=""
        self.__setup_window()
        self.__setup_frames()
        self.__setup_information_frame()
        self.__setup_directory_frame()
        self.__setup_button_frame()
        self.window.start_mainloop()

    def __setup_window(self):
        self.window.remove_min_max_buttons(True)
        self.window.resizable(False,False)

    def __setup_frames(self):
        self.information_frame=TkinterWrapper.WindowFrame(self.window.get_window())
        self.directory_frame=TkinterWrapper.WindowFrame(self.window.get_window())
        self.button_frame=TkinterWrapper.WindowFrame(self.window.get_window())
        self.information_frame.pack_frame("top",0,0)
        self.directory_frame.pack_frame("top",0,0)
        self.button_frame.pack_frame("top",0,0)

    def __setup_information_frame(self):
        description_label=TkinterWrapper.WindowLabel(self.information_frame.get_frame(),"")
        description_label.configure_text("Please chose a file to search from the list below:")
        description_label.configure_colors("grey20","grey95","times 11")
        description_label.pack_label("top",0,5)

    def __setup_directory_frame(self):
        self.__setup_directory_entry_frame()
        self.__setup_directory_listbox_frame()

    def __setup_directory_entry_frame(self):
        directory_entry_frame=TkinterWrapper.WindowFrame(self.directory_frame.get_frame())
        directory_entry_frame.pack_frame("top",0,0)
        current_directory_label=TkinterWrapper.WindowLabel(directory_entry_frame.get_frame(),"Current Directory:\n")
        current_directory_label.pack_label("left",0,0)
        current_directory_label.configure_colors("dodgerblue2","grey95","times 10")
        self.current_directory_entry=TkinterWrapper.WindowEntry(directory_entry_frame.get_frame())
        self.current_directory_entry.configure_size(65)
        self.current_directory_entry.pack_entry("top",0,0)
        x_scrollbar=TkinterWrapper.WindowScrollbar(directory_entry_frame.get_frame(),"x")
        x_scrollbar.attach_to_widget(self.current_directory_entry.get_entry_widget())
        self.current_directory_entry.attach_scrollbar(x_scrollbar.get_scrollbar())
        x_scrollbar.pack_scrollbar("bottom",0,0)

    def __setup_directory_listbox_frame(self):
        directory_listbox_frame=TkinterWrapper.WindowFrame(self.directory_frame.get_frame())
        directory_listbox_frame.pack_frame("top",0,0)
        self.dir_listbox=DirectoryListbox(directory_listbox_frame.get_frame(),self.current_directory_entry)

    def __setup_button_frame(self):
        self.search_button=TkinterWrapper.WindowButton(self.button_frame.get_frame(),"Scan",self.set_directory_and_destory_window)
        self.search_button.pack_button("top",0,0)

    def set_directory_and_destory_window(self):
        self.directory_to_search=self.current_directory_entry.get_entry()
        print("Directory to scan: "+self.directory_to_search)
        self.window.destroy_window(True)
    def get_saved_directory(self):
        return self.directory_to_search
        

#Might have to split up into two classes: DirectoryListboxFormating and DirectoryListboxActions
class DirectoryListbox(TkinterWrapper.WindowListbox):
    def __init__(self,frame,companion_text_entry):
        self.frame=frame
        self.selections=["",""]
        self.current_directory_entry=companion_text_entry
        self.computer_directory=ComputerDirectory()
        self.__setup_listbox_frame()
        self.__setup_error_frame()
        self.insert_harddrives()
        self.start_checking_for_selection()

    def __setup_listbox_frame(self):
        self.listbox_frame=TkinterWrapper.WindowFrame(self.frame)
        self.listbox_frame.pack_frame("top",0,0)
        super(DirectoryListbox, self).__init__(self.listbox_frame.get_frame())
        super(DirectoryListbox, self).pack_listbox("left",0,0)
        super(DirectoryListbox, self).configure_size(80,10)
        self.__setup_scrollbar()
    def __setup_scrollbar(self):
        y_scrollbar=TkinterWrapper.WindowScrollbar(self.listbox_frame.get_frame(),"y")
        y_scrollbar.attach_to_widget(super(DirectoryListbox, self).get_listbox())
        super(DirectoryListbox, self).attach_scrollbar("y",y_scrollbar.get_scrollbar())
        y_scrollbar.pack_scrollbar("left",0,0)

    def __setup_error_frame(self):
        self.error_frame=TkinterWrapper.WindowFrame(self.frame)
        self.error_frame.pack_frame("top",0,0)

    def insert_harddrives(self):
        super(DirectoryListbox, self).delete_text(0,"end")
        for harddrive in self.computer_directory.get_harddrives():
            print(harddrive)
            super(DirectoryListbox, self).insert_text("{0} {1}\n".format(RIGHT_TRIANGLE,harddrive),"end")

    def start_checking_for_selection(self):
        self.selections[0]=super(DirectoryListbox, self).get_current_selection()
        self.selections[0]=super(DirectoryListbox, self).get_text_from_index(self.selections[0])
        if self.selections[0]!=self.selections[1] and self.selections[0]!=None:
            print("Selection changed to: {0}".format(self.selections[0]))
            self.selection_actions()
            self.selections[1]=self.selections[0]
        self.frame.after(250,self.start_checking_for_selection)

    def selection_actions(self):
        if RIGHT_TRIANGLE in self.selections[0]:
            self.go_to_subdirectory()
        elif LEFT_TRIANGLE in self.selections[0]:
            self.go_up_directory()

    def go_to_subdirectory(self):
        self.computer_directory.set_current_directory(self.get_rid_of_arrows_in_directory(self.selections[0]))
        subdirectories=self.computer_directory.get_sub_directories()
        if subdirectories!="ACCESS DENIED":
            self.update_directory_entry()
            self.add_directional_information()
            for subdirectory in subdirectories:
                super(DirectoryListbox, self).insert_text("  {0} {1}\n".format(RIGHT_TRIANGLE,subdirectory),"end")
        else:
            error_message=UserErrorMessage.UserErrorMessage(self.error_frame.get_frame(),"Access to file was denied.")
            self.go_up_directory()
            print("Access to file denied")

    def add_directional_information(self):
        super(DirectoryListbox, self).delete_text(0,"end")
        super(DirectoryListbox, self).insert_text("{0} Back to {1}\n".format(LEFT_TRIANGLE,self.computer_directory.get_previous_directory()),"end")
        super(DirectoryListbox, self).insert_text("{0} {1}\n".format(DOWN_TRIANGLE,self.computer_directory.get_current_directory()),"end")

    def get_rid_of_arrows_in_directory(self,directory):
        for x in range(0,len(directory)):
            if (directory[x]!=RIGHT_TRIANGLE and directory[x]!=DOWN_TRIANGLE and directory[x]!=LEFT_TRIANGLE)\
               and ((x!=1 or x!=2 or x!=3) and (directory[x]!=" ")):
                directory=directory[x:len(directory):1]
                break
        return directory

    def go_up_directory(self):
        self.computer_directory.trim_from_current_directory(1)
        self.update_directory_entry()
        new_directories=self.computer_directory.get_sub_directories()
        if new_directories!=self.computer_directory.get_harddrives():
            self.add_directional_information()
        else:
            super(DirectoryListbox, self).delete_text(0,"end")
        for new_directory in new_directories:
            super(DirectoryListbox, self).insert_text("   {0} {1}\n".format(RIGHT_TRIANGLE,new_directory),"end")

    def update_directory_entry(self):
        self.current_directory_entry.configure_entry_text(self.computer_directory.get_formated_current_directory())
        
        
class ComputerDirectory(object):
    def __init__(self):
        self.harddrives=[]
        self.current_directory=[]
        self.formated_current_directory=""
        self.find_harddrives()

    def find_harddrives(self):
        self.harddrives=["{0}:".format(drive) for drive in ALAPHABET if os.path.exists("{0}:\\".format(drive))]
    def get_harddrives(self):
        return self.harddrives

    def set_current_directory(self, directory):
        self.current_directory.append("{0}\\".format(directory))
        self.set_formated_current_directory()
        print("Current Dir: ",self.current_directory)

    def get_current_directory(self):
        return self.current_directory[len(self.current_directory)-1]
    def get_previous_directory(self):
        if len(self.current_directory)==1:
            return "Hard drives"
        else:
            return self.current_directory[(len(self.current_directory)-1)-1]

    def trim_from_current_directory(self,number_of_levels):
        self.delete_last_directories(number_of_levels)
        self.set_formated_current_directory()
        print("Current Dir: ",self.current_directory)

    def delete_last_directories(self,number_of_levels):
        for x in range(0,len(self.current_directory)):
            if len(self.current_directory)-x<=number_of_levels:
                del(self.current_directory[x])
                break
        print(self.current_directory)

    def get_sub_directories(self):
        if len(self.current_directory)==0:
            return self.harddrives
        else:
            try:
                os.listdir(self.formated_current_directory)
            except:
                print("Error opening file")
                return "ACCESS DENIED"
            else:
                sub_directories=[sub_dir for sub_dir in os.listdir(self.formated_current_directory) if os.path.isdir(os.path.join(self.formated_current_directory, sub_dir))]
                print(sub_directories)
                return sub_directories
    
    def set_formated_current_directory(self):
        self.formated_current_directory=""
        for x in range(0,len(self.current_directory)):
            self.formated_current_directory="{0}{1}".format(self.formated_current_directory,self.current_directory[x])
            print("Formated Cur Dir: "+self.formated_current_directory)
    def get_formated_current_directory(self):
        return self.formated_current_directory


class SavedInfo(object):
    def __init__(self):
        self.known_good_file=FileWrapper.File(os.curdir,"KnownGoodFiletypes.txt")
        self.known_bad_file=FileWrapper.File(os.curdir,"KnownBadFiletypes.txt")
        self.__setup_filetypes()
        self.directory_to_scan=""

    def __setup_filetypes(self):
        self.known_good_filetypes=self.known_good_file.read_lines(0,'end')
        self.known_bad_filetypes=self.known_bad_file.read_lines(0,'end')

    def get_known_good_filetypes(self):
        good_file_types=self.known_good_filetypes
        return good_file_types[0:len(good_file_types)]
    def get_known_bad_filetypes(self):
        bad_file_types=self.known_bad_filetypes
        return bad_file_types[0:len(bad_file_types)]

    def add_file_type(self,file_consensus,file_type):
        if file_consensus=="KnownGood":
            self.known_good_filetypes.append(file_type)
        elif file_consensus=="KnownBad":
            self.known_bad_filetypes.append(file_type)
    def delete_file_type(self,file_consensus,file_type):
        if file_consensus=="KnownGood":
            file_list=self.known_good_filetypes
        elif file_consensus=="KnownBad":
            file_list=self.known_bad_filetypes
        for x in range(0,len(file_list)):
            if file_list[x]==file_type:
                del(file_list[x])
                break
        
    def set_directory_to_scan(self,new_directory):
        self.directory_to_scan=new_directory
    def get_directory_to_scan(self):
        return self.directory_to_scan

    def save_info_to_file(self):
        self.known_good_file.delete_all_file_contents()
        self.known_bad_file.delete_all_file_contents()
        for item in self.known_good_filetypes:
            self.known_good_file.append_line_to_file(item)
        for item in self.known_bad_filetypes:
            self.known_bad_file.append_line_to_file(item)

    def close_all_files(self):
        self.known_good_file.close_file()
        self.known_bad_file.close_file()



def main():
    application_window=AppWindow()
    print("here")
    saved_information.save_info_to_file()
    saved_information.close_all_files()
saved_information=SavedInfo()
main()
