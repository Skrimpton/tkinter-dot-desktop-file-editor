# tkinter-dot-desktop-file-editor
.desktop-file editor using configparser and tkinter

This is not a well-tested nor finished product.

### Usage
- can be used with or without -f
![tkeditor-example](https://github.com/Skrimpton/tkinter-dot-desktop-file-editor/assets/64572787/70e149e5-0210-4905-a023-251633455ed8)


## 28.02.2024 update:
# Several tweaks have been made:
- Non-toggleable darkmode (aka bestmode)
   
- Scrolling disabled when fullscreen / scrollable content is smaller than the window

- <Ctrl+plus> and <Ctrl+minus> (not the ones on keypad) enlarges and shrinks font-sizes and is in effect zoom in/out.

- Scrolling on the window is enabled by holding <Alt>.
  - On touchpad up & down and left & right both scroll the frame up and down.
  <br> This is due to event.delta always returning 0 on linux, so <Button> is overloaded and does not differenciate directionalty 

- In place editing of both key and value  ( requires Python v. 3.6+ )
  - This comes at the cost of much higher RAM use for larger files due to the lack of on-demand-gui-loading and the weight of all those entry-fields. ( ~65 mb ram for the firefox-dummy )
    
  - I'm working on a treeview-version which will have better/smoother and cleaner scrolling and hopefully be less rescource demanding. Downside: it might be too hard for me to keep undo/redo histories for all items. 
