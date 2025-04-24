import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from os.path import isfile
from pyrage import passphrase as age
from base64 import b64encode, b64decode
from tkinter import messagebox
from tkinter import END
import time
from tkinter import Scrollbar
from cryptography.fernet import Fernet


def main():
    global salsa, path, loki
    salsa = ""
    path = ""
    loki = []

    def on_close():
        close = False
        close = messagebox.askyesno("Warning", "Are you sure you want to exit?")
        if close:
            root.destroy()

    def new_file(event=None):
        global salsa, path
        close = False
        close = messagebox.askyesno("Warning", "Are you sure you want to exit this file?")
        if close:
            edit_mode_on()
            text.delete("1.0", END)
            salsa = ""
            path = ""
            root.title("pepog       new file: " + get_time())
            log("New file created")
        else:
            return
        
    def open_file(event=None):
        global salsa, path
        close = False
        close = messagebox.askyesno("Warning", "Are you sure you want to exit this file?")
        if close:
            salsa = ""
            path = ""
            try:
                path1 = filedialog.askopenfilename(defaultextension=".jage", filetypes=[("JAGE-File", "*.jage"), ("All files", "*.*")])
                if isfile(path1) == False:
                    return
                salsa1 = enter_password()
                if salsa1 == "":
                    return
                with open(path1, "r") as file:
                    content = file.read()
                decrypted = decrypt(salsa1, content)
                edit_mode_on()
                text.delete("1.0", END)
                text.insert("1.0", decrypted)
                edit_mode_off()
                root.title("pepog       file opened: " + get_time())
                path = path1
                salsa = salsa1
                log("File opened: (" + path + ")")
            except:
                log("ERROR Decrypting")
                messagebox.showerror("Error", "Error decrpyting")
        else:
            return

    def save_file(event=None):
        try:
            global path, salsa
            teksti = text.get(1.0, "end-1c")
            if teksti != "":
                if isfile(path):
                    if salsa != "":
                        with open(path, "w") as file:
                            file.write(encrypt(salsa, teksti))
                        root.title("pepog       saved: " + get_time())
                        log("File saved: ("+path+")")
                    else:
                        salsa = create_password()
                        save_file()
                else:
                    save_file_as()
            else:
                messagebox.showerror("Error", "The file is empty, can't save.")
        except:
            messagebox.showerror("Error", "Error saving the file")
                

    def save_file_as(event=None):
        global salsa, path
        try:
            teksti = text.get(1.0, "end-1c")
            if teksti != "":
                path1 = filedialog.asksaveasfilename(defaultextension=".jage", filetypes=[("JAGE-File", "*.jage"), ("All files", "*.*")])
                if path1 == "":
                    return
                salsa1 = create_password()
                if salsa1 != "":
                    with open(path1, "w") as file:
                        file.write(encrypt(salsa1, teksti))
                    salsa = salsa1
                    path = path1
                    root.title("pepog       saved as: " + get_time())
                    log("File saved as: ("+path+")")
                else:
                    messagebox.showerror("Error", "Try again")
                    save_file_as()
            else:
                messagebox.showerror("Error", "The file is empty, can't save.")
        except:
            messagebox.showerror("Error", "Error saving the file")
        
    def create_password():
        salsa1 = simpledialog.askstring("Password", "Add password", show="*", parent=root)
        salsa2 = simpledialog.askstring("Password", "Confirm password", show="*", parent=root)
        if salsa1 == salsa2 and salsa1 != "":
            log("New password created")
            return salsa1
        else:
            messagebox.showerror("Error", "Passwords don't match or are empty")
            return

    def enter_password():
        salsa1 = simpledialog.askstring("Password", "Enter password", show="*", parent=root)
        if salsa1 != "":
            log("Password entered")
            return salsa1
        else:
            messagebox.showerror("Error", "Password is empty")
            return
        
    def log(content):
        global loki
        loki.append(time.strftime("[%H:%M:%S] ", time.localtime()) + content)
        
    def edit_mode_on():
        text.config(state="normal")
    def edit_mode_off():
        text.config(state="disabled")

    def user_edit_mode_on(event=None):
        text.config(state="normal")
        log("Edit mode ON")
    def user_edit_mode_off(event=None):
        text.config(state="disabled")
        log("Edit mode OFF")
        
        

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
    edit_menu = tk.Menu(menu_bar, tearoff=0)
    others_menu = tk.Menu(menu_bar, tearoff=0)

    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open", command=open_file)

    menu_bar.add_cascade(label="Save", menu=save_menu)
    save_menu.add_command(label="Save", command=save_file)
    save_menu.add_command(label="Save As", command=save_file_as)
    
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="ON", command=user_edit_mode_on)
    edit_menu.add_command(label="OFF", command=user_edit_mode_off)

    menu_bar.add_cascade(label="Others", menu=others_menu)
    others_menu.add_command(label="Info", command=info)
    others_menu.add_command(label="Log", command=show_log)
    others_menu.add_command(label="Settings", command=settings)
    others_menu.add_separator()
    others_menu.add_command(label="Exit", command=on_close)

    root.bind("<Control-n>", new_file)
    root.bind("<Control-o>", open_file)
    root.bind("<Control-s>", save_file)
    root.bind("<Control-w>", save_file_as)
    root.bind("<Control-l>", show_log)
    root.bind("<Control-e>", user_edit_mode_on)
    root.bind("<Control-f>", user_edit_mode_off)

    root.mainloop()

