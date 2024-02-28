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

        self.root                   = root
        self.styler                 = Styler                (root)

        self.root.protocol          (   "WM_DELETE_WINDOW", self.quit   );
        self.root.geometry          (   "600x400"                       );
        self.root.minsize           (   400,200                         );
        # self.main_frame             = ttk.Fram (root)

        self.frame                  = VerticalScrolledFrame (root);


        # self.main_frame.pack        (   expand = True, fill = tk.BOTH )
        self.okbutton               = ttk.Button            (root,text="Save",command=self.ok_pressed)
        self.okbutton.pack          (   expand = False, fill = "x" );
        self.frame.pack             (   expand = True, fill = tk.BOTH );

        self.passed_file_item       = None
        self.passed_file_item_ref   = None
        self.passed_file_path       = None
        self.ctrl_c_timer           = None

        self.frame.bind             ('<<ScrollbarHasMouse>>'   ,self.handleScrollbarHovered)
        self.frame.bind             ('<<ScrollbarMouseless>>'  ,self.handleScrollbarHovered)
        self.root.bind              ("<<OkPressed>>"           ,self.ok_pressed)
        self.root.bind              ("<Configure>"             ,self.handleResize)
        self.root.bind              ("<Control-Button>"        ,self.handleZoom)
        self.root.bind              ("<Control-plus>"          ,self.zoom_in)
        self.root.bind              ("<Control-minus>"         ,self.zoom_out)
        self.root.bind              ("<Alt-Button>"            ,self.handleButtonScroll)
        self.root.bind              ("<Return>"                ,self.ok_pressed)
        # self.root.bind              ('<Configure>'         ,self._configure_interior)
        self.root.bind              ('<Control-Up>'            ,lambda e: self.frame._scroll_up())
        self.root.bind              ('<Control-Down>'          ,lambda e: self.frame._scroll_down())
        self.root.bind              ('<Alt-Up>'                ,lambda e: self.frame._scroll_up())
        self.root.bind              ('<Alt-Down>'              ,lambda e: self.frame._scroll_down())

    # def handleActiveFieldChanged(self,e=None):
    def handleScrollbarHovered(self,e=None):
        self.resize_is_safe = not self.resize_is_safe
    def handleResize(self,e):
        # print(e)
        self.frame._configure_canvas(e)
        self.frame._configure_interior(e)

    def handleZoom(self,e):
        if self.resize_is_safe:
            if e.num == 4 or e.num == 6:
                self.zoom_in()
            elif e.num == 5 or e.num == 7:
                self.zoom_out()
        return "break"


    def handleButtonScroll(self,e):
        if e.num == 4 or e.num == 6:
            self.frame._scroll_up()
        elif e.num == 5 or e.num == 7:
            self.frame._scroll_down()
        return "break"

    # def ok_pressed(self):
    #     self.event_generate('<<OkPressed>>')

    def update_fontsize(self,new_size1,new_size2):
        if self.zooming == True:
            self.root.update()
            # self.frame.canvas.unbind    ('<Configure>')
            # self.frame.interior.unbind  ('<Configure>')
            self.root.after             (60,lambda e1=new_size1,e2=new_size2:self.reset_zoom(e1,e2))

    def reset_zoom(self,e1,e2):

        for parent in self.frame.interior.winfo_children():

            for child in parent.winfo_children():

                for grandchild in child.winfo_children():

                    if isinstance(grandchild,ttk.Label):

                        if grandchild.tag == "s":
                            grandchild.configure(font=("",e1,"bold"))

                        elif grandchild.tag == "k":
                            grandchild.configure(font=("",e2))

                    elif isinstance(grandchild,TweakedEntry):
                        grandchild.configure(font=("",e2))

        # self.frame.canvas.bind      ('<Configure>',     self.frame._configure_canvas)
        # self.frame.interior.bind    ('<Configure>',     self.frame._configure_canvas)
        self.root.update            ()
        self.zooming = False

    def zoom_out(self,e=None): # has caused crashing
        if self.small_font_size > 9 and self.zooming == False:
            self.zooming = True
            self.big_font_size      -= 1
            self.small_font_size    -= 1

            self.update_fontsize    (   self.big_font_size,
                                        self.small_font_size );
        return "break"

    def zoom_in(self,e=None):
        if self.small_font_size < 13 and self.zooming == False:
            self.zooming = True
            self.big_font_size      += 1
            self.small_font_size    += 1
            self.update_fontsize    (   self.big_font_size,
                                        self.small_font_size );
        return "break"


        # self.root.event_generate('<<ZoomIn>>')


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
        if (self.passed_file_item_ref != self.passed_file_item) and "disabled" not in self.okbutton.state():

            did_save = False
            try: # https://docs.python.org/3/glossary.html#term-EAFP - like good god damned snakes
                conf                = configparser.RawConfigParser()
                conf.optionxform    = str
                for i,x in self.passed_file_item.items():
                    conf[i]         = x
                with open(self.passed_file_path, 'w+', encoding='utf8') as configfile:   # not sure about the encoding
                    conf.write      (configfile,space_around_delimiters=False)

            except Exception as e:

                error_msg               =   f"Error occured while saving file:\n{self.passed_file_path}\n\n{e}"
                print                   (   error_msg,  e   )
                messagebox.showerror    (   title="Desktop-file editor:",
                                            message=error_msg
                );
                self.root.destroy()
            else:
                did_save = True


            new_passed_file_item                            = {}

            for section in conf.sections():
                new_passed_file_item [section]              = {}

                for key, val in conf.items    (section):
                    new_passed_file_item [section][key]     = val

            self.passed_file_item                           = new_passed_file_item
            self.passed_file_item_ref                       = deepcopy(self.passed_file_item)
            self.check_save_enabled()
            if did_save and self.dialog == None:
                self.root.after(20,self.open_window)
            else:
                self.dialog.destroy()
                self.root.after(20,self.open_window)
                # result = messagebox.askquestion(title=f"Saved document", message=f"{basename(self.passed_file_path)} was saved\nDo you want to open the containing folder?\n\n{dirname(self.passed_file_path)}")
                #
                # if result == 'yes':
                #     args = ["xdg-open",dirname(self.passed_file_path)]
                #     subprocess_call(args, stderr=DEVNULL, stdout=DEVNULL)
        else:
            print(f"Not saving: {basename(self.passed_file_path)} is unchanged.")

        # print("ok_pressed finished")

