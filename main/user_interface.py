import tkinter as tk
import pathlib
import tkinter.ttk as ttk
import tkinter.font

class TrainingApp(tk.Tk):

    def create_frames(self):
        self.frames = {}
        F = StartPage
        page_name = F.__name__
        frame = F(parent=self.container, controller=self)

        self.frames[page_name] = frame

        #Put all the canvases in the same location in the container
        frame.grid(row=0, column=0, sticky='nsew')
        
        '''
        for F in (StartPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)

            self.frames[page_name] = frame

            #Put all the canvases in the same location in the container
            frame.grid(row=0, column=0, sticky='nsew')
        '''


    def __init__(self, *args, **kwargs):
        # initialise tkinter window
        tk.Tk.__init__(self, *args, **kwargs)
        self.tkRoot = self
        self.tkRoot.title("Training App")
        self.start_width = 900
        self.start_height = 450
        self.minsize(width=self.start_width, height= self.start_height)

        # all the canvases will be placed on the container frame. The one we want visible will be raised on top of the others
        self.container = tk.Frame(self)
        self.container.pack(side='top', fill='both', expand=True)
        self.container.pack_propagate(0)
        self.container.grid_rowconfigure(0,weight=1)
        self.container.grid_columnconfigure(0,weight=1)

        # this path is used for program data (in a different folder)
        path = pathlib.Path(__file__).parent.resolve()
        data_path = "/".join(str(path).split('\\')[:-1]) + "/data"


        # initialising a range of colours and fonts which are used throughout the programs
        self.backgroundColor = "#E7E7E7"
        self.backgroundColorStandOut = "#9E9E9E"
        self.buttonBackground = '#9E9E9E'
        self.headerBackgroundColor = "#848383"
        self.buttonClick = "#B9B7B7"
        self.textForeground = "#000000"

        self.h1 = tkinter.font.Font(family="Helvlevtica",size=19)
        self.h2 = tkinter.font.Font(family="Helvlevtica",size=16)
        self.p1 = tkinter.font.Font(family="Helvlevtica",size=14)
        self.p2 = tkinter.font.Font(family="Helvlevtica",size=11)
        self.p3 = tkinter.font.Font(family="Helvlevtica",size=12)


        self.create_frames()
        self.show_frame("StartPage")


        # creating a menu bar which appears at the top of the screen
        self.main_menu = tk.Menu(self, background=self.buttonBackground)
        #creating the menu items
        self.file_menu = tk.Menu(self.main_menu, tearoff=False)
        self.actions_menu = tk.Menu(self.main_menu, tearoff=False)
        #cascades are the primary menu selectors (a dropdown box appears after clicking a cascade)
        self.main_menu.add_cascade(label='File', menu=self.file_menu)
        self.main_menu.add_cascade(label='Actions', menu=self.actions_menu)
        #the options that appear in a dropdown box after clicking a cascade
        self.file_menu.add_command(label="New...")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command = self.destroy)
        self.actions_menu.add_command(label="Home", command=lambda: self.show_frame("StartMenu"))

        self.config(menu=self.main_menu)


        def on_scroll(event):
            self.current_frame_object.scrollable_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.bind_all("<MouseWheel>", on_scroll)
    
    
    '''
    Show a canvas for the given page name
    '''
    def show_frame(self, page_name):
        self.current_frame = page_name
        frame = self.frames[page_name]
        frame.set_heading()
        self.current_frame_object = frame
        frame.tkraise()


'''
Creates a scrollable frame within a canvas
'''
class CreateScrollableFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.parent.grid_rowconfigure(0,weight=1)
        self.parent.grid_columnconfigure(0,weight=1)
        self.parent.grid_columnconfigure(1,weight=1)
        self.parent.scrollable_canvas = tk.Canvas(parent, background=self.controller.backgroundColor, bd=0, highlightthickness=0)
        self.parent.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.parent.scrollable_canvas.yview)
        self.parent.scrollable_frame = tk.Frame(parent, background=self.controller.backgroundColor)
        self.parent.bind("<Configure>", lambda e: parent.scrollable_canvas.configure(scrollregion = parent.scrollable_canvas.bbox("all")))
        self.parent.scrollable_canvas.create_window((0,0), window=self.parent.scrollable_frame, anchor='nw')
        self.parent.scrollable_canvas.configure(yscrollcommand=self.parent.scrollbar.set)
        self.parent.scrollable_canvas.pack(side="left", fill="both", expand=True)
        self.parent.scrollbar.pack(side="right", fill="y")



class StartPage(tk.Frame):
    def set_heading(self):
        self.controller.tkRoot.title("Training App > Home")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        frame_obj = CreateScrollableFrame(self, self.controller)
        frame = self.scrollable_frame

        title = tk.Label(frame, text="Training Aoo", bg=self.controller.backgroundColor, fg='black', font=controller.h1)
        title.grid(row=0,column=0, padx=50, pady=(30,0))

        title = tk.Label(frame, text="Please select a process below to continue:",fg='black', bg=self.controller.backgroundColor, font=controller.p2)
        title.grid(row=1,column=0, padx=50, pady=20)

        placeholder_button_1 = tk.Button(frame, text='PLACEHOLDER',borderwidth=0,width=15, height=1,font=self.controller.p3, fg="#ffffff", bg=self.controller.buttonBackground,activebackground=self.controller.buttonClick,activeforeground="#ffffff", relief=tk.FLAT)
        placeholder_button_1.grid(row=2,column=0, padx=50, pady=(0,15))

        placeholder_button_2 = tk.Button(frame, text='PLACEHOLDER',borderwidth=0,width=15, height=1,font=self.controller.p3, fg="#ffffff", bg=self.controller.buttonBackground,activebackground=self.controller.buttonClick,activeforeground="#ffffff", relief=tk.FLAT)
        placeholder_button_2.grid(row=3,column=0, padx=50, pady=15)


if __name__ == '__main__':
    trainingApp = TrainingApp()
    trainingApp.mainloop()