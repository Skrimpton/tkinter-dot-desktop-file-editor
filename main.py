#!/bin/env python3

import sys,argparse,configparser,signal

try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter.constants import *
except:
    print("no tkinter, no joy"),sys.exit(1)
else:
    from TweakedEntry import CEntry as TweakedEntry

from copy import        deepcopy

from os.path import (   isfile,
                        dirname,
                        basename,
                        realpath
)
from os import      (   access,
                        W_OK
)



def keyboard_interrupt_handler(sig, frame):
    print(":: WINDOW :: You pressed Ctrl+C! Exiting...")
    if __name__ == "__main__":
        window.quit()
    else:
        MainWindow().quit()

    sys.exit(0)

passed_file         = ""
passed_file_item    = {}

parser              = argparse.ArgumentParser(description='Desktop file editor')

parser.add_argument (
    '-f',
    '-file',
    '--file',
    dest='desktop_file',
    type=str,
    help='The file to edit'
);

args, unknown = parser.parse_known_args()

if len(unknown) > 0:
    args_file = unknown[0]
    if isfile(args_file) and args_file.endswith(".desktop"):
        passed_file = args_file

elif args.desktop_file != None:
        args_file = args.desktop_file
        if isfile(args_file) and args_file.endswith(".desktop"):
            passed_file = args_file



if passed_file != "" and passed_file.endswith(".desktop"):
    _dir = dirname(realpath(passed_file))

    if access(_dir, W_OK) == False:
        print(f"Can't write to {_dir}"),sys.exit(1)
    # config = configparser.ConfigParser()
    config = configparser.RawConfigParser()
    config.optionxform = str
    config.read(passed_file)

    passed_file_item = {}
    if len(config.sections()) == 0:
        print(f"There are no sections to edit in {basename(passed_file)}"),sys.exit(1)
    else:
        for section in config.sections():           # https://stackoverflow.com/a/23944270

            passed_file_item[section]                = {}

            for key, val in config.items    (section):

                passed_file_item[section][key]       = val

else:
    print("Need a .desktop-file to edit"),sys.exit(1)



class VerticalScrolledFrame(ttk.Frame): # https://coderslegacy.com/python/make-scrollable-frame-in-tkinter/

    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.grid(row=0,column=1,sticky="ns")
        # vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                width = 200, height = 300,
                                yscrollcommand=vscrollbar.set)
        self.canvas.grid(row=0,column=0,sticky="nswe")
        # self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command = self.canvas.yview)
        self.okbutton = ttk.Button(self,text="Save",command=self.ok_pressed)
        self.okbutton.grid(row=1,column=0,columnspan=2,sticky="we",pady=1,padx=1)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior       = ttk.Frame(self.canvas)

        self.interior.bind  ('<Configure>',   self._configure_interior)
        self.canvas.bind    ('<Configure>',     self._configure_canvas)

        self.interior_id = self.canvas.create_window(   0, 0,
                                                        window=self.interior, anchor=NW );
        self.vscrollbar = vscrollbar
        # self.vscrollbar.bind('<Button>',self.scrollbar_pressed)

    # def scrollbar_pressed(self,e):
    #
    #     if e.num == 4 or e.num == 6:
    #         self._scroll_up()
    #         return "break"
    #
    #     elif e.num == 5 or e.num == 7:
    #         self._scroll_down()
    #         return "break"

    def ok_pressed(self):
        self.event_generate('<<OkPressed>>')

    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config( scrollregion=(  0, 0,
                                            size[0], size[1] ));
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id,
                                      width=self.canvas.winfo_width());

    def _scroll_up(self):
        self.canvas.yview_scroll(-1,'units')
        # self.vscrollbar.scroll(-1,'units')

    def _scroll_down(self):
        self.canvas.yview_scroll(1,'units')
        # self.vscrollbar.scroll(1,'units')


