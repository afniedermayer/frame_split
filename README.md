# LaTeX Split Frame

Splits a `frame` in a [LaTeX beamer presentation](https://en.wikibooks.org/wiki/LaTeX/Presentations) at the cursor position. Works for a split position in an `itemize` environment, an `enumerate` environment and no environment.

## Sublime Text 3 Plugin

### Installation

Copy the files `latex_frame_split.py` and `sublime_lframe_split.py` into your Sublime User Package directory. On Windows this is usually `C:\Users\YOUR_USER_NAME\AppData\Roaming\Sublime Text 3\Packages\User`. You have to replace YOUR_USER_NAME with your actual user name.

Also download the file `Default (Windows).sublime-keymap` into your Sublime User Package directory. Replace `Windows` with the name of your operating system if you are not using Windows. If you don't want to overwrite your default keymap, copy the following into your `Default (Windows).sublime-keymap` file:
```
[
	{"keys": ["ctrl+alt+s"], "command": "lsplit"}
]
```

### Usage

Set your cursor at the place where you wish to split the frame. Press "Ctrl-Alt-s". The frame is replaced by the split frame.

### Example

Input:

<img src="screenshots/sublime_before.png" width="400" />

Press "Ctrl-Alt-s", output:

<img src="screenshots/sublime_after.png" width="400" />


## Standalone Script with Graphical User Interface

### Installation

You should have Python 3.7+ installed. Download the .py files into a directory of your choice. 

### Usage

Open a terminal on Unix or a PowerShell on Windows, change to the directory with the .py files and type
```
python tk_lframe_split.py
```
Copy and paste LaTeX code into the input text box, place cursor at desired split position and press the "Split text and copy to clipboard" button.

### Example

Input:

<img src="screenshots/before.png" width="600" />

Output:

<img src="screenshots/after.png" width="600" />

## Limitations

If the `enumerate` or `itemize` environment that is being split is inside some other environment, then the text before and after the `enumerate` or `itemize` is copied to both new frames. You will have to manually remove the redundant text.

Splitting an `enumerate` environment is programmed to split an `enumerate` that starts counting items at 1. In particular, if the `enumerate` didn't start counting at 1 but at some `M`>1, i.e. it contained a `\setcounter{enumi}{M}`, then the `setcounter` command has to be manually replaced by `\setcounter{enumi}{M+N}` where `N` is the number of items before the split.

If the cursor is in a different environment than `itemize` or `enumerate`, then the result of splitting the frame might be invalid LaTeX code.
