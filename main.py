import tkinter
from tkinter import filedialog

import sqlite3

import settings as st


class Root(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.guiSettings()
        self.setCommandFrame()
        self.setInputFrame()
        self.setOutputFrame()
        self.setHotKeys()
        self.changeTheme()

    def guiSettings(self, *args, **kwargs):
        self.geometry(f"{st.WIDTH}x{st.HEIGHT}+{(self.winfo_screenwidth() - st.WIDTH) // 2}+{(self.winfo_screenheight() - st.HEIGHT) // 2}")
        self.minsize(*st.MIN_SIZE)
        self.maxsize(*st.MAX_SIZE)
        self.resizable(*st.ROOT_RESIZABLE)
        self.title(st.ROOT_TITLE)


    def setHotKeys(self, *args, **kwargs):
        self.bind("<Control-f>", self.fileOpen)
        self.bind("<Control-F>", self.fileOpen) # if caps is on
        self.bind("<F5>", self.runSql)
        self.bind("<Control-Key-a>", self.selectAll)
        self.bind("<Control-Key-A>", self.selectAll) # if caps is on


    def setCommandFrame(self, *args, **kwargs):
        self.command_frame = tkinter.Frame(self)
        self.command_frame.pack(fill='x')
        
        self.connect_button = tkinter.Button(self.command_frame, text='Connect', command=self.fileOpen)
        self.connect_button.pack(padx=(20, 5), pady=(3,3), side='left')

        self.run_button = tkinter.Button(self.command_frame, text='Run', command=self.runSql)
        self.run_button.pack(padx=(5, 5), pady=(3,3), side='left')

        self.exit_button = tkinter.Button(self.command_frame, text='Exit', command=lambda: self.destroy())
        self.exit_button.pack(padx=(5, 20), pady=(3,3), side='right')

        self.theme_button = tkinter.Button(self.command_frame, text='Dark theme', command=self.changeTheme)
        self.theme_button.pack(padx=(5, 5), pady=(3,3), side='right')

    def setInputFrame(self, *args, **kwargs):
        self.input_frame = tkinter.Frame(self)
        self.input_frame.pack(fill='both', expand=True)
    
        self.input_sql = tkinter.Text(self.input_frame, width=0, height=0)
        self.input_sql.pack(fill='both', expand=True, padx=(20, 20), pady=(3,3), ipady=100)

    def setOutputFrame(self, *args, **kwargs):
        self.output_frame = tkinter.Frame(self)
        self.output_frame.pack(fill='both', expand=True)

        self.output_label = tkinter.Label(self.output_frame, anchor='nw')
        self.output_label.pack(fill='both', expand=True, side='bottom', padx=(20, 20), pady=(3,5))

    def fileOpen(self, *args, **kwargs):      
        dlg = filedialog.Open(self, filetypes = st.FILE_TYPES)
        st.DB_NAME = dlg.show()


    def runSql(self, *args, **kwargs):
        request = self.input_sql.get(0.0, 'end')

        if request.isspace():
            self.delOutputFrameChild()
            response = tkinter.Label(self.output_label, text='Request is empty', font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
            response.grid(column=0, row=0)
            return

        response, response_col = self.conn(request)
        
        if response is None and response_col is None:
            return

        self.delOutputFrameChild()
        
        if response_col:    
            for column, i in enumerate(response_col):
                res = tkinter.Label(self.output_label, text=str(i[0]), font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
                res.grid(column=column, row=0)

        if response:
            for row, i in enumerate(response, 1):
                for column, j in enumerate(i, 0):
                    res = tkinter.Label(self.output_label, text=str(j), font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
                    res.grid(column=column, row=row) 

        if response == [] and not response_col:
            res = tkinter.Label(self.output_label, text='OK', font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['FG'])
            res.grid(column=0, row=0)

        

    def conn(self, request, *args, **kwargs):
        if not st.DB_NAME:
            tkinter.messagebox.showerror(title='Error', message='Database not connected')
            return None, None

        self.cursor = sqlite3.connect(st.DB_NAME, isolation_level=None).cursor()

        try:
            self.cursor.execute(request)
            response = self.cursor.fetchall()
            response_col = self.cursor.description
            
        except Exception as exp:
            self.delOutputFrameChild()
            error = tkinter.Label(self.output_label, text=exp, font=st.FONT, bg=self.THEME['LABEL'], fg=self.THEME['ERROR'], name='!error')
            error.grid(column=0, row=0)
            response = None
            response_col = None

        self.cursor.close()
        return response, response_col

    def delOutputFrameChild(self, *args, **kwargs):
        for child in self.output_label.winfo_children():
            child.destroy()
               

    def changeTheme(self, *args, **kwargs):
        if st.NOW_LIGHT_THEME:
            self.THEME = st.THEME_LIGHT
            st.NOW_LIGHT_THEME = False
            self.theme_button.configure(text='Dark theme')
        else:
            self.THEME = st.THEME_DARK
            st.NOW_LIGHT_THEME = True
            self.theme_button.configure(text='Light theme')
        
        self.changeThemeWidget(self.winfo_children())

    
    def changeThemeWidget(self, list_child, *args, **kwargs):
        for child in list_child:
            if isinstance(child, tkinter.Frame):
                child.configure(bg=self.THEME['FRAME'])
            if isinstance(child, tkinter.Button):
                child.configure(bg=self.THEME['BUTTON'], fg=self.THEME['FG'], relief=st.RELIEF, activebackground=self.THEME['ACTIVE'], highlightbackground=self.THEME['BORDER'])
            if isinstance(child, tkinter.Text):
                child.configure(bg=self.THEME['TEXT'], fg=self.THEME['FG'], relief=st.RELIEF, font=st.FONT, highlightbackground=self.THEME['FRAME'])
            if isinstance(child, tkinter.Label):
                child.configure(bg=self.THEME['LABEL'], fg=self.THEME['FG'], relief=st.RELIEF)
            if child.winfo_name() == '!error':
                child.configure(bg=self.THEME['LABEL'], fg=self.THEME['ERROR'], relief=st.RELIEF)
            if child.winfo_children():
                self.changeThemeWidget(child.winfo_children())

    def selectAll(self, *args, **kwargs):
        self.input_sql.tag_add('sel', "1.0", 'end')
        self.input_sql.mark_set('insert', "1.0")
        self.input_sql.see('insert')

        

root = Root()
root.mainloop()
