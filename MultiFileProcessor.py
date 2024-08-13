import os
import sys
import traceback
from tkinter import (
    END,
    BOTH,
    LEFT,
    NE,
    X,
    TOP,
    W,
    Listbox,
    Tk,
    filedialog,
)
from tkinter.ttk import Frame, Button, Scrollbar
from pathlib import Path
from strategy import FileProcessStrategy


class MultiFileProcessorUI(Frame):
    def __init__(self, strategy: FileProcessStrategy, files: list):
        super().__init__()
        self.strategy: FileProcessStrategy = strategy
        self.init_ui(files)

    def init_ui(self, files):
        self.master.resizable(0, 0)  # this removes the maximize button
        self.master.title(self.strategy.get_window_title())
        self.pack(fill=BOTH, expand=True)

        left_frame = Frame(self, borderwidth=1, relief="solid")
        right_frame = Frame(self, borderwidth=0)

        left_frame.pack(side=LEFT, fill=BOTH, padx=(5, 0), pady=5)
        right_frame.pack(side=LEFT, anchor=NE, padx=5, pady=5)

        self.listbox = Listbox(
            left_frame, width=64, borderwidth=0, highlightthickness=0, relief="flat"
        )
        self.listbox.pack(side="left", expand=True, fill=BOTH)

        scrollbar = Scrollbar(left_frame, orient="vertical")
        scrollbar.config(command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        open_button = Button(right_frame, text="Open", command=self.open)
        open_button.pack(side=TOP, anchor=W, fill=X, expand=True, ipadx=3, ipady=3)

        up_button = Button(right_frame, text="↑", command=self.move_up)
        up_button.pack(side=TOP, anchor=W, fill=X, expand=True, ipadx=3, ipady=3)

        down_button = Button(right_frame, text="↓", command=self.move_down)
        down_button.pack(
            side=TOP, anchor=W, fill=X, expand=True, ipadx=3, ipady=3, pady=(0, 10)
        )

        command_button = Button(
            right_frame,
            text=self.strategy.get_command_name(),
            command=self.run_strategy,
        )
        command_button.pack(side=TOP, anchor=W, fill=X, expand=True, ipadx=5, ipady=5)

        close_button = Button(right_frame, text="Close", command=self.master.destroy)

        close_button.pack(side=TOP, anchor=W, fill=X, expand=True, ipadx=5, ipady=5)

        if files:
            [self.listbox.insert(END, os.path.basename(f)) for f in files]
            self.output_folder = os.path.dirname(files[0])
        else:
            self.output_folder = Path.home()

    def open(self, *args):
        files = filedialog.askopenfilenames(
            initialdir=self.output_folder,
            title="Select file",
            filetypes=self.strategy.get_file_types(),
        )

        if files:
            self.output_folder = os.path.dirname(files[0])
            self.listbox.delete(0, END)
            [self.listbox.insert(END, os.path.basename(f)) for f in files]

    def move_up(self, *args):
        try:
            self.indexes = self.listbox.curselection()
            if not self.indexes:
                return
            for position in self.indexes:
                if position == 0:
                    continue
                text = self.listbox.get(position)
                self.listbox.delete(position)
                self.listbox.insert(position - 1, text)
                self.listbox.selection_set(position - 1)
        except:
            pass

    def move_down(self, *args):
        try:
            self.indexes = self.listbox.curselection()
            if not self.indexes:
                return
            for position in self.indexes:
                if position == self.listbox.size() - 1:
                    continue

                text = self.listbox.get(position)
                self.listbox.delete(position)
                self.listbox.insert(position + 1, text)
                self.listbox.selection_set(position + 1)
        except:
            pass

    def run_strategy(self):
        if self.listbox.size() == 0:
            return

        try:
            self.strategy.run(
                [self.output_folder + "\\" + f for f in self.listbox.get(0, END)]
            )
        except:
            print("Exception in user code:")
            print("-" * 60)
            traceback.print_exc(file=sys.stdout)
            print("-" * 60)


class StrategyFactory:
    @staticmethod
    def create(appName) -> FileProcessStrategy:
        if appName == "MergePDF":
            from MergePDF import MergePDF
            return MergePDF()
        elif appName == "DecryptPDF":
            from DecryptPDF import DecryptPDF
            return DecryptPDF()
        elif appName == "MergeTIFF":
            from MergeTIFF import MergeTIFF
            return MergeTIFF()
        else:
            return None


if __name__ == "__main__":
    root = Tk()
    appName = sys.argv[1]
    strategy = StrategyFactory.create(appName)
    files = sys.argv[2:]

    if strategy:
        MultiFileProcessorUI(strategy, files)
        root.mainloop()
    else:
        import ctypes

        ctypes.windll.user32.MessageBoxW(0, "Error! No Strategy Provided.", 1)
