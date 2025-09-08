import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from appendixd import copy_contents_to_appendix


class AppendixGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Appendix Generator")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        # Center the window
        self.center_window()

        # Variables
        self.folder_var = tk.StringVar()
        self.skip_folder_var = tk.StringVar()
        self.output_var = tk.StringVar(value="appendix.txt")
        self.mode_var = tk.StringVar(value="default")
        self.ignore_patterns_var = tk.StringVar()
        self.manual_files_var = tk.StringVar()
        self.last_generated_file = None  # Track the last generated file

        self.create_widgets()

    def center_window(self):
        """Center the window on the screen"""
        self.root.update_idletasks()
        width = 800
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Main container with padding
        main_container = ttk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # Title
        title_label = ttk.Label(main_container, text="Appendix Generator",
                               font=("TkDefaultFont", 16, "bold"))
        title_label.pack(pady=(0, 30))

        # Main content frame
        content_frame = ttk.Frame(main_container)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Configure grid weights for content frame
        content_frame.columnconfigure(1, weight=1)

        row = 0

        # Input section frame
        input_section = ttk.LabelFrame(content_frame, text="Input Configuration", padding="20")
        input_section.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        input_section.columnconfigure(1, weight=1)

        # Folder selection
        ttk.Label(input_section, text="Folder to Convert:").grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        folder_frame = ttk.Frame(input_section)
        folder_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8)
        folder_frame.columnconfigure(0, weight=1)

        ttk.Entry(folder_frame, textvariable=self.folder_var, font=("TkDefaultFont", 10)).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 8))
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).grid(row=0, column=1)

        # Skip folder
        ttk.Label(input_section, text="Folder to Skip:").grid(row=1, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        ttk.Entry(input_section, textvariable=self.skip_folder_var, font=("TkDefaultFont", 10)).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=8)

        # Output file
        ttk.Label(input_section, text="Output File:").grid(row=2, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        output_frame = ttk.Frame(input_section)
        output_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=8)
        output_frame.columnconfigure(0, weight=1)

        ttk.Entry(output_frame, textvariable=self.output_var, font=("TkDefaultFont", 10)).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 8))
        ttk.Button(output_frame, text="Browse", command=self.browse_output).grid(row=0, column=1)

        row += 1

        # Mode selection section
        mode_section = ttk.LabelFrame(content_frame, text="Processing Mode", padding="20")
        mode_section.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        modes = [("Default (auto-detect)", "default"),
                ("All files", "all"),
                ("Ignore patterns", "ignore"),
                ("Manual file list", "manual")]

        for i, (text, value) in enumerate(modes):
            ttk.Radiobutton(mode_section, text=text, variable=self.mode_var,
                           value=value, command=self.on_mode_change).grid(row=i//2, column=i%2,
                           sticky=tk.W, padx=(0, 20), pady=4)

        row += 1

        # Mode-specific options section
        options_section = ttk.LabelFrame(content_frame, text="Options", padding="20")
        options_section.grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        options_section.columnconfigure(1, weight=1)
        options_section.rowconfigure(1, weight=1)

        # Ignore patterns (for ignore mode)
        self.ignore_label = ttk.Label(options_section, text="Ignore Patterns:")
        self.ignore_label.grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        self.ignore_entry = ttk.Entry(options_section, textvariable=self.ignore_patterns_var, font=("TkDefaultFont", 10))
        self.ignore_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=8)

        self.ignore_help = ttk.Label(options_section, text="Separate patterns with spaces (e.g., *.log *.tmp)",
                                    font=("TkDefaultFont", 9), foreground="gray")
        self.ignore_help.grid(row=1, column=1, sticky=tk.W, pady=(0, 8))

        # Manual files (for manual mode)
        self.manual_label = ttk.Label(options_section, text="Manual Files:")
        self.manual_label.grid(row=0, column=0, sticky=(tk.W, tk.N), pady=8, padx=(0, 10))

        manual_frame = ttk.Frame(options_section)
        manual_frame.grid(row=0, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=8)
        manual_frame.columnconfigure(0, weight=1)
        manual_frame.rowconfigure(0, weight=1)

        self.manual_text = scrolledtext.ScrolledText(manual_frame, height=6, wrap=tk.WORD, font=("TkDefaultFont", 10))
        self.manual_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        manual_buttons_frame = ttk.Frame(manual_frame)
        manual_buttons_frame.grid(row=1, column=0, sticky=tk.W, pady=(8, 0))

        ttk.Button(manual_buttons_frame, text="Add Files", command=self.add_files).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(manual_buttons_frame, text="Clear Files", command=self.clear_files).grid(row=0, column=1)

        row += 1

        # Actions section
        actions_section = ttk.Frame(content_frame)
        actions_section.grid(row=row, column=0, columnspan=2, pady=20)

        # Button frame for centered buttons
        button_frame = ttk.Frame(actions_section)
        button_frame.pack()

        # Generate button
        self.generate_btn = ttk.Button(button_frame, text="Generate Appendix",
                                      command=self.generate_appendix)
        self.generate_btn.grid(row=0, column=0, padx=8, ipadx=20, ipady=8)

        # Clear button
        self.clear_btn = ttk.Button(button_frame, text="Clear All",
                                   command=self.clear_all_fields)
        self.clear_btn.grid(row=0, column=1, padx=8, ipadx=20, ipady=8)

        # Download button
        self.download_btn = ttk.Button(button_frame, text="Download Last File",
                                      command=self.download_last_file, state='disabled')
        self.download_btn.grid(row=0, column=2, padx=8, ipadx=20, ipady=8)

        row += 1

        # Status section
        status_section = ttk.Frame(content_frame)
        status_section.grid(row=row, column=0, columnspan=2, pady=(20, 0))

        # Progress bar
        self.progress = ttk.Progressbar(status_section, mode='indeterminate', length=400)
        self.progress.pack(pady=(0, 10))

        # Status label
        self.status_label = ttk.Label(status_section, text="Ready to generate appendix",
                                     font=("TkDefaultFont", 10))
        self.status_label.pack()

        # Initially hide mode-specific widgets
        self.on_mode_change()

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select folder to convert")
        if folder:
            self.folder_var.set(folder)

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save appendix as",
            initialvalue="appendix.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if filename:
            self.output_var.set(filename)

    def add_files(self):
        files = filedialog.askopenfilenames(title="Select files to include")
        if files:
            current_text = self.manual_text.get(1.0, tk.END).strip()
            if current_text:
                current_text += "\n"
            for file in files:
                current_text += file + "\n"
            self.manual_text.delete(1.0, tk.END)
            self.manual_text.insert(1.0, current_text)

    def clear_files(self):
        self.manual_text.delete(1.0, tk.END)

    def on_mode_change(self):
        mode = self.mode_var.get()

        # Hide/show ignore pattern widgets
        if mode == "ignore":
            self.ignore_label.grid()
            self.ignore_entry.grid()
            self.ignore_help.grid()
        else:
            self.ignore_label.grid_remove()
            self.ignore_entry.grid_remove()
            self.ignore_help.grid_remove()

        # Hide/show manual file widgets
        if mode == "manual":
            self.manual_label.grid()
            self.manual_text.master.grid()
        else:
            self.manual_label.grid_remove()
            self.manual_text.master.grid_remove()

    def validate_inputs(self):
        if not self.folder_var.get() and self.mode_var.get() != "manual":
            messagebox.showerror("Error", "Please select a folder to convert")
            return False

        if not self.output_var.get():
            messagebox.showerror("Error", "Please specify an output file")
            return False

        if self.mode_var.get() == "manual":
            files_text = self.manual_text.get(1.0, tk.END).strip()
            if not files_text:
                messagebox.showerror("Error", "Please add files for manual mode")
                return False

        return True

    def generate_appendix(self):
        if not self.validate_inputs():
            return

        # Disable the button and start progress
        self.generate_btn.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="Generating appendix...")

        # Run in a separate thread to avoid freezing the UI
        thread = threading.Thread(target=self.run_generation)
        thread.daemon = True
        thread.start()

    def run_generation(self):
        try:
            # Prepare arguments
            folder = self.folder_var.get()
            skip_folder = self.skip_folder_var.get()
            output_file = self.output_var.get()
            mode = self.mode_var.get()

            ignore_patterns = None
            if mode == "ignore" and self.ignore_patterns_var.get():
                ignore_patterns = self.ignore_patterns_var.get().split()

            manual_files = None
            if mode == "manual":
                files_text = self.manual_text.get(1.0, tk.END).strip()
                if files_text:
                    manual_files = [f.strip() for f in files_text.split('\n') if f.strip()]

            # Call the original function
            copy_contents_to_appendix(
                folder,
                output_file,
                skip_folder,
                mode,
                ignore_patterns=ignore_patterns,
                manual_files=manual_files
            )

            # Update last generated file
            self.last_generated_file = output_file

            # Update UI on success
            self.root.after(0, self.on_success)

        except Exception as e:
            # Update UI on error
            self.root.after(0, lambda: self.on_error(str(e)))

    def on_success(self):
        self.progress.stop()
        self.generate_btn.config(state='normal')
        self.status_label.config(text="Appendix generated successfully!")
        self.download_btn.config(state='normal')  # Enable download button
        messagebox.showinfo("Success",
                           f"Appendix generated successfully!\n\n"
                           f"Output: {self.output_var.get()}\n\n"
                           f"WARNING: This is in .txt format for editing before you convert it to PDF.\n"
                           f"Editing before converting is highly recommended as there might be bugs.")

    def on_error(self, error_msg):
        self.progress.stop()
        self.generate_btn.config(state='normal')
        self.status_label.config(text="Error occurred during generation")
        messagebox.showerror("Error", f"An error occurred:\n{error_msg}")

    def download_last_file(self):
        if self.last_generated_file and os.path.exists(self.last_generated_file):
            # Ask where to save the downloaded file
            download_path = filedialog.asksaveasfilename(
                title="Download last generated file",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if download_path:
                try:
                    # Copy the last generated file to the new location
                    with open(self.last_generated_file, 'rb') as fsrc:
                        with open(download_path, 'wb') as fdst:
                            fdst.write(fsrc.read())
                    messagebox.showinfo("Download complete", f"File downloaded to:\n{download_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to download file:\n{str(e)}")
        else:
            messagebox.showwarning("No file", "No file has been generated yet to download.")

    def clear_all_fields(self):
        """Clear all input fields and reset the form"""
        self.folder_var.set("")
        self.skip_folder_var.set("")
        self.output_var.set("appendix.txt")
        self.mode_var.set("default")
        self.ignore_patterns_var.set("")
        self.manual_files_var.set("")
        self.last_generated_file = None

        # Clear text in manual file list
        self.manual_text.delete(1.0, tk.END)

        # Reset status label
        self.status_label.config(text="Ready to generate appendix")

        # Disable download button
        self.download_btn.config(state='disabled')

        # Update mode-specific widgets visibility
        self.on_mode_change()


def main():
    root = tk.Tk()
    app = AppendixGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