class Window():

    signal.signal(
        signal.SIGINT,
        keyboard_interrupt_handler
    );

    def __init__(self, root, *args, **kwargs):
        self.root           = root
        self.root.protocol  ( "WM_DELETE_WINDOW", self.quit );
        self.root.geometry  ("600x400")
        self.root.minsize   (400,200)


        self.startup        = True
        self.frame          = VerticalScrolledFrame (   root );
        self.desktop_boxes  = []
        self.frame.pack     (   expand = True, fill = tk.BOTH );

        self.passed_file_item       = None
        self.passed_file_item_ref   = None
        self.passed_file_path       = None
        self.ctrl_c_timer           = None

        self.frame.bind("<<OkPressed>>",self.ok_pressed)
        self.root.bind("<Control-plus>",self.zoom_in)
        self.root.bind("<Return>",self.ok_pressed)

    def zoom_in(self,e):
        print("zooming1")
        self.root.event_generate('<<ZoomIn>>')

    def quit(self):

        if self.ctrl_c_timer != None:
            self.root.after_cancel          (self.ctrl_c_timer)
            self.ctrl_c_timer               = None
        self.root.destroy                   ()

    def ok_pressed(self,event=None):
        if self.passed_file_item_ref != self.passed_file_item:
            try: # https://docs.python.org/3/glossary.html#term-EAFP - like good god damned snakes
                conf = configparser.RawConfigParser()
                conf.optionxform = str
                for i,x in self.passed_file_item.items():
                    conf[i]=x
                with open(self.passed_file_path, 'w+', encoding='utf8') as configfile:   # not sure about the encoding
                    conf.write(configfile,space_around_delimiters=False)

            except Exception as e:

                error_msg = f"Error occured while saving file:\n{self.passed_file_path}\n\n{e}"
                print(error_msg,e)
                tk.messagebox.showerror(title="Desktop-file editor:",
                                        message=error_msg)
                self.root.destroy()

            new_passed_file_item = {}

            for section in conf.sections():
                new_passed_file_item [section]                = {}

                for key, val in conf.items    (section):
                    new_passed_file_item [section][key]       = val

            self.passed_file_item = new_passed_file_item
            self.passed_file_item_ref = deepcopy(self.passed_file_item)
            self.check_save_enabled()



    def buildUi(self):
        if self.passed_file_item != None:
            _row = 0
            subframe=tk.Frame       (self.frame.interior)
            #
            for i,x in self.passed_file_item.items():
                # print(i,x)

                box                 =   tk.Frame    (   subframe );
                top_label           =   tk.Label    (   box, text=i, font=("",10) );
                top_label.grid      (   row=0,
                                        column=0, columnspan=2 );
                b_row = 1

                for a,b in x.items():
                    # print(a,"=",b)
                    label               =   tk.Label        (   box,text=a, anchor="w",font=("",10) );
                    label.bind('<<ZoomIn>>',lambda e:print("zooming"))

                    label.grid          (   row=b_row,
                                            column=0,
                                            sticky="we" );

                    entry               =   TweakedEntry    (   parent=box,
                                                                root=self.root,
                                                                # key=a,
                                                                font=("",10)
                    );
                    # '<<ReturnPressed>>' is hmmmm...
                    entry.bind('<<FieldChanged>>', lambda e, key=a, section=i: \
                                                    self.text_changed(e,key,section)
                    );
                    entry.insert        (   0, b );

                    entry.grid          (   row=b_row,
                                            column=1,
                                            padx=3,
                                            sticky="we" );
                    b_row += 1

                box.grid                    (   row=_row,
                                                column=0,
                                                sticky="we" );
                box.grid_columnconfigure    (   1, weight=1 );

                _row += 1

            subframe.grid_columnconfigure   (   0,
                                                weight=1 );
            subframe.pack                   (   fill=BOTH,
                                                expand=1 );
            self.subframe = subframe

        else:
            self.root.destroy()

        self.passed_file_item_ref = deepcopy(self.passed_file_item)
        self.startup = False
        self.check_save_enabled()
        self.root.title(f"Editing: {self.passed_file_path}")
        self.toggleCtrlCTimer()


    # def return_pressed(self,e,key,section):
    def check_save_enabled(self):
        if self.passed_file_item_ref == self.passed_file_item:
            self.frame.okbutton.configure(state="disabled")
        else:
            self.frame.okbutton.configure(state="normal")

    def text_changed(self,e,key,section):
        if self.startup == False:
            origin      = e.widget
            new_value                       = origin.entry_text.get()

            # print(new_value)
            if self.passed_file_item[section][key] != new_value:
                self.passed_file_item[section][key] = new_value
                # print(key,":",self.passed_file_item[section][key])
            self.check_save_enabled()



    # --- ### INFINTE LOOP ### ---------------------------------------------------------------------------------
    # DECLARE AND START THE TIMER THAT LETS <CTRL+C> IN THE TERMINAL CLOSE THE WINDOW
    #
    def startCtrlCTimer(self): # <⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅               START <CTRL+C>-TIMER

        self.ctrl_c_timer = self.root.after (
            80,self.startCtrlCTimer
        );


    def toggleCtrlCTimer(self): # <⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅⋅       TOGGLE <CTRL+C>-TIMER ON/OFF
        if self.ctrl_c_timer is None:
            self.startCtrlCTimer            ()

        else:
            self.root.after_cancel          (self.ctrl_c_timer)
            self.ctrl_c_timer               = None

    # --- END INFINTE LOOP END ---------------------------------------------------------------------------------


if __name__ == "__main__":

    root = tk.Tk()

    window = Window(root)
    window.passed_file_item = passed_file_item
    window.passed_file_path = passed_file
    window.buildUi()

    root.mainloop()
