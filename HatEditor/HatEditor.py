import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import webbrowser
import os

class CodeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("HatEditor")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.current_file = None
        self.current_language = "Plain Text"
        self.current_extension = ".txt"
        self.current_workspace = None

        self.text_editor = tk.Text(root, bg='black', fg='white', state='normal', insertbackground='white')
        self.text_editor.pack(expand=True, fill=tk.BOTH)
        self.text_editor.bind("<<Modified>>", self.on_modified)
        self.text_editor.bind("<Control-f>", lambda event: self.search_code())

        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.language_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.workspace_menu = tk.Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Language", menu=self.language_menu)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.menu_bar.add_cascade(label="Workspace", menu=self.workspace_menu)

        self.root.config(menu=self.menu_bar)

        self.create_file_menu()
        self.create_language_menu()
        self.create_settings_menu()
        self.create_workspace_menu()

        # Bind keyboard shortcuts
        root.bind('<Control-s>', lambda event: self.save_file())
        root.bind('<Control-S>', lambda event: self.save_file_as())

        self.auto_recovery()

    def create_file_menu(self):
        self.file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        self.file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        self.file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        self.file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.on_close)

    def create_language_menu(self):
        languages = [
            ("Plain Text", ".txt"),
            ("Python", ".py"),
            ("Java", ".java"),
            ("C", ".c"),
            ("C++", ".cpp"),
            ("HTML", ".html"),
            ("CSS", ".css"),
            ("JavaScript", ".js"),
            ("PHP", ".php"),
            ("Ruby", ".rb"),
            ("Swift", ".swift"),
            ("Go", ".go"),
            ("Rust", ".rs")
        ]

        for language, extension in languages:
            self.language_menu.add_command(label=language, command=lambda lang=language, ext=extension: self.set_language(lang, ext))

    def create_settings_menu(self):
        self.settings_menu.add_command(label="HTML Viewer", command=self.open_html_viewer)
        self.settings_menu.add_command(label="Search", command=self.search_code)

    def create_workspace_menu(self):
        self.workspace_menu.add_command(label="New Workspace", command=self.new_workspace)
        self.workspace_menu.add_command(label="Open Workspace", command=self.open_workspace)

    def new_file(self):
        self.text_editor.delete(1.0, tk.END)
        self.current_file = None
        self.text_editor.edit_modified(False)
        self.root.title("HatEditor")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.current_file = file_path
            with open(file_path, "r") as file:
                content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, content)
            self.text_editor.edit_modified(False)
            self.root.title("HatEditor - " + os.path.basename(file_path))

    def save_file(self):
        if self.current_file:
            content = self.text_editor.get(1.0, tk.END)
            with open(self.current_file, "w") as file:
                file.write(content)
            self.text_editor.edit_modified(False)
            self.root.title("HatEditor - " + os.path.basename(self.current_file))
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=self.current_extension,
                                                 filetypes=[(f"{self.current_language} files", f"*{self.current_extension}"), ("All files", "*.*")])
        if file_path:
            content = self.text_editor.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.current_file = file_path
            self.text_editor.edit_modified(False)
            self.root.title("HatEditor - " + os.path.basename(self.current_file))

    def set_language(self, language, extension):
        self.current_language = language
        self.current_extension = extension

    def open_html_viewer(self):
        if self.current_language == "HTML":
            html_content = self.text_editor.get(1.0, tk.END)
            with open("temp.html", "w") as file:
                file.write(html_content)
            webbrowser.open("temp.html")
        else:
            messagebox.showinfo("Error", "HTML Viewer is only available for HTML files.")

    def search_code(self):
        search_text = simpledialog.askstring("Search", "Enter text to search:")
        if search_text:
            content = self.text_editor.get(1.0, tk.END)
            start_index = content.find(search_text)
            if start_index != -1:
                line_number = content.count('\n', 0, start_index) + 1
                char_index = start_index - content.rfind('\n', 0, start_index)
                messagebox.showinfo("Search Result", f"Text found at Line {line_number}, Column {char_index}")
                self.text_editor.tag_add("search", f"{line_number}.{char_index}", f"{line_number}.{char_index + len(search_text)}")
                self.text_editor.tag_config("search", background="yellow", foreground="black")
                self.text_editor.mark_set(tk.INSERT, f"{line_number}.{char_index}")
                self.text_editor.see(tk.INSERT)
            else:
                messagebox.showinfo("Search Result", "Text not found.")

    def new_workspace(self):
        self.current_workspace = None
        self.new_file()

    def open_workspace(self):
        file_path = filedialog.askopenfilename(filetypes=[("Workspace files", "*.workspace"), ("All files", "*.*")])
        if file_path:
            self.current_workspace = file_path
            with open(file_path, "r") as file:
                content = file.read()
                self.text_editor.delete(1.0, tk.END)
                self.text_editor.insert(tk.END, content)
            self.text_editor.edit_modified(False)
            self.root.title("HatEditor - Workspace: " + os.path.basename(file_path))

    def save_workspace(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".workspace", filetypes=[("Workspace files", "*.workspace"), ("All files", "*.*")])
        if file_path:
            content = self.text_editor.get(1.0, tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.current_workspace = file_path
            self.text_editor.edit_modified(False)
            self.root.title("HatEditor - Workspace: " + os.path.basename(file_path))

    def on_modified(self, event):
        self.root.title("HatEditor - " + os.path.basename(self.current_file) + "*")

    def auto_recovery(self):
        recovery_file = os.path.join(os.path.dirname(__file__), "source", "recovery")
        if os.path.isfile(recovery_file):
            if messagebox.askyesno("Recovery", "Recovery file found. Do you want to recover the code?"):
                with open(recovery_file, "r") as file:
                    content = file.read()
                    self.text_editor.delete(1.0, tk.END)
                    self.text_editor.insert(tk.END, content)
                os.remove(recovery_file)

    def on_close(self):
        if self.text_editor.edit_modified():
            save_changes = messagebox.askyesnocancel("Save Changes", "Do you want to save changes before exiting?")
            if save_changes is None:
                return
            elif save_changes:
                self.save_file()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    editor = CodeEditor(root)
    root.mainloop()
