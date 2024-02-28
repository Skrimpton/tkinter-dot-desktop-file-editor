import tkinter as tk
from tkinter import ttk

from os.path import (   isfile,
                        dirname,
                        basename,
                        realpath
)
from os import      (   access,
                        W_OK
)

from subprocess     import (    call as subprocess_call,
                                DEVNULL
)
from TweakedEntry   import CEntry as TweakedEntry
class QuestionDialog(tk.Toplevel):

    def __init__(self, parent=None, saved_file=None , root=None, text="",  *args, **kwargs):

        self.saved_file = saved_file

        super().__init__(parent)
        self.geometry('360x80')
        self.title(f"Saved {basename(self.saved_file)}")


        self.yes        = ttk.Button        (   self,
                                            text='Yes',
                                            command=self.open_dir,
        );
        self.no         = ttk.Button        (   self,
                                            text='No',
                                            command=self.destroy,
        );
        self.question   = ttk.Label         (   self,
                                            text=f"Open containing directory?",
                                            font=("",12),
        );
        self.info       = TweakedEntry      (   self,
                                            enabled=False,
                                            font=("",10),
        );
        self.info.entry_text.set(f"{dirname(self.saved_file)}")

        self.question.bind('<Configure>', lambda e: self.question.config(wraplength=self.info.winfo_width()))

        self.question.pack  (expand=0,   side="top",    fill="both", anchor="n")
        self.info.pack      (expand=0,   side="top",    fill="x",    anchor="n")
        self.yes.pack       (expand=1,   side="left",   fill="x",    anchor="s")
        self.no.pack        (expand=1,   side="right",  fill="x",    anchor="s")
        self.no.focus_set()

    def open_dir(self):
        _dir = dirname(self.saved_file)
        args = ["xdg-open",_dir]
        try:
            subprocess_call(args, stderr=DEVNULL, stdout=DEVNULL)
        except:
            print(f"xdg-open {_dir} failed")
        self.destroy()
