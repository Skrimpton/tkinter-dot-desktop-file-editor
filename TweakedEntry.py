#!/bin/env python

import  re, sys, signal

# from os.path import isfile

import  tkinter     as      tk
from    tkinter     import  ttk
from    collections import  deque


class CEntry(ttk.Entry): # https://stackoverflow.com/a/75367456
    def __init__(self, parent=None, root=None, font=None, key=None,enabled=True, *args, **kwargs):

        ttk.Entry.__init__(self, parent, *args, **kwargs)
        self.key                    = key
        self.parent                 = parent
        self.root                   = root
        self.dir_select             = False
        self.undo_redo_reopen       = False
        self._undo_stack            = deque(maxlen=100)
        self._redo_stack            = deque(maxlen=100)
        # self.entry_text             = parent.entry_text
        self.changes                = [""]
        self.steps                  = int()
        self.keep_active_timer      = None


        self.entry_text         =   tk.StringVar    ( );
        if font == None:
            _font   = ("Arial",18)
        else:
            _font   = font
        if enabled:
            _state  = "enabled"
        else:
            _state  = "disabled"
        self.configure(
            font                = _font,
            text                = self.entry_text,
            state               = _state,
            # highlightbackground = ,
            # highlightcolor      = ,
            # disabledbackground  = ,
            # insertbackground    = ,
            # background          = ,
            # foreground          = ,
            # foreground          = ,
            # selectforeground    = ,
            # selectbackground    = ,
            # borderwidth         = ,
        );
        # self.element_options(self.context_menu)
        self.makeMenu()
        self.set_bindings()

    def makeMenu(self):
        self.context_menu = tk.Menu(self,
            tearoff=0,
            bg="#000000",
            fg="#ffffff",
            relief="flat",
            bd=6,
            font=('',11),
        );
        # print(self.context_menu.winfo_class())
        self.context_menu.add_command(label="Cut",command=lambda: self.event_generate("<<Cut>>"))
        self.context_menu.add_command(label="Copy",command=lambda: self.event_generate("<<Copy>>"))
        self.context_menu.add_command(label="Paste",command=lambda: self.event_generate("<<Paste>>"))
        self.context_menu.add_command(label="Delete",command=lambda: self.delete_selcted())
        self.context_menu.add_command(label="Select all",command=self._select_all_menu)
        self.context_menu.add_command(label="Clear",command=lambda: self.delete(0, tk.END))
        self.context_menu.add_command(label="Undo")
        self.context_menu.add_command(label="Redo")


    def set_bindings(self):
        self.bind("<FocusOut>",self.handlePopupClose)

        self.bind("<Button>", self.onMouse)

        self.bind("<Button-3>", self.popup)

        # self.bind("<Motion>",self.onWheel)
        self.bind   ('<<Paste>>',           self.paste)
        self.bind   ('<FocusOut>',          self.handleFocusOut)
        self.bind   ("<Return>",            self._return_pressed)
        self.bind   ("<Shift-Up>",          self._shift_up_down)
        self.bind   ("<Shift-Down>",        self._shift_up_down)
        self.bind   ("<Alt-Shift-slash>",   self.toggle_dir_select)
        self.bind   ("<Alt-Shift-R>",       self.toggle_undo_redo_reopen)
        self.bind   ("<Alt-Left>",          lambda e:self.scrollHandler(2))
        self.bind   ("<Alt-Right>",         lambda e:self.scrollHandler(1))
        self.bind   ("<Control-A>",         self._select_all)
        self.bind   ("<Control-a>",         self._select_all)

        self.bind   ("<Control-z>",         self.undo)
        self.bind   ("<Control-Z>",         self.undo)
        #
        self.bind   ("<Control-y>",         self.redo)
        self.bind   ("<Control-Y>",         self.redo)
        self.bind   ("<Control-Shift-z>",   self.redo)
        self.bind   ("<Control-Shift-Z>",   self.redo)

        self.trace_id = self.entry_text.trace("w", self.on_changes)
        self.bind   ('<Control-BackSpace>', self.entry_ctrl_bs)

    def toggle_undo_redo_reopen(self,e):
        self.undo_redo_reopen = not self.undo_redo_reopen

    def toggle_dir_select(self,e):

        self.event_generate('<<SelectModeChanged>>')
        print("select mode (dir):",self.dir_select)

        self.dir_select = not self.dir_select
        if self.select_present():
            self.select_range(0,0)

    def _return_pressed(self,e):
        self.event_generate('<<ReturnPressed>>')

    def handleFocusOut(self,e=None):
        self.select_range(0,0)
        self.context_menu.unpost()

    def handlePopupClose(self,e=None):
        self.context_menu.unpost()

    def _wordAtIndex(self,string,index):
        if self.dir_select == True:
            sp = string.split('/')
        else:
            sp = string.split(' ')
        total_len = 0
        for word in sp:
            total_len += (len(word) + 1)    #The '+1' accounts for the underscore
            if index < total_len:
                result = word
                break

        end_idx         = self.index(tk.INSERT)
        if self.dir_select == True:
            start_idx       = (self.get().rfind("/", None, end_idx)+1) # magic word-boundary finder <3
        else:
            start_idx       = (self.get().rfind(" ", None, end_idx)+1) # magic word-boundary finder <3
        _s              = start_idx
        _e = _s + len(result)
        # return (_s,_e,result)
        return (_s,_e)

    def _select_all(self,e):
        if self.select_present():
            if self.selection_get() == self.get():
                self.select_range(0,0)
            else:
                self.select_range(0,tk.END)

        else:
            # print("selecting all")
            self.after(10, lambda: self.select_range(0,tk.END))
            # self.select_range(0,tk.END)
        return "break"

    def _select_all_menu(self):
        self.after(10, lambda: self.select_range(0,tk.END))

    def _shift_up_down(self,e):
        index_pack = self._wordAtIndex(e.widget.get(),self.index(tk.INSERT))

        if self.select_present():
            if self.selection_get() == e.widget.get():
                self.select_range(index_pack[0],index_pack[1])
                # self.select_range(0,0)
            else:
                self.select_range(0,tk.END)

        else:
            self.select_range(index_pack[0],index_pack[1])
        return "break"

    def onMouse(self,e):
        self.handlePopupClose()
        # print(e.num,e.y)
        if e.num==5 or e.num ==6:
            self.scrollHandler(1)
            return "break"
        elif e.num==4 or e.num==7:
            self.scrollHandler(2)
            return "break"



    def scrollHandler(self,mode):
        if mode == 2:
            self.xview_scroll(-2, "units")
        else:
            self.xview_scroll(2, "units")
        return "break"

    def entry_ctrl_bs(self, event): # TODO Automatically adapt to contents separator (";" "/" and so forth)
        # print()
        if not self.select_present():
            end_idx         = self.index(tk.INSERT)
            start_idx       = (self.get().rfind(" ", None, end_idx)+1)
            if end_idx != start_idx:
                self.selection_range(start_idx, end_idx)
                if self.selection_get().startswith("\""):
                    self.selection_range(start_idx+1, end_idx)

    def paste(self,e):
        self.on_changes()


    def popup(self, event):
        self.focus_set()
        # self.context_menu.entryconfigure( "Paste", command=lambda: self.event_generate("<<Paste>>"),state="normal")

        if self.select_present():
            self.context_menu.entryconfigure("Cut", state="normal")
            self.context_menu.entryconfigure("Copy", state="normal")
            self.context_menu.entryconfigure("Delete", state="normal")
        else:
            self.context_menu.entryconfigure    ("Cut", state="disabled")
            self.context_menu.entryconfigure    ("Copy", state="disabled")
            self.context_menu.entryconfigure    ("Delete", state="disabled")
            self.context_menu.entryconfigure    ("Select all", state="disabled")

        if not self._undo_stack or len(self._undo_stack) == 1:
            self.context_menu.entryconfigure    ("Undo",state="disabled",   command=lambda e=event: self.undo_menu(e))
        else:
            self.context_menu.entryconfigure    ("Undo",state="normal",     command=lambda e=event: self.undo_menu(e))
        if not self._redo_stack:
            self.context_menu.entryconfigure    ("Redo",state="disabled",   command=lambda e=event: self.redo_menu(e))
        else:
            self.context_menu.entryconfigure    ("Redo",state="normal",     command=lambda e=event: self.redo_menu(e))

        if len(event.widget.get()) == 0:
            self.context_menu.entryconfigure    ("Clear",state="disabled")
        else:
            self.context_menu.entryconfigure    ("Clear",state="normal")

        if len(event.widget.get()) == 0 or (self.select_present() and self.selection_get() == event.widget.get()) :
            self.context_menu.entryconfigure    ("Select all",state="disabled")
        else:
            self.context_menu.entryconfigure    ("Select all",state="normal")



        self.context_menu.post(event.x_root, event.y_root)
        # self.context_menu.focus_set()
    #
    def delete_selcted(self):
        sel_start   = self.index("sel.first")
        sel_end     = self.index("sel.last")
        self.delete(sel_start, sel_end)


    # --------------------------------------------------------------------------
    #                                       https://stackoverflow.com/a/75367456

    def undo_menu(self, event=None):  # noqa
        self.undo()
        if self.undo_redo_reopen:
            self.after(100,
                lambda e=event: self.popup(e)
            )

    def redo_menu(self, event=None):  # noqa
        self.redo()
        if self.undo_redo_reopen:
            self.after(100,
                lambda e=event: self.popup(e)
            )

    def undo(self, event=None):  # noqa
        if len(self._undo_stack) <= 1:
            return "break"
        else:
            old_view =  self.xview()
            # print(old_view)
            old_index = self.index(tk.INSERT)
            if old_index < self.index(tk.END):
                reset_index = True
            else:
                reset_index = False
            content = self._undo_stack.pop()
            self._redo_stack.append(content)
            content = self._undo_stack[-1]
            self.entry_text.trace_vdelete("w", self.trace_id)
            self.delete(0, tk.END)
            self.insert(0, content)

            self.event_generate('<<FieldChanged>>')
            if reset_index == False:
                self.icursor(len(content))
                # self.xview_moveto(1.0)
            else:
                self.icursor(old_index)
            self.trace_id = self.entry_text.trace("w", self.on_changes)
            # self.see(tk.INSERT)
            if old_index == (len(self.get())+1):
                # if self.xview()[1] != 1.0:
                self.xview(100)
                # print("pop")
            else:
                self.xview_moveto(old_view[0])
            return "break"

    def redo(self, event=None):  # noqa
        if not self._redo_stack:
            return

        old_view =  self.xview()
        old_index = self.index(tk.INSERT)
        if old_index < self.index(tk.END):
            reset_index = True
        else:
            reset_index = False
        content = self._redo_stack.pop()
        self._undo_stack.append(content)
        self.entry_text.trace_vdelete("w", self.trace_id)
        self.delete(0, tk.END)
        self.insert(0, content)

        self.event_generate('<<FieldChanged>>')
        # self.icursor(len(content))
        self.trace_id = self.entry_text.trace("w", self.on_changes)
        if reset_index:
            self.icursor(old_index)
        if old_index == (len(self.get())-1):
            # if self.xview()[1] != 1.0:
            self.xview(100)
            # print("pop")
        else:
            self.xview_moveto(old_view[0])
        # self.xview_scroll(old_view[0])
        # self.see(tk.INSERT)
        return "break"


    def on_changes(self, a=None, b=None, c=None):  # noqa
        # Event.VirtualEventData = "poop"
        self.event_generate('<<FieldChanged>>')
        self._undo_stack.append(self.entry_text.get())
        self._redo_stack.clear()

    def reset_undo_stacks(self):
        self._undo_stack.clear()
        self._redo_stack.clear()
        self._undo_stack.append(self.entry_text.get())

