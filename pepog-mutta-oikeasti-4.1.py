import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from os.path import isfile
from pyrage import passphrase as age
from base64 import b64encode, b64decode
from tkinter import messagebox
from tkinter import END

def main():
    global salsa, path
    salsa = ""
    path = ""

    def on_close():
        close = False
        close = messagebox.askyesno("Warning", "Are you sure you want to exit?")
        if close:
            root.destroy()

    def new_file():
        global salsa, path
        close = False
        close = messagebox.askyesno("Warning", "Are you sure you want to exit this file?")
        if close:
            text.delete("1.0", END)
            salsa = ""
            path = ""
        else:
            return
        
    def open_file():
        global salsa, path
        close = False
        close = messagebox.askyesno("Warning", "Are you sure you want to exit this file?")
        if close:
            salsa = ""
            path = ""
            try:
                path = filedialog.askopenfilename(defaultextension=".jage", filetypes=[("JAGE-File", "*.jage")])
                with open(path, "r") as file:
                    content = file.read()
                salsa = create_password()
                decrypted = decrypt(salsa, content)
                text.delete("1.0", END)
                text.insert("1.0", decrypted)
            except:
                messagebox.showerror("Error", "Error decrpyting")
        else:
            return

    def save_file():
        try:
            global path, salsa
            teksti = text.get(1.0, "end-1c")
            if teksti != "":
                if isfile(path):
                    if salsa != "":
                        with open(path, "w") as file:
                            file.write(encrypt(salsa, teksti))
                    else:
                        salsa = create_password()
                        save_file()
                else:
                    save_file_as()
            else:
                messagebox.showerror("Error", "The file is empty, can't save.")
        except:
            messagebox.showerror("Error", "Error saving the file")
                

    def save_file_as():
        try:
            teksti = text.get(1.0, "end-1c")
            if teksti != "":
                path1 = filedialog.asksaveasfilename(defaultextension=".jage", filetypes=[("JAGE-File", "*.jage")])
                salsa = create_password()
                if salsa != "":
                    with open(path1, "w") as file:
                        file.write(encrypt(salsa, teksti))
                    messagebox.showinfo("Success", "File saved")
                else:
                    messagebox.showerror("Error", "Try again")
                    save_file_as()
            else:
                messagebox.showerror("Error", "The file is empty, can't save.")
        except:
            messagebox.showerror("Error", "Error saving the file")
        
    def create_password():
        salsa1 = simpledialog.askstring("Password", "Add password", show="*")
        salsa2 = simpledialog.askstring("Password", "Confirm password", show="*")
        if salsa1 == salsa2 and salsa1 != "":
            return salsa1
        else:
            messagebox.showerror("Error", "Passwords don't match or are empty")

    root = tk.Tk()
    root.title("pepog")
    root.configure(background="black")
    root.minsize(200, 200)
    root.geometry("600x500")

    root.protocol("WM_DELETE_WINDOW",  on_close)

    text = tk.Text(root, wrap="word", undo=True, bg="black", fg="white", insertbackground="white", insertwidth=0.5, highlightthickness=0, borderwidth=0)
    text.pack(expand="yes", fill="both", padx=30,pady=30)

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    save_menu = tk.Menu(menu_bar, tearoff=0)
    others_menu = tk.Menu(menu_bar, tearoff=0)

    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open", command=open_file)

    menu_bar.add_cascade(label="Save", menu=save_menu)
    save_menu.add_command(label="Save", command=save_file)
    save_menu.add_command(label="Save As", command=save_file_as)

    menu_bar.add_cascade(label="Others", menu=others_menu)
    others_menu.add_command(label="Info", command=info)
    others_menu.add_command(label="Settings", command=info)
    others_menu.add_separator()
    others_menu.add_command(label="Exit", command=on_close)

    root.mainloop()

def info():
    teksti = "pepog v.k2\nMade by Juuso"
    info = tk.Tk()
    info.title("Info")
    info.configure(background="black")
    info.minsize(270, 150)
    info.geometry("300x150")
    info.columnconfigure(0, weight=1)
    info.columnconfigure(1, weight=1)
    info.columnconfigure(2, weight=1)
    info.rowconfigure(0, weight=3)
    info.rowconfigure(1, weight=3)
    info.rowconfigure(2, weight=3)
    info.rowconfigure(3, weight=3)
    info.rowconfigure(4, weight=1)
    tk.Label(info, text=teksti, bg="black", fg="white").grid(row=0, column=1)
    button = tk.Button(info, text="Close", bg="black", fg="white", command=info.destroy)
    button.grid(row=3, column=1)
    info.mainloop()
    
def encrypt(password, text):
    return b64encode(age.encrypt(str(text).encode(), str(password))).decode()

def decrypt(password, text):
    return age.decrypt(b64decode(str(text).encode()), str(password)).decode()


try:
    main()
except:
    messagebox.showerror("Error", "Random ass error")