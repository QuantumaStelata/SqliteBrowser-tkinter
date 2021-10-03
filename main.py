import tkinter
from tkinter import filedialog
import threading
import time
import sqlite3
from tkinter.constants import W

import settings as st


class Root(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.guiSettings()
        self.setHotKeys()

        self.cursor = sqlite3.connect(st.DB_NAME).cursor()
        
        command_frame = tkinter.Frame(self, height=50)
        command_frame.pack(fill='x')
        
        connect_button = tkinter.Button(command_frame, text='Connect', relief=st.RELIEF, command=self.fileOpen)
        connect_button.pack(padx=(20, 5), pady=(3,3), side='left')

        run_button = tkinter.Button(command_frame, text='Run', relief=st.RELIEF)
        run_button.pack(padx=(5, 5), pady=(3,3), side='left')

        exit_button = tkinter.Button(command_frame, text='Exit', relief=st.RELIEF, command=lambda: self.destroy())
        exit_button.pack(padx=(5, 20), pady=(3,3), side='right')

        input_frame = tkinter.Frame(self)
        input_frame.pack(fill='both', expand=True)
    
        input_sql = tkinter.Text(input_frame, relief=st.RELIEF, width=0, height=0, font='Arial 16')
        input_sql.pack(fill='both', expand=True, padx=(20, 20), pady=(3,3))

        output_frame = tkinter.Frame(self, bg='#00F', height=225)
        output_frame.pack(fill='x', side='bottom')
    
    def guiSettings(self):
        self.geometry(f"{st.WIDTH}x{st.HEIGHT}+{(self.winfo_screenwidth() - st.WIDTH) // 2}+{(self.winfo_screenheight() - st.HEIGHT) // 2}")
        self.minsize(*st.MIN_SIZE)
        self.maxsize(*st.MAX_SIZE)
        self.resizable(*st.ROOT_RESIZABLE)
        self.title(st.ROOT_TITLE)


    def setHotKeys(self):
        self.bind("<Control-f>", self.fileOpen)


    def fileOpen(self, *args, **kwargs):
        dlg = filedialog.Open(self, filetypes = st.FILE_TYPES)
        st.DB_NAME = dlg.show()

        

root = Root()
root.mainloop()
