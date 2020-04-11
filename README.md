# LaTeX Split Frame

Splits a `frame` in a [LaTeX beamer presentation](https://en.wikibooks.org/wiki/LaTeX/Presentations).

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

The code does not distinguish between LaTeX comments and regular LaTeX code. So if your have commented out `\begin{frame}` or similar code inside the frame, it might generate wrong output.

The code is made to split frames at the cursor when the cursor is in an `itemize` environment or if the cursor is not in any environment. Splitting will be incorrect if the cursor is in an other environment, e.g. an `enumerate` environment.