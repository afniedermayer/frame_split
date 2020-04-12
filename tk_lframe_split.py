import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
import sys
import traceback
from latex_frame_split import split_frame

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=50, height=50)
        self.master = master
        self.pack(fill="both", expand=True)
        self.master.title('Split LaTeX Beamer Frame')
        self.create_widgets()
        self.master.minsize(350, 150)

    def create_widgets(self):
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=3)
        opts = {"padx": 20, "pady": 5}
        ttk.Label(self, text="Input Text").grid(row=0, column=0, columnspan=2,
                 sticky=tk.W, **opts)
        self.clear_button = ttk.Button(self, text="Clear", command=self.clear_input, underline=0)
        self.clear_button.grid(row=0, column=2, sticky=tk.E, **opts)
        self.input_text = scrolledtext.ScrolledText(self, height=8)
        self.input_text.grid(row=1, column=0, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S, **opts)
        self.split_button = ttk.Button(self, text="Split text and copy to clipboard", 
            command=self.split_text, underline=0)
        self.split_button.grid(row=2, column=2, sticky=tk.E, **opts)
        ttk.Label(self, text="Output Text").grid(row=2, column=0, columnspan=3,
                 sticky=tk.W, **opts)
        self.output_text = scrolledtext.ScrolledText(self, height=8)
        self.output_text.grid(row=3, column=0, columnspan=3, sticky=tk.E+tk.W+tk.N+tk.S,
            pady=(5,20), padx=20)
        self.master.bind('<Alt-s>', lambda event: self.split_text())
        self.master.bind('<Alt-c>', lambda event: self.clear_input())
        self.input_text.focus_set()

    def split_text(self):
        position = self.input_text.count('1.0', tk.INSERT)[0]
        buffer = self.input_text.get("1.0", "end-1c")
        self.output_text.delete("1.0", "end")
        try:
            frame, frame1, frame2 = split_frame(buffer, position)
        except ValueError as e:
            traceback.print_exc()
            self.show_warning('Error: {}'.format(e.args[0]))
            return
        new_frame = frame1 + '\n\n' + frame2
        self.output_text.insert("1.0", new_frame)
        self.master.clipboard_clear()
        self.master.clipboard_append(new_frame)
        self.output_text.focus_set()
        self.output_text.tag_add("sel", "1.0", "end")

    def clear_input(self):
        self.input_text.delete("1.0", "end")
        self.input_text.focus_set()

    def show_warning(self, message):
        messagebox.showerror("Error", message)


def main():
    try:
        while True:
            print('paste frame (end with empty line): ')
            s = ''
            while True:
                newline = input()
                if newline == '': break
                s += newline + '\n'
            print()
            split = int(input('split after item: '))
            print()
            print(str(items_before(s, split)))
            print()
            print(items_after(s, split))
            print()
            print('press Ctrl-C to exit')
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        main()
    elif len(sys.argv) > 1 and sys.argv[1] == '-h':
        print('split_latex_frame')
        print('command line arguments:')
        print(' -t: text interface (default: gui interface)')
        print(' -h: help')
    elif len(sys.argv) > 1:
        print('unknown command line argument(s): ' + ' '.join(sys.argv[1:]))
    else:
        root = tk.Tk()
        root.style = ttk.Style()
        # root.style.theme_use("clam")
        # root.geometry("300x300")
        app = Application(master=root)
        app.mainloop()
