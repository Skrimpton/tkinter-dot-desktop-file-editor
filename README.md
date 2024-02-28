# tkinter-dot-desktop-file-editor
.desktop-file editor using configparser and tkinter

This is not a well-tested nor finished product.

# EPILEPTIC SEIZURE WARNING
There is a lot of flickering when scrolling, especially when scrolling while hovering over the scrollbar.

### Usage
- can be used with or without -f
![tkeditor-example](https://github.com/Skrimpton/tkinter-dot-desktop-file-editor/assets/64572787/70e149e5-0210-4905-a023-251633455ed8)

### Keyboard shortcuts:

- ```<Ctrl+plus>``` and ```<Ctrl+minus>``` enlarges and shrinks font-sizes and is in effect zoom in/out.
  - Does not handle keypad keys (yet)

- Holding ```<Ctrl>``` enables touchpad zooming.

- Holding ```<Alt>``` enables touchpad scrolling.
  - Touchpad scrolling horizontally and vertically both scroll the frame up and down.
  - This is due to event.delta always returning 0 on linux, so ```<Button>``` event is handled instead
  - ```<Button>```-event does not reveal direction, according to my searxng results
  - TODO: add check for OS-type and make ```<MouseWheel>``` logic

- ```<Alt+Up/Down>``` scrolls the window

- ```<Alt+Left/Right>``` scrolls the text of focused entry-field

## 28.02.2024 update:
# Several tweaks have been made:
- Non-toggleable darkmode (aka bestmode)
   
- Scrolling disabled when fullscreen / scrollable content is smaller than the window
  
- In place editing of both key and value  ( requires Python v. 3.6+ )
  - This comes at the cost of much higher RAM use for larger files due to the lack of on-demand-gui-loading and the weight of all those entry-fields. ( ~65 mb ram for the firefox-dummy )
    
  - I'm working on a treeview-version which will have better/smoother and cleaner scrolling and hopefully be less rescource demanding. Downside: it might be too hard for me to keep undo/redo histories for all items. 
