#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import sqlite3
import sys

import settings as st


class Root(tk.Tk):
    def __init__(self):
        super().__init__()
        self.guiSettings()
        self.setHotKeys()
        self.changeTheme()

        self.managerWindow('MAIN')
        
    
    def managerWindow(self, on, *args, **kwargs):
        '''Window manager. Destroy all windows and run widnow with name in argument <on>'''            
        if on == 'MAIN':
            self.destroyWindow()
            self.mainFrame()
        elif on == 'DATA':
            if st.DB_NAME != '':
                self.destroyWindow()
                self.dataFrame()
            else:
                tk.messagebox.showerror(title='Error', message='Database not connected')
        else:
            raise Exception(f'Window not Found. List windows: {st.WINDOWS}')
        
        self.changeThemeWidget(self.winfo_children())


    def mainFrame(self, *args, **kwargs):
        '''Run Main Frame. Set Child Frames'''
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill='both', expand=True)
        
        self.mainCommandFrame()
        self.mainInputFrame()
        self.mainOutputFrame()
        

    def guiSettings(self, *args, **kwargs):
        '''Set gui settings from setings.py'''
        self.geometry(f"{st.WIDTH}x{st.HEIGHT}+{(self.winfo_screenwidth() - st.WIDTH) // 2}+{(self.winfo_screenheight() - st.HEIGHT) // 2}")
        self.minsize(*st.MIN_SIZE)
        self.maxsize(*st.MAX_SIZE)
        self.resizable(*st.ROOT_RESIZABLE)
        self.title(st.ROOT_TITLE)

        if (sys.platform.startswith('win')): 
            self.iconbitmap('/static/db.ico')


    def setHotKeys(self, *args, **kwargs):
        '''Set Hot Keys for main window'''
        self.bind("<Control-f>", self.fileOpen)
        self.bind("<Control-F>", self.fileOpen) # if caps is on
        self.bind("<F5>", self.runSql)
        self.bind("<Control-Key-a>", self.selectAll)
        self.bind("<Control-Key-A>", self.selectAll) # if caps is on
        self.bind("<<ComboboxSelected>>", self.dataOutputResponse)
        self.protocol("WM_DELETE_WINDOW", self.exit) # Call when exit


    def mainCommandFrame(self, *args, **kwargs):
        '''Run Command Frame. Set Child Buttons'''
        self.command_frame = tk.Frame(self.main_frame)
        self.command_frame.pack(fill='x')
        
        self.connect_button = tk.Button(self.command_frame, text='Connect', command=self.fileOpen)
        self.connect_button.pack(padx=(20, 5), pady=(3,3), side='left')

        self.run_button = tk.Button(self.command_frame, text='Run', command=self.runSql)
        self.run_button.pack(padx=(5, 5), pady=(3,3), side='left')

        self.create_db_button = tk.Button(self.command_frame, text='Create DB', command=self.createDB)
        self.create_db_button.pack(padx=(5, 5), pady=(3,3), side='left')

        self.data_button = tk.Button(self.command_frame, text='Data', command=lambda: self.managerWindow('DATA'))
        self.data_button.pack(padx=(5, 5), pady=(3,3), side='left')

        self.exit_button = tk.Button(self.command_frame, text='Exit', command=self.exit)
        self.exit_button.pack(padx=(5, 20), pady=(3,3), side='right')

        self.theme_button = tk.Button(self.command_frame, command=self.changeTheme, name='!theme')
        self.theme_button.pack(padx=(5, 5), pady=(3,3), side='right')


    def mainInputFrame(self, *args, **kwargs):
        '''Run Input Frame. Set Text widget for input sql commands'''
        self.input_frame = tk.Frame(self.main_frame)
        self.input_frame.pack(fill='both', expand=True)
    
        self.input_sql = tk.Text(self.input_frame, width=0, height=0)
        self.input_sql.pack(fill='both', expand=True, padx=(20, 20), pady=(3,3), ipady=100)


    def mainOutputFrame(self, *args, **kwargs):
        '''Run Output Frame. Set Label widget for output sql response'''
        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(fill='both', expand=True)

        self.output_label = tk.Text(self.output_frame)#, anchor='nw')
        self.output_label.pack(fill='both', expand=True, side='bottom', padx=(20, 20), pady=(3,10))


    def fileOpen(self, *args, **kwargs): 
        '''The dialog window for found and connect to database'''     
        dlg = filedialog.Open(self, filetypes = st.FILE_TYPES)
        _dir = dlg.show()
        
        if not st.DB_NAME:
            st.DB_NAME = _dir


    def runSql(self, *args, **kwargs):
        '''Method for run sql command'''
        request = self.input_sql.get(0.0, 'end')

        if request.isspace():
            self.delOutputFrameChild()
            response = tk.Label(self.output_label, text='Request is empty', font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
            response.grid(column=0, row=0)
            return

        response, response_col = self.conn(request)
        
        if response is None and response_col is None:
            return

        self.delOutputFrameChild()
        
        if response_col:    
            for column, i in enumerate(response_col):
                res = tk.Label(self.output_label, text=str(i[0]), font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
                res.grid(column=column, row=0)

        if response:
            for row, i in enumerate(response, 1):
                for column, j in enumerate(i, 0):
                    res = tk.Label(self.output_label, text=str(j), font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
                    res.grid(column=column, row=row) 

        if response == [] and not response_col:
            res = tk.Label(self.output_label, text='OK', font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
            res.grid(column=0, row=0)

        
    def conn(self, request, *args, **kwargs):
        '''Method for connect to database, send request and return response to runSql method'''
        if not st.DB_NAME:
            tk.messagebox.showerror(title='Error', message='Database not connected')
            return None, None

        self.cursor = sqlite3.connect(st.DB_NAME, isolation_level=None).cursor()

        try:
            self.cursor.execute(request)
            response = self.cursor.fetchall()
            response_col = self.cursor.description
            
        except Exception as exp:
            self.delOutputFrameChild()
            error = tk.Label(self.output_label, text=exp, font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['ERROR'], name='!error')
            error.grid(column=0, row=0)
            response = None
            response_col = None

        self.cursor.close()
        return response, response_col


    def delOutputFrameChild(self, *args, **kwargs):
        '''Clean Output Frame'''
        for child in self.output_label.winfo_children():
            child.destroy()
               

    def changeTheme(self, *args, **kwargs):
        '''Сhanges theme from light to dark and vice versa. Run changeThemeWidget method'''
        if not getattr(self, 'combostyle_l', False):
            self.combostyle_l = ttk.Style()
            self.combostyle_l.theme_create('combostyle_l', parent='alt', settings = st.THEME_LIGHT['COMBOBOX']['SETTINGS'])
            self.combostyle_l.configure("Alt.TCombobox", font=50)

        if not getattr(self, 'combostyle_d', False):
            self.combostyle_d = ttk.Style()
            self.combostyle_d.theme_create('combostyle_d', parent='alt', settings = st.THEME_DARK['COMBOBOX']['SETTINGS'])

        
        if st.NOW_LIGHT_THEME:
            self.THEME = st.THEME_LIGHT
            st.NOW_LIGHT_THEME = False
            self.combostyle_l.theme_use('combostyle_l')
        else:
            self.THEME = st.THEME_DARK
            st.NOW_LIGHT_THEME = True
            self.combostyle_d.theme_use('combostyle_d')
        
        self.changeThemeWidget(self.winfo_children())

    
    def changeThemeWidget(self, frame, *args, **kwargs):
        '''Sets theme to all widgets. Get theme from changeTheme method'''
        self.configure(bg=self.THEME['FRAME'])

        
        self.option_add("*TCombobox*Listbox*Background", self.THEME['COMBOBOX']['BACKGROUND'])
        self.option_add("*TCombobox*Listbox*Foreground", self.THEME['COMBOBOX']['FOREGROUND'])
        self.option_add("*TCombobox*Listbox*Font", st.FONT)
        self.option_add('*TCombobox*Listbox*selectBackground', self.THEME['COMBOBOX']['SBACKGROUND'])
        self.option_add('*TCombobox*Listbox*selectForeground', self.THEME['COMBOBOX']['SFOREGROUND'])

        if hasattr(self, 'tables_box'):
            if self.tables_box._tclCommands != None:
                self.tables_box.config(font=st.FONT)


        for child in frame:
            if isinstance(child, tk.Frame):
                child.configure(bg=self.THEME['FRAME'])
            if isinstance(child, tk.Button):
                child.configure(bg=self.THEME['BUTTON'], fg=self.THEME['FG'], relief=st.RELIEF, activebackground=self.THEME['ACTIVE'], highlightbackground=self.THEME['BORDER'])
            if isinstance(child, tk.Text):
                child.configure(bg=self.THEME['TEXT'], fg=self.THEME['FG'], relief=st.RELIEF, font=st.FONT, highlightbackground=self.THEME['FRAME'])
            if isinstance(child, tk.Label):
                child.configure(bg=self.THEME['LABEL'], fg=self.THEME['FG'], relief=st.RELIEF)
            if child.winfo_name() == '!error':
                child.configure(bg=self.THEME['LABEL'], fg=self.THEME['ERROR'], relief=st.RELIEF)
            if child.winfo_name() == '!theme':
                child.configure(text=self.THEME['THEME'])
            if child.winfo_children():
                self.changeThemeWidget(child.winfo_children())


    def selectAll(self, *args, **kwargs):
        '''Method for Hot Key <CTRL+A>'''
        self.input_sql.tag_add('sel', "1.0", 'end')
        self.input_sql.mark_set('insert', "1.0")
        self.input_sql.see('insert')


    def createDB(self, *args, **kwargs):
        '''Method for create database in this directory'''
        st.DB_NAME = 'base.db'
        self.cursor = sqlite3.connect(st.DB_NAME, isolation_level=None).cursor()
        self.cursor.close()
        self.delOutputFrameChild()
        res = tk.Label(self.output_label, text='Created base.db', font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
        res.grid(column=0, row=0)


    def dataFrame(self, *args, **kwargs):
        '''Run Data Frame and set child widgets'''
        self.data_frame = tk.Frame(self)
        self.data_frame.pack(fill='both', expand=True)

        self.dataCommandFrame()
        self.dataOutputFrame()

    def dataCommandFrame(self, *args, **kwargs):
        self.command_frame = tk.Frame(self.data_frame)
        self.command_frame.pack(fill='x')

        self.data_button = tk.Button(self.command_frame, text='< Back', command=lambda: self.managerWindow('MAIN'))
        self.data_button.pack(padx=(20, 5), pady=(3,3), side='left')

        self.exit_button = tk.Button(self.command_frame, text='Exit', command=lambda: self.destroy())
        self.exit_button.pack(padx=(5, 20), pady=(3,3), side='right')

        self.theme_button = tk.Button(self.command_frame, command=self.changeTheme, name='!theme')
        self.theme_button.pack(padx=(5, 5), pady=(3,3), side='right')

    def dataOutputFrame(self, *args, **kwargs):
        response, _ = self.conn('SELECT name FROM sqlite_master;')

        self.tables_box = ttk.Combobox(self.data_frame, values=response, state="readonly", font=st.FONT)
        self.tables_box.pack(fill='x', expand=False,  padx=(20, 20), pady=(3,3))
        self.tables_box.current(0)
        
        # frame = tk.Frame(self.data_frame)
        # frame.pack(fill='both', expand=True, side='bottom', padx=(20, 20), pady=(3,10))

        # scrollbar = tk.Scrollbar(frame)
        # scrollbar.pack(side='right', fill='y')

        self.output_label = tk.Text(self.data_frame)#, yscrollcommand=scrollbar.set)#, anchor='nw')
        self.output_label.pack(fill='both', expand=True, side='bottom', padx=(20, 20), pady=(3,10))
        # scrollbar.config(command=self.output_label.yview)
 

        self.dataOutputResponse()

    def dataOutputResponse(self, *args, **kwargs):
        self.delOutputFrameChild()
        table_name = self.tables_box.get()

        response, response_col = self.conn(f'SELECT * from {table_name};')
           
        for column, i in enumerate(response_col):
            res = tk.Label(self.output_label, text=str(i[0]), font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
            res.grid(column=column, row=0)

        
        for row, i in enumerate(response, 1):
            for column, j in enumerate(i, 0):
                res = tk.Label(self.output_label, text=str(j), font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
                res.grid(column=column, row=row) 
    

    def destroyWindow(self, *args, **kwargs):
        '''Destroy window and her child'''
        for child in self.winfo_children():          
            child.destroy()

    def exit(self, *args, **kwargs):
        close = tk.messagebox.askyesno(title='Close', message='Are you sure you want to close?')
        if close:
            self.destroy()

        

root = Root()
root.mainloop()
