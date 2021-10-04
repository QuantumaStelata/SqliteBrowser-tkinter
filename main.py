import tkinter
from tkinter import filedialog

import sqlite3

import settings as st


class Root(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.guiSettings()
        self.setHotKeys()

        self.command_frame = tkinter.Frame(self)
        self.command_frame.pack(fill='x')
        
        self.connect_button = tkinter.Button(self.command_frame, text='Connect', relief=st.RELIEF, command=self.fileOpen)
        self.connect_button.pack(padx=(20, 5), pady=(3,3), side='left')

        self.run_button = tkinter.Button(self.command_frame, text='Run', relief=st.RELIEF, command=self.runSql)
        self.run_button.pack(padx=(5, 5), pady=(3,3), side='left')

        self.exit_button = tkinter.Button(self.command_frame, text='Exit', relief=st.RELIEF, command=lambda: self.destroy())
        self.exit_button.pack(padx=(5, 20), pady=(3,3), side='right')

        self.input_frame = tkinter.Frame(self)
        self.input_frame.pack(fill='both', expand=True)
    
        self.input_sql = tkinter.Text(self.input_frame, relief=st.RELIEF, width=0, height=0, font=st.FONT)
        self.input_sql.pack(fill='both', expand=True, padx=(20, 20), pady=(3,3), ipady=100)

        self.output_frame = tkinter.Label(self, relief=st.RELIEF, bg='#FFF', anchor='nw')
        self.output_frame.pack(fill='both', expand=True, side='bottom', padx=(20, 20), pady=(3,5)) #TODO
    
    def guiSettings(self, *args, **kwargs):
        self.geometry(f"{st.WIDTH}x{st.HEIGHT}+{(self.winfo_screenwidth() - st.WIDTH) // 2}+{(self.winfo_screenheight() - st.HEIGHT) // 2}")
        self.minsize(*st.MIN_SIZE)
        self.maxsize(*st.MAX_SIZE)
        self.resizable(*st.ROOT_RESIZABLE)
        self.title(st.ROOT_TITLE)


    def setHotKeys(self, *args, **kwargs):
        self.bind("<Control-f>", self.fileOpen)
        self.bind("<F5>", self.runSql)


    def fileOpen(self, *args, **kwargs):
        # for i in self.__dict__:
        #     try:
        #         getattr(self, i).config(bg='#282828')
        #     except:
        #         pass
        
        dlg = filedialog.Open(self, filetypes = st.FILE_TYPES)
        st.DB_NAME = dlg.show()


    def runSql(self, *args, **kwargs):
        request = self.input_sql.get(0.0, 'end')

        if request.isspace():
            self.delOutputFrameChild()
            response = tkinter.Label(self.output_frame, text='Request is empty', font=st.FONT, bg='#FFF')
            response.grid(column=0, row=0)
            return

        response, response_col = self.conn(request)
        print(response, response_col)
        if response is None and response_col is None:
            return

        self.delOutputFrameChild()
        
        if response_col:    
            for column, i in enumerate(response_col):
                res = tkinter.Label(self.output_frame, text=str(i[0]), font=st.FONT, bg='#FFF')
                res.grid(column=column, row=0)

        if response:
            for row, i in enumerate(response, 1):
                for column, j in enumerate(i, 0):
                    res = tkinter.Label(self.output_frame, text=str(j), font=st.FONT, bg='#FFF')
                    res.grid(column=column, row=row) 

        if response == [] and not response_col:
            res = tkinter.Label(self.output_frame, text='OK', font=st.FONT, bg='#FFF')
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
            error = tkinter.Label(self.output_frame, text=exp, font=st.FONT, bg='#FFF', fg='#F00')
            error.grid(column=0, row=0)
            response = None
            response_col = None

        self.cursor.close()
        return response, response_col

    def delOutputFrameChild(self):
        for child in self.output_frame.winfo_children():
            child.destroy()
        

root = Root()
root.mainloop()