# --- ### SAVE THE FILE ### ---------------------------------------------------------------------------- END


    # def return_pressed(self,e,key,section):
    def check_save_enabled(self):
        if self.passed_file_item_ref == self.passed_file_item:
            self.okbutton.configure(state="disabled")
        else:
            self.okbutton.configure(state="normal")

    def text_changed(self,e,key,section,neighbor):
        if self.startup == False:
            origin      = e.widget
            new_key     = origin.entry_text.get()
            key         = neighbor.get()

            # print(new_key)
            if self.passed_file_item[section][key] != new_key:
                self.passed_file_item[section][key] = new_key
                # print(key,":",self.passed_file_item[section][key])
            self.check_save_enabled()

    def text_changed_key(self,e,key,section,neighbor):
        if self.startup == False:
            origin      = e.widget
            new_key     = origin.entry_text.get()
            old_key     = key
            # print(key)
            try:
                # print(new_key)
                self.passed_file_item[section][new_key]
                if self.passed_file_item[section][new_key] != neighbor.get():
                    self.okbutton.configure(state="disabled")
                else:
                    self.okbutton.configure(state="enabled")
                # del t
            except KeyError:

                d = self.passed_file_item[section] # https://stackoverflow.com/a/59196714
                replacement = {old_key: new_key}

                # print(new_key)
                # print(self.passed_file_item[section])

                for k, v in list(d.items()):
                    d[replacement.get(k, k)] = d.pop(k)

                # print(d)
                # print(self.passed_file_item[section])

                origin.unbind('<<FieldChanged>>')
                origin.bind('<<FieldChanged>>', lambda e, key=new_key, section=section,neighbor=neighbor: \
                                                    self.text_changed_key(e,key,section,neighbor) );
                self.check_save_enabled()

    def buildUi(self):
        if self.passed_file_item != None:
            _row = 0
            subframe=ttk.Frame       (self.frame.interior)
            #
            for i,x in self.passed_file_item.items():
                # print(i,x)

                box                 =   ttk.Frame    (   subframe );
                top_label           =   ttk.Label    (   box, text=i, font=("",self.big_font_size,"bold") );
                top_label.tag       =   "s"
                top_label.grid      (   row=0,
                                        column=0, columnspan=2 );
                b_row = 1

                for a,b in x.items():
                    # print(a,"=",b)

                    # label               =   ttk.Label        (   box,text=a, anchor="w",font=("",self.small_font_size) );
                    label               =   TweakedEntry    (parent=box,root=self.root,font=("",self.small_font_size));
                    label.tag           =   "k"
                    label.grid          (   row=b_row,
                                            column=0,
                                            sticky="we" );

                    entry               =   TweakedEntry    (   parent=box,
                                                                root=self.root,
                                                                # key=a,
                                                                font=("",self.small_font_size)
                    );
                    # '<<ReturnPressed>>' is hmmmm...

                    entry.bind('<<FieldChanged>>', lambda e, key=a, section=i,neighbor=label: \
                                                    self.text_changed(e,key,section,neighbor)
                    );
                    entry.bind('<<ScrollUp>>', lambda e: self.frame._scroll_up()
                    );
                    entry.bind('<<ScrollDown>>', lambda e: self.frame._scroll_down()
                    );
                    entry.bind('<<ScrollToField>>', lambda e: self.frame._scroll_to_widget(e.widget)
                    );

                    label.bind('<<FieldChanged>>', lambda e, key=a, section=i, neighbor=entry: \
                                                    self.text_changed_key(e,key,section,neighbor)
                    );
                    label.bind('<<ScrollToField>>', lambda e: self.frame._scroll_to_widget(e.widget)
                    );
                    label.insert        (   0, a );
                    entry.insert        (   0, b );
                    entry.grid          (   row=b_row,
                                            column=1,
                                            padx=3,
                                            sticky="we" );
                    b_row += 1

                    # if a.lower() == "type" or a.lower() == "actions":
                    #     entry.configure(state="disabled",justify='center')
                    #     entry.bind('<Button>', lambda e: e.widget.focus_set()
                    #     );

                box.grid                    (   row=_row,
                                                column=0,
                                                sticky="we" );
                box.grid_columnconfigure    (   1, weight=1 );

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


#---- END CLASSES ---------------------------------------------------------------------------------

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