def info():
    teksti = "pepog v: 0.6\nMade by JH\n\nFile names aren't encrypted\nTest verison, some bugs may occur\nEncryption: age (pyrage)"
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
    
    
def show_log(event=None):
    global loki
    log_w = tk.Tk()
    log_w.title("Log")
    log_w.configure(background="black")
    log_w.minsize(200, 200)
    log_w.geometry("600x500")
    menu_bar = tk.Menu(log_w)
    log_w.config(menu=menu_bar)
    menu = tk.Menu(menu_bar, tearoff=0)
    
    def save_log(event=None):
        global loki
        path2 = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("TXT-File", "*.txt"), ("All files", "*.*")])
        log_to_txt = ""
        for x in range(len(loki)):
            log_to_txt += loki[x]+"\n"
        log_to_txt += time.strftime("[%H:%M:%S]", time.localtime()) + "Log saved as txt: ("+path2+")"
        with open(path2, "w") as file:
            file.write(log_to_txt)
        loki.append(time.strftime("[%H:%M:%S] ", time.localtime()) + "Log saved as txt: ("+path2+")")
        messagebox.showinfo("Success", "Log saved")
    
    menu_bar.add_cascade(label="Options", menu=menu)
    menu.add_command(label="Save", command=save_log)
    v=Scrollbar(log_w, orient='vertical')
    v.pack(side="right", fill='y')
    text = tk.Text(log_w, wrap="word", undo=False, bg="black", fg="white", insertbackground="white", insertwidth=0.5, highlightthickness=0, borderwidth=0, yscrollcommand=v.set)
    for x in range(len(loki)):
        text.insert(END,loki[x]+"\n")
    text.config(state="disabled")
    text.pack(expand="yes", fill="both", padx=15,pady=10)

    log_w.bind("<Control-s>", save_log)
    

    log_w.mainloop()

def settings():
    teksti = "No settings for you     yet..."
    setting = tk.Tk()
    setting.title("Settings")
    setting.configure(background="black")
    setting.minsize(270, 150)
    setting.geometry("300x150")
    setting.columnconfigure(0, weight=1)
    setting.columnconfigure(1, weight=1)
    setting.columnconfigure(2, weight=1)
    setting.rowconfigure(0, weight=3)
    setting.rowconfigure(1, weight=3)
    setting.rowconfigure(2, weight=3)
    setting.rowconfigure(3, weight=3)
    setting.rowconfigure(4, weight=1)
    tk.Label(setting, text=teksti, bg="black", fg="white").grid(row=0, column=1)
    button = tk.Button(setting, text="Close", bg="black", fg="white", command=setting.destroy)
    button.grid(row=3, column=1)
    setting.mainloop()

def encrypt(password, text):
    return b64encode(age.encrypt(str(text).encode(), str(password))).decode()

def decrypt(password, text):
    return age.decrypt(b64decode(str(text).encode()), str(password)).decode()

def get_time():
    return time.strftime("%H:%M", time.localtime())

try:
    main()
except:
    messagebox.showerror("Error", "Random ahh error")