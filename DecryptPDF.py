import os
from tkinter import simpledialog, messagebox
from contextlib import suppress
from strategy import FileProcessStrategy

class DecryptPDF(FileProcessStrategy):
    def get_window_title(self):
        return "Decrypt PDF (jake.jeon@daum.net)"

    def get_file_types(self):
        return [("PDF files", ".pdf")]

    def get_command_name(self):
        return "Decrypt"

    def run(self, files):
        qpdf = r"\\blackrock\dfs\HKG\USERS012\Hjeon\dev\tools\MultiFileProcessor\qpdf\qpdf.exe"
        outputFolder = os.path.dirname(files[0])

        error_count = 0
        total_count = 0
        for input_file in files:
            total_count = total_count + 1
            output_file_name = (
                outputFolder + "/Unencrypted_" + os.path.basename(input_file)
            )

        basename = os.path.basename(input_file)
        password = ""
        while password == "":
            password = simpledialog.askstring(
                title="PDF Document", prompt=basename + " password?:"
            )

        with suppress(Exception):
            os.remove(output_file_name)

        # Decrypt
        command = (
            qpdf
            + " --password="
            + password
            + " --decrypt "
            + '"'
            + input_file
            + '" "'
            + output_file_name
            + '"'
        )
        os.system(command)

        # Failed
        if not os.path.exists(output_file_name):
            error_count = error_count + 1
            messagebox.showerror("Error", "Failed to decrypt " + basename)
