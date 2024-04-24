# Project Three Updates

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import datetime
import os

class MainWindow(tk.Tk):      # defines the main window of the class 
    def __init__(self):
        super().__init__()
        self.geometry("600x400")
        self.title('Notebook')
        self.notes = []     # empty list to store the notes
        
        # frame and buttons for new notes, opening notebook, and saving notebook 
        #adding a notebook button
        new_button = ttk.Button(self, text="New Note", command=self.new_note)
        new_button.pack(side=tk.LEFT, padx=10, pady=10, anchor='center')  # Center the button
        new_notebook_btn = ttk.Button(self, text="Create Notebook", command=self.new_notebook)
        new_notebook_btn.pack(side=tk.LEFT, padx=10, pady=10, anchor='center')
        open_button = ttk.Button(self, text="Open Notebook", command=self.open_notebook)
        open_button.pack(side=tk.LEFT, padx=10, pady=10, anchor='center')  # Center the button
        save_button = ttk.Button(self, text="Save Notebook", command=self.save_notebook)
        save_button.pack(side=tk.LEFT, padx=10, pady=10, anchor='center')  # Center the button

        self.note_frame = tk.Frame(self)
        self.note_frame.pack(padx=10, pady=10)


# creates new notes 
    def new_note(self):
        note_window = Form(self, self.notes)
    
    def new_notebook(self):
        notebook_window = NotebookForm(self)
        
# can open existing notes that have been saved
    def open_notebook(self):
        initial_dir = os.path.dirname(os.path.realpath(__file__))
        dir_path = filedialog.askdirectory(initialdir=initial_dir)
        
        if dir_path:
            try:
                files = [f for f in os.listdir(dir_path) if f.endswith(".json")]
                self.notes = []
                
                for file in files:
                    file_path = os.path.join(dir_path, file)
                    with open(file_path, "r") as file:
                        note_content = json.load(file)
                        self.notes.append(note_content)
                    
                self.display_notes()
            except FileNotFoundError:
                messagebox.showwarning("Warning", "No notebook found.")
        else:
            messagebox.showwarning("Warning", "No notebook selected.")

    def save_notebook(self):
        initial_dir = os.path.dirname(os.path.realpath(__file__))
        dir_path = filedialog.askdirectory(initialdir=initial_dir)
        
        if dir_path:
            try:
                # WARNING: the following 3 lines will delete all json files in ur folder :D
                json_files = [f for f in os.listdir(dir_path) if f.endswith(".json")]
                for file in json_files:
                    os.remove(os.path.join(dir_path, file))
                
                for note in self.notes:
                    file_path = os.path.join(dir_path, note["title"]) + ".json"
                    with open(file_path, "w") as file:
                        json.dump(note, file)
            except FileNotFoundError:
                messagebox.showwarning("Warning", "No notebook found.")
        else:
            messagebox.showwarning("Warning", "No notebook selected.")
            
# allows it to appear on the notebook in the main window

    def display_notes(self):
        for widget in self.note_frame.winfo_children():  # winfo_children --> retrieves all the widgets within the the self note frame
            widget.destroy()
        for note in self.notes:
            note_button = ttk.Button(self.note_frame, text=note["title"], command=lambda n=note: self.show_note_details(n))
            note_button.pack(pady=5)

    def show_note_details(self, note):
        note_window = Form(self, self.notes, note)

# window with a form for the new note

