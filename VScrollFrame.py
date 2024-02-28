import tkinter as tk
from tkinter import ttk
from tkinter.constants import *
class VerticalScrolledFrame(ttk.Frame): # https://coderslegacy.com/python/make-scrollable-frame-in-tkinter/

    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)
        # self.counter = 0
        # self.okbutton = ttk.Button(self,text="Save",command=self.ok_pressed)
        # self.okbutton.grid(row=0,column=0,columnspan=2,sticky="we",pady=1,padx=1)
        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.grid(row=0,column=1,sticky="ns")
        # vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, bg="#555555",
                                width = 200, height = 300,
                                yscrollcommand=self.handleScroll)
        self.canvas.grid(row=0,column=0,sticky="nswe")
        # self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command = self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior       = ttk.Frame(self.canvas)


        self.interior.bind  ('<Configure>',     self._configure_interior)
        self.canvas.bind    ('<Configure>',     self._configure_canvas)

        self.interior_id = self.canvas.create_window(   0, 0,
                                                        window=self.interior, anchor=NW );
        self.vscrollbar = vscrollbar
        self.vscrollbar.bind ('<Enter>',        lambda e: self.event_generate('<<ScrollbarHasMouse>>'))
        self.vscrollbar.bind ('<Leave>',        lambda e: self.event_generate('<<ScrollbarMouseless>>'))
        # self.vscrollbar.bind('<Button>',self.scrollbar_pressed)

    def _scroll_to_widget(self, widget):
        if self.interior.winfo_reqheight() > self.canvas.winfo_height():
            pos     = widget.winfo_rooty() - self.interior.winfo_rooty()
            height  = self.interior.winfo_reqheight()

            self.canvas.yview_moveto(pos / height)

    def handleScroll(self,e1,e2):
        # print(e1," : ",e2)
        # print(self.canvas.yview())
        # print(self.canvas.yview())
        # print(self.interior.yview())
        self.vscrollbar.set(e1,e2)
    # def scrollbar_pressed(self,e):
    #
    #     if e.num == 4 or e.num == 6:
    #         self._scroll_up()
    #         return "break"
    #
    #     elif e.num == 5 or e.num == 7:
    #         self._scroll_down()
    #         return "break"


    def _configure_interior(self, event):
        # self.counter += 1
        # print("------------------")
        # print("interior.winfo_reqheight" ,self.interior.winfo_reqheight())
        # print("interior.winfo_height"    ,self.interior.winfo_height())
        # print("self.winfo_height"        ,self.winfo_height())
        # print("canvas.winfo_height"      ,self.canvas.winfo_height())
        # print("",self.)

        if self.interior.winfo_reqheight() >= self.winfo_height():
            height = self.interior.winfo_reqheight()
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        else:
            # print(f"...{self.counter}...")
            height = self.winfo_height()
            size = (self.winfo_width(), self.winfo_height())

        ## Update the scrollregion.
        # print(self.canvas.bbox("all"))
        # print("final height",height)
        # print(size)
        self.canvas.config( scrollregion=(  0, 0,
                                          size[0], size[1] ));
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            self.canvas.config(width = self.interior.winfo_reqwidth())

        # if self.interior.winfo_reqheight() != self.canvas.winfo_height():
            # self.canvas.config(height = self.interior.winfo_reqheight())

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
