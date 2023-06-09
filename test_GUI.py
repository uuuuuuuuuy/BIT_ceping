import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class LoginApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.master.title("Login")
        self.master.geometry("300x200")
        self.master.configure(background='light grey')

        style = ttk.Style()
        style.configure('T.Label', background='light grey', font=('Arial', 12))
        style.configure('T.Entry', font=('Arial', 12))
        style.configure('T.Button', background='dark grey', font=('Arial', 12))

        # Center the window
        window_width = self.master.winfo_reqwidth()
        window_height = self.master.winfo_reqheight()
        position_right = int(self.master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.master.winfo_screenheight() / 2 - window_height / 2)
        self.master.geometry("+{}+{}".format(position_right, position_down))

    def create_widgets(self):
        # Load the logos


        username_label = ttk.Label(self, text="Username:")
        username_label.pack(side="top", padx=10, pady=10)

        self.username_entry = ttk.Entry(self)
        self.username_entry.pack(side="top", padx=10, pady=10)


        password_label = ttk.Label(self, text="Password:")
        password_label.pack(side="top", padx=10, pady=10)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.pack(side="top", padx=10, pady=10)


        quit_button = ttk.Button(self, text="QUIT", command=self.master.destroy)
        quit_button.pack(side="bottom", padx=10, pady=10)

    # ... rest of the class code ...

def main():
    root = tk.Tk()
    app = LoginApp(master=root)
    app.mainloop()



