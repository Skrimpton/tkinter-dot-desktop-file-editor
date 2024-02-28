#!/bin/env python3

import sys,argparse,configparser,signal

from subprocess     import (    call as subprocess_call,
                                DEVNULL
)
# from subprocess import DEVNULL

try:
    import tkinter as tk
    from tkinter import ttk,messagebox

except:
    print("no tkinter, no joy"),sys.exit(1)
else:
    from TweakedEntry   import CEntry as TweakedEntry
    from Dialog         import QuestionDialog
    from VScrollFrame   import VerticalScrolledFrame
    from Styler         import Styler

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

python_version_major = sys.version_info[0]
python_version_minor = sys.version_info[1]

if python_version_major < 3:
    print("Need python 3.6 or greater")
    sys.exit(1)
elif python_version_major >= 3 and python_version_minor < 6:
    print("Need python 3.6 or greater")
    sys.exit(1)

#---- BEGIN CLASSES ---------------------------------------------------------------------------------

class Window():

    signal.signal(
        signal.SIGINT,
        keyboard_interrupt_handler
    );

    def __init__(self, root, *args, **kwargs):
        self.startup                = True
        self.dialog                 = None
        self.active_field           = None
        self.zooming                = False
        self.resize_is_safe         = True
        self.big_font_size          = 10
        self.small_font_size        = 9
        self.ctrl_c_timer           = None

        self.root                   = root
        self.styler                 = Styler                (root)

        self.root.protocol          (   "WM_DELETE_WINDOW", self.quit   );
        self.root.geometry          (   "600x400"                       );
        self.root.minsize           (   400,200                         );
        # self.main_frame             = ttk.Fram (root)


        # self.main_frame.pack        (   expand = True, fill = tk.BOTH )
        self.okbutton               = ttk.Button            (root,text="Save",command=self.ok_pressed)
        self.okbutton.pack          (   expand = False, fill = "x" );


    def quit(self):

        if self.ctrl_c_timer != None:

            self.root.after_cancel      (self.ctrl_c_timer)
            self.ctrl_c_timer           = None

        self.root.destroy               ()

    def open_window(self):
        self.dialog     =   QuestionDialog  (   self.root,
                                                saved_file = self.passed_file_path
        );
        # print("open_window func finished")

# --- ### SAVE THE FILE ### -------------------------------------------------------------------------- BEGIN

    def ok_pressed(self,event=None):
        if self.passed_file_item_ref != self.passed_file_item:
           print("diff")
        # print("ok_pressed finished")

# --- ### SAVE THE FILE ### ---------------------------------------------------------------------------- END


    # def return_pressed(self,e,key,section):
    def check_save_enabled(self):
        if self.passed_file_item_ref == self.passed_file_item:
            self.okbutton.configure(state="disabled")
        else:
            self.okbutton.configure(state="normal")
    #
    # def text_changed(self,e,key,section,neighbor):
    #     if self.startup == False:
    #         origin      = e.widget
    #         new_key     = origin.entry_text.get()
    #         key         = neighbor.get()
    #
    #         # print(new_key)
    #         if self.passed_file_item[section][key] != new_key:
    #             self.passed_file_item[section][key] = new_key
    #             # print(key,":",self.passed_file_item[section][key])
    #         self.check_save_enabled()

    # def text_changed_key(self,e,key,section,neighbor):
    #     if self.startup == False:
    #         origin      = e.widget
    #         new_key     = origin.entry_text.get()
    #         old_key     = key
    #         # print(key)
    #         try:
    #             # print(new_key)
    #             self.passed_file_item[section][new_key]
    #             if self.passed_file_item[section][new_key] != neighbor.get():
    #                 self.okbutton.configure(state="disabled")
    #             else:
    #                 self.okbutton.configure(state="enabled")
    #             # del t
    #         except KeyError:
    #
    #             d = self.passed_file_item[section] # https://stackoverflow.com/a/59196714
    #             replacement = {old_key: new_key}
    #
    #             # print(new_key)
    #             # print(self.passed_file_item[section])
    #
    #             for k, v in list(d.items()):
    #                 d[replacement.get(k, k)] = d.pop(k)
    #
    #             # print(d)
    #             # print(self.passed_file_item[section])
    #
    #             origin.unbind('<<FieldChanged>>')
    #             origin.bind('<<FieldChanged>>', lambda e, key=new_key, section=section,neighbor=neighbor: \
    #                                                 self.text_changed_key(e,key,section,neighbor) );
    #             self.check_save_enabled()

    def buildUi(self):
        if self.passed_file_item != None:
            _row = 0
            subframe=tk.Frame       (self.root)
            #
            for i,x in self.passed_file_item.items():
                print(i)

                # box                 =   ttk.Frame    (   subframe );
                # top_label           =   ttk.Label    (   box, text=i, font=("",self.big_font_size,"bold") );
                # top_label.tag       =   "s"
                # top_label.grid      (   row=0,
                #                         column=0, columnspan=2 );
                # b_row = 1

                for a,b in x.items():
                    print(a,"=",b)

                _row += 1

            subframe.grid_columnconfigure   (   0,
                                                weight=1 );
            subframe.pack                   (   fill='both',
                                                expand=1 );
            self.subframe = subframe

        else:
            print("something is very wrong. sorry")
            self.root.destroy()

        self.passed_file_item_ref   = deepcopy(self.passed_file_item)
        self.startup                = False
        self.check_save_enabled     ()
        self.root.title             (f"Editing: {self.passed_file_path}")
        self.toggleCtrlCTimer       ()



    # --- BEGIN INFINTE LOOP ---------------------------------------------------------------------------------
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

    # --- END INFINTE LOOP -----------------------------------------------------------------------------------


#---- BEGIN ARGS PARSING AND START MAINLOOP ---------------------------------------------------------------------------------


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
    try:
        config.read(passed_file)
    except configparser.Error as config_error:
        print(config_error)
        sys.exit(1)
    except Exception as exception_error:
        print(exception_error)
        sys.exit(1)


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



if __name__ == "__main__":

    root = tk.Tk()

    window = Window(root)
    window.passed_file_item = passed_file_item
    window.passed_file_path = passed_file
    window.buildUi()

    root.mainloop()

#---- END OF FILE ----


