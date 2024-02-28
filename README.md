# tkinter-dot-desktop-file-editor
.desktop-file editor using configparser and tkinter

### This is not an actual tool. 
This is to test out stuff and map limitations of aforementioned stuff, my brain, and tkinter.

It can edit, but handling edits of the keys (left side) is bad and, for now, disallows saving under at least one safe condition 
<br>(to avoid key-clobbering, which would be worse).

# EPILEPTIC SEIZURE WARNING
Yes, for real.

There is a lot of flickering when scrolling, especially large documents when scrolling with mouse or touchpad while hovering over the scrollbar.

## Example video:

https://github.com/Skrimpton/tkinter-dot-desktop-file-editor/assets/64572787/acf69b57-bb69-488f-a83a-de65c07a0c72

## Usage
- can be used with or without -f
![tkeditor-example](https://github.com/Skrimpton/tkinter-dot-desktop-file-editor/assets/64572787/70e149e5-0210-4905-a023-251633455ed8)

### Keyboard shortcuts:  
- ```<Ctrl+Space>``` scrolls view to the currently focused entry 

- ```<Ctrl+plus>``` and ```<Ctrl+minus>``` enlarges and shrinks font-sizes and is in effect zoom in/out.
  - Does not handle keypad keys (yet)

- Holding ```<Ctrl>``` enables touchpad zooming.

- Holding ```<Alt>``` enables touchpad scrolling inside the window / ouside of the scrollbar.
  - Why? I decided to let the fields take precedence over window for scrolling.
  - Also: Touchpad scrolling horizontally and vertically both scroll the frame up and down.
  - This is due to event.delta always returning 0 on linux, so ```<Button>```-event is handled instead.
  - ```<Button>```-events do not reveal direction, according to both my experience and searxng results.
  - TODO: add check for OS-type and ```<MouseWheel>```-logic

- ```<Alt+Up/Down>``` scrolls the window

- ```<Alt+Left/Right>``` scrolls the text of focused entry-field

## 28.02.2024 update:
# Several tweaks have been made:
- Non-toggleable darkmode (aka bestmode)
   
- Scrolling now disables when fullscreen / scrollable content is smaller than the window
  
- [\(Hopefully safe)](https://stackoverflow.com/a/59196714) In-place editing of both key and value
  - BUG: will deny saving under at least one safe condition 
  - I think this requires Python v. 3.6+.
  - If anyone ever sees this and knows, please leave a comment/issue.

- This version also comes with a much higher RAM cost and slower load time for larger files
  <br>due to the lack of on-demand-gui-loading and the weight of all those entry-fields. ( ~65 mb ram for the firefox-dummy )
    
#### I'm working on a treeview-version which will have better/smoother scrolling<br>... and, hopefully, needs both less resources and avoids problems with key editing.
