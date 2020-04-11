from TexSoup import TexSoup # works with TexSoup version 0.1
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import ttk
import sys
import traceback

def items_before(original_latex:str, split:int) -> str:
    r"""returns a frame that contains items 1 to split
    from the itemize in the original frame
    >>> print(items_before(r'''\begin{frame}
    ... \begin{itemize}
    ... \item foo
    ... \item bar
    ... \item
    ... \end{itemize}
    ... \end{frame}
    ... ''',2))
    \begin{frame}
    <BLANKLINE>
    \begin{itemize}
    <BLANKLINE>
    \item foo
    \item bar\end{itemize}
    <BLANKLINE>
    \end{frame}"""
    soup=TexSoup(original_latex)
    children=list(soup.itemize.children)
    for child in children[split:]: 
        soup.itemize.remove_child(child)
    return str(soup)

def items_after(original_latex:str, split:int) -> str:
    r"""returns a frame that contains items split+1 to the end
    from the itemize in the original frame
    >>> print(items_after(r'''\begin{frame}
    ... \begin{itemize}
    ... \item foo
    ... \item bar
    ... \item
    ... \end{itemize}
    ... \end{frame}''', 2))
    \begin{frame}
    <BLANKLINE>
    \begin{itemize}
    <BLANKLINE>
    \item\end{itemize}
    <BLANKLINE>
    \end{frame}"""    
    soup=TexSoup(original_latex)
    children=list(soup.itemize.children)
    for child in children[:split]: 
        soup.itemize.remove_child(child)
    return str(soup)

class Application(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, width=50, height=50)
        self.master = master
        self.pack()
        #self.pack_propagate(0) #Don't allow the widgets inside to determine the frame's width / height
        #self.pack(fill=ttk.BOTH, expand=True) #Expand the frame to fill the root window
        self.master.title('Split LaTeX Beamer Frame')
        self.create_widgets()

    def create_widgets(self):
        #self.master.grid_rowconfigure(1, weight=1)
        #self.master.grid_rowconfigure(5, weight=1)
        #self.master.grid_columnconfigure(0, weight=1)
        opts = {"padx": 20, "pady": 5}
        ttk.Label(self, text="Input Text").grid(row=0, column=0, columnspan=2,
                 sticky=tk.W, **opts)
        self.clear_button = ttk.Button(self, text="Clear", command=self.clear_input)
        self.clear_button.grid(row=0, column=2, sticky=tk.E, **opts)
        self.input_text = scrolledtext.ScrolledText(self, height=8)
        self.input_text.grid(row=1, column=0, columnspan=3, **opts)
        ttk.Label(self, text="Insert after item number:").grid(row=2, column=0,
                 sticky=tk.NW, **opts)
        self.split_after = ttk.Entry(self)
        self.split_after.grid(row=2, column=2, sticky=tk.W+tk.E, **opts)
        self.split_button = ttk.Button(self,
            text="Split text\nand copy to >>\nclipboard", command=self.split_text)
        self.split_button.grid(row=3, column=1)
        ttk.Label(self, text="Output Text").grid(row=4, column=0, columnspan=3,
                 sticky=tk.W, **opts)
        self.output_text = scrolledtext.ScrolledText(self, height=8)
        self.output_text.grid(row=5, column=0, columnspan=3, pady=(5,20), padx=20)

    def split_text(self):
        try:
            try:
                split = int(self.split_after.get())
            except ValueError:
                messagebox.showerror("Error", "'{}' is not a valid item number".format(self.split_after.get()))
                return
            input_string = self.input_text.get("1.0", "end-1c")
            self.output_text.delete("1.0", "end")
            output_string = items_before(input_string, split) + '\n' + items_after(input_string, split)
            self.output_text.insert("1.0", output_string)
            self.master.clipboard_clear()
            self.master.clipboard_append(output_string)
            self.output_text.focus_set()
            self.output_text.tag_add("sel", "1.0", "end")
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", "Error occurred during split: {}".format(e))

    def clear_input(self):
        self.input_text.delete("1.0", "end")
        self.input_text.focus_set()

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
