import sqlite3
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import datetime
from datetime import datetime, timedelta
import os
import shutil

databaseName = 'last_check.sqlite'
#make table
def datetime_tbl():
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS datetime_tbl(datestamp TEXT)');
    c.close()
    conn.close()
#grab entry from ui
def data_entry():
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    c.execute("INSERT INTO datetime_tbl (datestamp) VALUES (?)", (str(datetime.now()),))
    conn.commit()
    conn.close()

#this grabs file transfer from tbl for entry form              
def generatelasttransfer():
    conn = sqlite3.connect(databaseName)
    c = conn.cursor()
    global transfer
    transfer = c.execute("""SELECT MAX(datestamp) FROM datetime_tbl ORDER BY datestamp DESC LIMIT 1""").fetchall() 
    #print(transfer)#testing 
    return(transfer)
    c.close()
    #conn.close()    
    
def ui(root):
    #transfer = str()
    transfer = StringVar()
    transfer.set(generatelasttransfer())
    src_filename = str()
    des_filename = str()
    #btn for main file transfer 
    btn_ck = tk.Button(text='File Transfer',command= f_transfer).grid(row = 3, column = 2, padx = 5, pady = 5)
    #btns for src and des files
    btn_src = tk.Button(text='Choose file to send out',command= src_files).grid(row = 2, column = 2, padx = 5, pady = 5)
    btn_des = tk.Button(text='Choose file to send to',command= des_files).grid(row = 2, column = 4, padx = 5, pady = 5)
    # btn for generatelasttransfer
    #btn_func = tk.Button(text='Last Transfer',command= generatelasttransfer).grid(row = 3, column = 4, padx = 3, pady = 3)
    
    e = tk.Entry(root, textvariable = transfer, width=28)
    e.grid(row = 7, column = 7, padx = 7, pady = 7)
        
def src_files():
    global src_filename
    src_filename =  filedialog.askdirectory()
def des_files():
    global des_filename
    des_filename =  filedialog.askdirectory()
#file transfer
def f_transfer():
    data_entry()
    for root,dirs,files in os.walk(src_filename):
        for file_name in files:
            now = datetime.now()
            before = now - timedelta(hours=24)
            files = os.path.join(src_filename, file_name)
            mod_time = datetime.fromtimestamp(os.path.getmtime(files))
            if mod_time > before:
                shutil.move(os.path.join(src_filename, file_name), des_filename)

if __name__ == '__main__':
    datetime_tbl()
    data_entry()
    root = Tk()
    root.mainloop
    ui(root)
    

