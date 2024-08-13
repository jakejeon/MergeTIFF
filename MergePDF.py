import os
from pdfrw import PdfReader, PdfWriter
from tkinter import messagebox
from strategy import FileProcessStrategy


class MergePDF(FileProcessStrategy):
    def get_window_title(self):
        return "Merge PDF (jake.jeon@daum.net)"

    def get_file_types(self):
        return [("PDF files", ".pdf")]

    def get_command_name(self):
        return "Merge"

    def run(self, files):
        if len(files) < 2:
            return

        try:
            outputFolder = os.path.dirname(files[0])
            outputFileName = outputFolder + "/" + "__MERGED__.pdf"

            writer = PdfWriter()
            for inputFile in files:
                writer.addpages(PdfReader(inputFile).pages)

                writer.write(outputFileName)

            messagebox.showinfo("", "Merged")
        except:
            messagebox.showerror("", "__MERGED__ file is being used by anothe program.")
