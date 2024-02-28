import tkinter as tk
from tkinter import ttk


C000                    = "#000000"
C101                    = "#101010"
C181                    = "#181818"
C222                    = "#222222"
C333                    = "#333333"
C444                    = "#444444"
Cba8                    = "#ba8404"
Cffa                    = "#ffaa00" # yellowish orange
Cfff                    = "#ffffff"
Cff1c                   = "#ffff1c" # bright yellow, more pale/white
Cff00                   = "#ffff00" # bright yellow, least pale/white
C55f                    = "#55ff7f" # bright/pale green
C313                    = "#313100" # poop
C391                    = "#391d00" # also poop, but different
C4c3                    = "#4c3401" # also poop, but a darker roast
C6f4                    = "#6f4e02" # too-much-fiber diarrhoea, and you had 2 glasses of milk
C4c4                    = "#4c4c00" # too-much-fiber diarrhoea, but only 1 glass
C2e1                    = "#2e1581" # blue
C002                    = "#002839" # dark greenish-blue / blueish-green
C013                    = "#01392d" # green that isn't trying too hard and is a little bit depressed
C3f4                    = "#3f452a" # GREENISH BROWNISH

BLACK                   = C000
ENTRY_FOCUSED           = Cffa
ENTRY_UNFOCUSED         = Cfff
CANVAS_COLOR            = C333

class Styler:

    def __init__(self, root):
        self.root = root

        self.style=ttk.Style(self.root)
        self.style.theme_use            ("alt")
        # self.style.theme_use            ("clam")
        # self.style.theme_use            ("classic")
        # self.style.theme_create("user_theme", parent="clam")
        self.stylegroup_frames  = []
        self.stylegroup_buttons = []
        self.stylegroup_entries = []
        self.stylegroup_labels  = []
        # self.style.theme_use("user_theme")

        # self.style.theme_use          ("clam")                            # use "clam"-theme
        # self.style.theme_use          ("classic")                         # use "classic"-theme
        # self.style.theme_use          ("vista")                           # use "vista"-theme (not available on linux)
        self.become_stylish             ()

    def become_stylish(self):
        self.style.layout(      "TEntry",
            [
                (   'Entry.plain.field', {
                        'children':
                        [(  'Entry.background', {'children':
                            [(  'Entry.padding', {'children': [( 'Entry.textarea', {'sticky': 'nswe'} )], 'sticky': 'nswe'} )],
                            'sticky': 'nswe'}
                        )],
                        'border':'1', 'sticky': 'nswe'
                    }
                )
            ]
        );

        self.style.map('Vertical.TScrollbar',
            foreground      = [ ('disabled', BLACK),
                                ('pressed', BLACK),
                                ('active', BLACK)
            ],
            background      = [ ('disabled', C222),
                                ('pressed', '!focus', Cba8),
                                ('active', C6f4),
                                ('!active', C333)
            ],
            bordercolor     = [ ('active', BLACK),
                                ('!active', BLACK)
            ],
            troughcolor     = [ ('!active', BLACK),
                                ('active', C101)
            ],
            highlightcolor  = [ ('focus', C181),
                                ('!focus', C6f4)
            ],
            relief          = [ ('pressed', 'flat'),
                                ('!pressed', 'flat')
            ],
            arrowcolor      = [ ('active', C6f4),
                                ('!active', Cffa)
            ],
        );

        self.style.configure("Vertical.TScrollbar" ,
            width               = 8,
            arrowsize           = 9,
            borderwidth         = 0,
            highlightthickness  = 0,
            arrowcolor          = C000,
            relief              = "flat",

        );
        self.style.map(         'TEntry',

            foreground          = [ ('disabled',C000),('!focus',"#ffefd8"), ('focus',"#ffefd8")    ],
            background          = [ ('disabled',"#aaaaaa"),('!focus',CANVAS_COLOR), ('focus',BLACK)    ],
            bordercolor         = [ ('disabled',C444),('focus',BLACK), ('!focus',CANVAS_COLOR)    ],
            insertcolor         = [ ('focus',Cfff),('!focus',Cff1c)    ],
            fieldbackground     = [ ('disabled',"#888888"),('focus',BLACK),('!focus',CANVAS_COLOR)    ],
            selectbackground    = [ ('disabled','#007f5b'), ('!disabled','#007f5b') ],
        );
        self.style.map(         'TLabel',

            # foreground          = [ ('disabled',Cfff), ('!disabled',"#ffefd8")    ],
            foreground          = [ ('disabled',Cfff), ('!disabled',"#ffd900")    ],
            background          = [ ('disabled',CANVAS_COLOR),('!disabled',BLACK)  ],
            bordercolor         = [ ('disabled',C444),('focus',C444), ('!focus',BLACK)    ],
        );
        self.style.map(         'TButton',

            foreground          = [ ('disabled',C101), ("!active","#ffefd8"), ("active",Cff00)   ],
            background          = [ ('disabled',"#888888"),('!active',BLACK),("active",C181)  ],
            bordercolor         = [ ('disabled',C444),('focus',C444), ('!focus',BLACK)    ],
        );

        self.style.configure(   'TFrame',
            background=BLACK,
            # background="#555555",
        );
