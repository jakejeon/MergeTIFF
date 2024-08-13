import os
import tifftools
from tkinter import messagebox
from strategy import FileProcessStrategy


class MergeTIFF(FileProcessStrategy):
    def get_window_title(self):
        return "Merge TIFF (jake.jeon@daum.net)"

    def get_file_types(self):
        return [("TIFF files", ".tif .tiff")]

    def get_command_name(self):
        return "Merge"

    def run(self, files):
        if len(files) < 2:
            return

        try:
            outputFolder = os.path.dirname(files[0])
            outputFileName = outputFolder + "/" + "__MERGED__.tiff"
            tifftools.tiff_concat(files, outputFileName, overwrite=True)
            messagebox.showinfo("", "Merged")
        except Exception as e:
            messagebox.showerror("", str(e))