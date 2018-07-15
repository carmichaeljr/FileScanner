"""
            File(File,read,write,opps)          FileOpperations(object)
            -Contains the actual file            -contains gereral file 
            -Only has super calls in it      <---- opperations, such as copy,
             to the classes it inherits from       close, move, delete.
            /\                /\
            /                  \
           /                    \
ReadFile(object)              WriteFile(object)
-Contains advanced read     -Contains advanced write file
 file opperations,such as     opperations, such as write to a 
 character and specific       specific character,line.
 line reads.
"""

import os
import linecache
from shutil import copy

__name__="FileWrapper"

def print_all():
    print("FileWrapper classes and coresponding functions:")
    print("NOTE - this list only includes classes avialble for use")
    print("-File\n\t-change_file_mode(new_mode)\n\t-move_file(new_location)")
    print("\t-copy_file(new_location)\n\t-print_file_locations()")
    print("\t-delete_file()\n\t-close_file()")
    print("\t-append_line_to_file(line)\n\t-append_lines_to_file(lines)")
    print("\t-delete_all_file_contents()\n\t-read_line(line)")
    print("\t-read_lines(start,end)\n\t-read_character(line,character)")
    print("\t-print_file_contents(formating)")
    

class FileOpperations(object):
    def __init__(self):
        pass

    def set_file_path(self, file_location, file_name):
        if file_location=="":
            self.file_location=file_location
            self.file_name=file_name
            self.full_file_path=self.file_name
        else:
            self.file_location=file_location
            self.file_name=file_name
            self.full_file_path=self.file_location+"\\"+self.file_name
        
    def open_file_for_first_time(self):
        try:
            self.file=open(self.full_file_path,"r")
        except:
            self.file=open(self.full_file_path,"w")
            self.change_file_mode("r")

    def change_file_mode(self,new_mode):
        #Note - should i check to see if the file is already in the supplied mode?
        if (new_mode.upper()=="R" or new_mode.upper()=="RB" or new_mode.upper()=="R+" or\
           new_mode.upper()=="RB+" or new_mode.upper()=="W" or new_mode.upper()=="WB" or\
           new_mode.upper()=="W+" or new_mode.upper()=="WB+" or new_mode.upper()=="A" or\
           new_mode.upper()=="AB" or new_mode.upper()=="A+" or new_mode.upper()=="AB+"):
            self.file.close()
            self.file=open(self.full_file_path,new_mode)
            
    def move_file(self,new_location):
        self.copy_file(new_location)
        self.delete_file()
        self.set_file_path(new_location,self.file_name)
        self.change_file_mode("r")
        
    def copy_file(self,new_location):
        copy(self.full_file_path, new_location)
        self.file_locations.append(new_location+"\\"+self.file_name)

    def print_file_locations(self):
        counter=1
        print("Locations of File: {0}".format(self.file_name))
        for location in self.file_locations:
            print("   Location {0}: {1}".format(counter,location))
            counter+=1

    def delete_file(self):
        self.close_file()
        os.remove(self.full_file_path)
        for x in range(0,len(self.file_locations)-1):
            if self.file_locations[x]==self.full_file_path:
                del(self.file_locations[x])

    def close_file(self):
        self.file.close()
        

class ReadFile(object):
    def __init__(self):
        pass

    def read_line(self,line):
        return linecache.getline(self.full_file_path, line).rstrip()

    def read_lines(self,start,end):
        lines=[]
        line_counter=1
        for line in self.file:
            if line_counter>=start and (type(end).__name__=='str' and end.upper()=="END"):
                lines.append(line.rstrip())
            elif line_counter>=start and line_counter<=end:
                lines.append(line.rstrip())
            line_counter+=1
        return lines

    def read_character(self,line,character):
        return self.read_line(line)[character]

    def print_file_contents(self, formating):
        counter=1
        for line in self.file:
            if formating==True:
                print("{0}| {1}".format(counter,line.rstrip()))
                counter+=1
            else:
                print(line.rstrip())


class WriteFile(object):
    def __init__(self):
        pass

    def append_line(self,line):
        if line[len(line)-1]=="\n":
            self.file.write(line)
        else:
            self.file.write(line+"\n")

    def append_lines(self,lines):
        for item in lines:
            self.append_line(item)

    def delete_file_contents(self):
        self.file.seek(0)
        self.file.truncate(0)  


class File(FileOpperations,ReadFile,WriteFile):
    def __init__(self,file_location,file_name):
        self.file_location=file_location
        self.file_name=file_name
        self.full_file_path=""
        self.file_locations=[]
        super(File,self).set_file_path(self.file_location,self.file_name)
        super(File,self).open_file_for_first_time()

    def __str__(self):
        string="<File: {0:15s}| Encoding: {1:8s} Mode: {2:4s} Closed: {3:2b}>".format(\
             self.file.name, self.file.encoding, self.file.mode, self.file.closed)
        return string

    def change_file_mode(self,new_mode):
        super(File,self).change_file_mode(new_mode)
    def move_file(self,new_location):
        super(File,self).move_file(new_location)
    def copy_file(self,new_location):
        super(File,self).copy_file(new_location)
    def print_file_locations(self):
        super(File,self).print_file_locations()
    def delete_file(self):
        super(File,self).delete_file()
    def close_file(self):
        super(File,self).close_file()

    def append_line_to_file(self,line):
        super(File,self).change_file_mode("a")
        super(File, self).append_line(line)
    def append_lines_to_file(self,lines):
        super(File,self).change_file_mode("a")
        super(File,self).append_lines(lines)
    def delete_all_file_contents(self):
        super(File,self).change_file_mode("a")
        super(File,self).delete_file_contents()
        
    def read_line(self,line):
        super(File,self).change_file_mode("r")
        return super(File,self).read_line(line)
    def read_lines(self, start, end):
        super(File,self).change_file_mode("r")
        return super(File,self).read_lines(start,end)
    def read_character(self,line,character):
        super(File,self).change_file_mode("r")
        return super(File,self).read_character(line,character)
    def print_file_contents(self, formating):
        super(File,self).change_file_mode("r")
        super(File, self).print_file_contents(formating)
            
"""
print_all()
test_file=File("","Test file.txt")
print(test_file)
test_file.delete_all_file_contents()
test_file.append_line_to_file("Test line 1")
test_file.append_line_to_file("Test line 2\n")
test_file.append_line_to_file("Third line, I'm the boss.")
test_file.append_lines_to_file(["Line 4","Line 5","Line 6"])

test_file.print_file_contents(True)
lines1_2=test_file.read_lines(1,2)
line2=test_file.read_line(2)
print("Line 2: " +line2)
print(lines1_2)

test_file.move_file("H:\\Sensor Diagrams")

test_file.append_line_to_file("Line 7")

test_file.print_file_contents(True)
lines6_7=test_file.read_lines(6,7)
character=test_file.read_character(6,5)
print(lines6_7)
print("Line 6, Character 5: "+character)

test_file.copy_file("H:\\Python Documents")
test_file.delete_file()
test_file.close_file()
print(test_file)
test_file.print_file_locations()
"""
