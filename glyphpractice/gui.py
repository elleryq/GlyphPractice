import sys
import os
import subprocess
import threading
import time
import codecs
import tempfile
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, askyesno
from tkinter.scrolledtext import ScrolledText

from glyphpractice.cli import generate


class GPFrame(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Glyph practice book generator")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W+E+N+S)

        ttk.Label(self, text="Filename:").grid(column=0, row=1, sticky=(W, E))

        self.fn = StringVar()
        self.fn_entry = ttk.Entry(self, width=32, textvariable=self.fn)
        self.fn_entry.grid(column=1, row=1, sticky=(W, E))

        self.btnBrowse = Button(self, text="Browse",
                                command=self.load_file, width=10)
        self.btnBrowse.grid(row=1, column=2, sticky=W)

        self.editArea = ScrolledText(self, wrap=WORD, width=100, height=10)
        self.editArea.grid(row=2, column=0, columnspan=3, sticky=W)

        self.progress = ttk.Progressbar(self, length=200)
        self.progress.grid(row=3, column=1, sticky=W)

        self.btnGenerate = Button(self, text="Generate",
                                  command=self.generate_pdf, width=10)
        self.btnGenerate.grid(row=3, column=2, sticky=W)

    def load_file(self):
        fname = askopenfilename(filetypes=(("Text files", "*.txt"),
                                           ("All files", "*.*")))
        if fname:
            try:
                self.fn_entry.insert(0, fname)
                self.editArea.delete(1.0, END)
                with codecs.open(fname, encoding="utf-8") as f:
                    self.editArea.insert(INSERT, f.read())
            except Exception as ex:
                showerror("Open", repr(ex))
            return

    def generate_thread(self, fn):
        self.pdf_fn = generate(fn)
        self.done = True

    def text2file(self, text):
        with tempfile.NamedTemporaryFile("wt", encoding='utf-8', delete=False) as fp:
            fp.write(text)
            fn = fp.name
            fp.close()
        new_out_file = "{0}.txt".format(fn)
        os.rename(fn, new_out_file)
        return new_out_file

    def generate_pdf(self):
        text = self.editArea.get(1.0, END)
        if text:
            fname = self.text2file(text)
            self.done = False
            thread = threading.Thread(
                target=self.generate_thread,
                args=(fname,))
            thread.start()
            self.progress.start()
            while not self.done:
                time.sleep(1)
                self.progress.update()
            self.progress.stop()
            os.remove(fname)
            answer = askyesno(
                "Confirmation",
                "'{0}' is generated!  Would you like to open it?".format(
                    self.pdf_fn))
            if answer:
                if sys.platform == 'linux':
                    subprocess.call(["xdg-open", self.pdf_fn])
                else:
                    os.startfile(self.pdf_fn)

    def enterGeneratingState(self):
        self.btnBrowse.config(state='disabled')
        self.btnGenerate.config(state='disabled')

    def leaveGeneratingState(self):
        self.btnBrowse.config(state='normal')
        self.btnGenerate.config(state='normal')


if __name__ == "__main__":
    GPFrame().mainloop()