class NotebookForm(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title('Create New Notebook')
        #prompt = ttk.Label(notebook_name_prompt, 
        #      text ="Notebook Title: ")
        #prompt.pack(side=tk.LEFT, padx=10, pady=10, anchor='center')  # Center the button
        # create widgets for title, text, and tags
        self.title_label = ttk.Label(self, text="Notebook Title:")
        self.title_label.pack(side=tk.TOP, padx=10, pady=5)
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack(side=tk.TOP, padx=10, pady=5)
        
        self.submit_button = ttk.Button(self, text="Initialize Notebook", command=self.initNoteBook)
        self.submit_button.pack(side=tk.TOP, padx=10, pady=10)
  
    def initNoteBook(self):
        title = self.title_entry.get()
        timestamp = str(datetime.datetime.now())

        #self.master.new_notebook_save()
        #new_notebook_save code is used below 
        directory = "notebook " + title
        self.master.notebook = title
        
        # Parent Directory path  
        parent_dir = os.path.dirname(os.path.realpath(__file__))
        
        # Path  
        path = os.path.join(parent_dir, directory)
        self.master.notebook_filepath = path
            
        # Create the directory in '/home / User / INST326'  
        os.mkdir(path)  
        print("Directory '% s' created" % directory)  
        
        #figure out how to print notebook name as a button on main screen
        #figure out how to add notes to the labeled notebooks and put things in
        #their file directory
        
        # if directory / file that  is to be created already  
        # exists then 'FileExistsError'  
        # will be raised by os.mkdir() method  

        # if specified path is invalid 'FileNotFoundError' Error  
        # will be raised   
        
        self.master.display_notes()
        self.destroy() 

class Form(tk.Toplevel):
    def __init__(self, master, notes, note=None):
        super().__init__(master)
        self.title('New Note' if note is None else 'Note Details')

        self.master = master
        self.notes = notes
        self.note = note

        # Create widgets for title, text, tags, and author
        self.title_label = ttk.Label(self, text="Title:")
        self.title_label.pack(side=tk.TOP, padx=10, pady=5)
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack(side=tk.TOP, padx=10, pady=5)

        self.text_label = ttk.Label(self, text="Text:")
        self.text_label.pack(side=tk.TOP, padx=10, pady=5)
        self.text_entry = tk.Text(self, height=10, width=40)
        self.text_entry.pack(side=tk.TOP, padx=10, pady=5)

        self.tags_label = ttk.Label(self, text="Tags:")
        self.tags_label.pack(side=tk.TOP, padx=10, pady=5)
        self.tags_entry = ttk.Entry(self)
        self.tags_entry.pack(side=tk.TOP, padx=10, pady=5)

        self.author_label = ttk.Label(self, text="Author:")
        self.author_label.pack(side=tk.TOP, padx=10, pady=5)
        self.author_entry = ttk.Entry(self)
        self.author_entry.pack(side=tk.TOP, padx=10, pady=5)

        # Create submit button
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(side=tk.TOP, padx=10, pady=10)

        if note is not None:
            self.fill_form()

    def fill_form(self):
        self.title_entry.delete(0, tk.END)
        self.text_entry.delete(1.0, tk.END)
        self.tags_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        if self.note:
            self.title_entry.insert(0, self.note["title"])
            self.text_entry.insert(tk.END, self.note["text"])
            self.tags_entry.insert(0, self.note.get("tags", ""))
            self.author_entry.insert(0, self.note.get("author", ""))

    def submit(self):
        title = self.title_entry.get()
        text = self.text_entry.get("1.0", tk.END).strip()
        tags = self.tags_entry.get().strip()
        author = self.author_entry.get().strip()
        timestamp = str(datetime.datetime.now())

        if self.note is None:
            self.notes.append({"title": title, "text": text, "tags": tags, "author": author, "created_at": timestamp, 
            "edit_history":[]})
        else:
            self.note["title"] = title
            self.note["text"] = text
            self.note["tags"] = tags
            self.note["author"] = author
            self.note["edit_history"].append({"timestamp": timestamp, "changes": {"title": title, 
            "text": text, "tags": tags, "author":author}})
            
        self.master.display_notes()
        self.destroy()
        
class SnippetForm(tk.Toplevel):
    def __init__(self, master, snippets, snippet=None):
        super().__init__(master)
        self.title('New Snippet' if snippet is None else 'Snippet Details')

        self.master = master
        self.snippets = snippets
        self.snippet = snippet
        self.edit_mode = False

        # Create widgets for snippet title and code
        self.title_label = ttk.Label(self, text="Title:")
        self.title_label.pack(side=tk.TOP, padx=10, pady=5)
        self.title_entry = ttk.Entry(self)
        self.title_entry.pack(side=tk.TOP, padx=10, pady=5)

        self.code_label = ttk.Label(self, text="Code:")
        self.code_label.pack(side=tk.TOP, padx=10, pady=5)
        self.code_entry = tk.Text(self, height=10, width=40)
        self.code_entry.pack(side=tk.TOP, padx=10, pady=5)

        # Create submit and edit buttons
        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)
        self.submit_button.pack(side=tk.TOP, padx=10, pady=10)
        self.edit_button = ttk.Button(self, text="Edit", command=self.toggle_edit_mode)
        self.edit_button.pack(side=tk.TOP, padx=10, pady=5)

        if snippet is not None:
            self.fill_form()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if self.edit_mode:
            self.title_entry.config(state=tk.NORMAL)
            self.code_entry.config(state=tk.NORMAL)
            self.submit_button.config(state=tk.NORMAL, text="Save")
        else:
            self.fill_form()

    def fill_form(self):
        self.title_entry.delete(0, tk.END)
        self.code_entry.delete(1.0, tk.END)
        if self.snippet:
            self.title_entry.insert(0, self.snippet["title"])
            self.code_entry.insert(tk.END, self.snippet["code"])

    def submit(self):
        title = self.title_entry.get()
        code = self.code_entry.get("1.0", tk.END).strip()
        timestamp = str(datetime.datetime.now())

        if self.snippet is None:
            self.snippets.append({"title": title, "code": code, "created_at": timestamp, "edit_history": []})
        else:
            self.snippet["title"] = title
            self.snippet["code"] = code
            self.snippet["edit_history"].append({"timestamp": timestamp, "changes": {"title": title, "code": code}})
        self.master.save_snippets()
        self.master.display_snippets()
        self.destroy()


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()