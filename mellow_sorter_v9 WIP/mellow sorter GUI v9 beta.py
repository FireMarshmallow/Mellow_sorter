import csv
import datetime
import os
import sys
import threading
import time
import tkinter as tk
from shutil import copy2
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import pickle

root = Tk()
root.title("Me//0W sorter v9.1.0 beta")
path = "."

# selector for the inport folder


def folder1():
    global folder_selected1
    folder_selected1 = filedialog.askdirectory()

# selector for the output folder


def folder2():
    global folder_selected2
    folder_selected2 = filedialog.askdirectory()

# funcshon for saving paths

#save############


def save_file_path():
    PathAndName = os.path.join(sys.path[0], "mellow_sorter_save.dat")
    return PathAndName


def Save(folder_selected1, folder_selected2):
    thing_to_save_for_next_time = [
        folder_selected1,
        folder_selected2,
    ]
    outfile = open(save_file_path(), "wb")
    pickle.dump(thing_to_save_for_next_time, outfile)
    outfile.close()


def open_save():
    try:
        infile = open(save_file_path(), "rb")
        new_dict = pickle.load(infile)
        infile.close()
        global folder_selected2
        global folder_selected1
        folder_selected1 = new_dict[0]
        folder_selected2 = new_dict[1]
        changeText1()
        changeText2()
    except:
        pass

##############


def Run():
    path = folder_selected1
    for subdir, dirs, files in os.walk(path):
        path = folder_selected1
        if '.DS_Store' in files:
            files.remove('.DS_Store')
        for file in files:
            progress['maximum'] = len(files)
            try:
                this = os.path.join(subdir, file)
                modificationTime = time.strftime(
                    '%d', time.localtime(os.path.getmtime(this)))
                modificationTime1 = time.strftime(
                    '%m', time.localtime(os.path.getmtime(this)))
                modificationTime2 = time.strftime(
                    '%Y', time.localtime(os.path.getmtime(this)))
            except:
                print('Cant find date')
            os.chdir(folder_selected2)
            dayFolder = modificationTime+' - '+modificationTime1+' - '+modificationTime2
            if not os.path.exists(modificationTime2):
                os.makedirs(modificationTime2)
            os.chdir(folder_selected2+'/'+modificationTime2)
            months_nom = ['00-IgotLazy', '01 - January', '02 - February', '03 - March', '04 - April', '05 - May',
                          '06 - June', '07 - July', '08 - August', '09 - September', '10 - October', '11 - November', '12 - December']
            if not os.path.exists(months_nom[int(modificationTime1)]):
                os.makedirs((months_nom[int(modificationTime1)]))
            os.chdir(folder_selected2+'/'+modificationTime2 +
                     '/'+months_nom[int(modificationTime1)])
            if not os.path.exists(dayFolder):
                os.makedirs(dayFolder)
            os.chdir(folder_selected2+'/'+modificationTime2 +
                     '/'+months_nom[int(modificationTime1)])
            if not os.path.exists(file):
                try:
                    move(this, dayFolder)
                    print(file, 'moved')
                except:
                    print('cant move', file)
            else:
                print(file, 'exists')
            progress.step()
            root.update()
        print('Done')


def Undo():
    def doit():
        for subdir, dirs, files in os.walk(folder_selected2):
            os.chdir(subdir)
            for file in files:
                try:
                    copy2(file, folder_selected1)
                except:
                    print('nope')
        kill()

    def kill():
        top.destroy()

    top = Toplevel()
    top.title("Undo")
    warning = Label(top, text='!WARNING!').grid(row=0, column=1)
    undoworning = Label(
        top, text='This will put all the files into').grid(row=1, column=1)
    woringfolder = Label(top, text=folder_selected1).grid(row=2, column=1)
    nosub = Label(top, text='With NO sub folders').grid(row=3, column=1)
    undoconfarm = Button(top, text='continue',
                         command=doit).grid(row=4, column=1)
    button = Button(top, text="Dismiss", command=kill).grid(row=5, column=1)


def changeText1():
    Button1['text'] = folder_selected1


def changeText2():
    Button2['text'] = folder_selected2


def sd():
    top1 = Toplevel()
    top1.title("SD offloder V1.0")

    def Stopreview():
        camera.stop_preview()
        print('preview stoped')

    def switchon():
        global switch
        switch = True
        print('scaning Started')
        starttimelaps()

    def switchoff():
        print('scaning Stoped')
        global switch
        switch = False

    def kill():
        top1.destroy()

    def starttimelaps():
        def Run():
            while (switch == True):
                def path_to_drive():
                    list = [
                        "/Volumes/WinInstall/tow",
                    ]  # SD card From canon
                    return list

                # cherk if drives are connected

                def if_connected():
                    # gets path from list
                    for path in path_to_drive():
                        # checks if the drive is conected
                        if os.path.exists(path) == True:
                            # tells the offlode def drive is conected
                            offlode_card(path)
                            # passes the path

                # move files off sd card

                def offlode_card(sd):
                    # path to the directore to move files to
                    move_to = "/Volumes/WinInstall/one"
                    # walks the directory
                    for dirName, subdirList, fileList in os.walk(sd, topdown=False):
                        for fname in fileList:
                            # comdins to path with the file name
                            pathtofile = dirName + "/" + fname
                            # trys to move the fils or skips it
                            try:
                                print("moving: " + fname)
                                move(pathtofile, move_to)
                            except:
                                pass
                print("scaning")
                if_connected()
                time.sleep(6)

        thread = threading.Thread(target=Run)
        thread.start()

    onbutton = tk.Button(top1, height=3, width=15,
                         text="Start Scaning", command=switchon)
    offbutton = tk.Button(top1, height=3, width=15,
                          text="Stop scaning", command=switchoff)
    killbutton = tk.Button(top1, height=3, width=15,
                           text="EXIT", command=lambda: [kill(), switchoff()])

    onbutton.grid(row=11, column=0)
    offbutton.grid(row=11, column=2)

    killbutton.grid(row=12, column=1)


Button6 = tk.Button(root, text="sd", activeforeground="blue",
                    height=5, width=20, command=lambda: [sd()])

Button0 = tk.Button(root, text="Save", activeforeground="blue",
                    height=5, width=20, command=lambda: [Save(folder_selected1, folder_selected2)])
progress = Progressbar(root, orient=HORIZONTAL, length=450, mode='determinate')
Button1 = tk.Button(root, text="Select input folder", activeforeground="blue",
                    height=5, width=50, command=lambda: [folder1(), changeText1()])
Button2 = tk.Button(root, text="Select output folder", activeforeground="blue",
                    height=5, width=50, command=lambda: [folder2(), changeText2()])
Button3 = tk.Button(root, text="Run Me//0W sorter",
                    activeforeground="green", height=5, width=50, command=Run)
Button4 = tk.Button(root, text="UNDO",
                    activeforeground="red", height=5, width=20, command=Undo)

Button6.grid(columnspan=1, column=1, row=7)
Button0.grid(columnspan=1, column=1, row=6)  # save button
Button1.grid(columnspan=3, column=1, row=2)  # inout
Button2.grid(columnspan=3, column=1, row=3)  # output
Button3.grid(columnspan=3, column=1, row=4)  # run
Button4.grid(columnspan=1, column=2, row=6)  # undo
progress.grid(columnspan=3, column=1, row=5)  # progras bar

open_save()
root.mainloop()
