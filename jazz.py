from tkinter import *              # Importing necessary modules from tkinter for GUI creation
from tkinter import filedialog     # Importing file dialog from tkinter to open file selection dialogs
from tkinter import messagebox     # Importing messagebox from tkinter for displaying alerts
from Crypto import Random          # Importing Random from PyCryptodome for generating IVs
from Crypto.Cipher import AES      # Importing AES from PyCryptodome for AES encryption and decryption
import os                          # Importing os for file operations
from pathlib import Path           # Importing Path from pathlib for path operations
from PIL import ImageTk, Image     # Importing ImageTk and Image from PIL for image processing
import tkinter.font as tkFont      # Importing font module from tkinter for custom fonts
import sys                         # Importing sys for system-specific parameters and functions

root = Tk()                        # Creating the main application window
root.title("Encryption & Decryption") # Setting the title of the main window
root.geometry("400x390")           # Setting the size of the main window

class Encryptor:
    def __init__(self, key):
        self.key = key

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size) # Padding the message to be multiple of block size

    def encrypt(self, message, key, key_size=128):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size) # Generating a random IV
        cipher = AES.new(key, AES.MODE_CBC, iv) # Creating a new AES cipher
        return iv + cipher.encrypt(message) # Returning the IV concatenated with the encrypted message

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc" , 'wb') as fo:
            fo.write(enc)
        os.remove(file_name) # Removing the original file after encryption

    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size] # Extracting the IV from the ciphertext
        cipher = AES.new(key, AES.MODE_CBC, iv) # Creating a new AES cipher with the extracted IV
        plaintext = cipher.decrypt(ciphertext[AES.block_size:]) # Decrypting the ciphertext
        return plaintext.rstrip(b"\0") # Removing padding

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name) # Removing the encrypted file after decryption

key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)
clear = lambda: os.system('cls') # Clearing the console (specific to Windows)

def showimg():
    window3 = Toplevel(window2)
    window3.title("Decrypted Image")
    im = Image.open(filename[:-4]) # Opening the decrypted image
    tkimage = ImageTk.PhotoImage(im)
    myvar = Label(window3, image=tkimage)
    myvar.image = tkimage
    myvar.pack()
    window3.mainloop()

def encrypt():
    password = pass1.get(1.0, END).strip() # Getting the entered password

    if not password:
        messagebox.showwarning("Warning!", "Please enter a cipher key.")
    else:
        f = open(s + r"\data.txt", "w+")
        f.write(password)
        f.close()
        enc.encrypt_file(s + r"\data.txt")
        enc.encrypt_file(filename)
        messagebox.showinfo("Success!", "Image encrypted successfully...")

        # Reset the encryption window
        pass1.delete(1.0, END)  # Clear the password field
        window1.title("Encryption")  # Reset the title

def decrypt():
    password2 = pass2.get(1.0, END).strip()
    enc.decrypt_file(s + r"\data.txt.enc")

    with open(s + r"\data.txt", "r") as f:
        p = f.read().strip()

    if p == password2:
        enc.decrypt_file(filename)
        messagebox.showinfo("Success!", "Image successfully decrypted!")
        btn = Button(window2, text="Show File", width=14, height=2, command=showimg)
        btn.place(x=163, y=280)
    else:
        enc.encrypt_file(s + r"\data.txt")
        messagebox.showerror("Password Mismatched", "Incorrect cipher key!")

        # Reset the decryption window
        pass2.delete(1.0, END)
        window2.title("Decryption")

def choosefile1():
    global filename, s
    file1 = filedialog.askopenfile(mode='r', filetype=[('jpg file', '*.jpg')])
    if file1 is not None:
        filename = file1.name
        p = Path(filename)
        Label(window1, text=p.name, bg='#111111', fg='white').place(x=140, y=155)
        s = str(p.parent)

def choosefile2():
    global filename, s
    file1 = filedialog.askopenfile(mode='r', filetype=[('jpg file', '*.jpg.enc')])
    if file1 is not None:
        filename = file1.name
        p = Path(filename)
        Label(window2, text=p.name, bg='#000', fg='#fff').place(x=140, y=75)
        s = str(p.parent)

def openEncrypt():
    global window1
    global pass1
    window1 = Toplevel(root)
    root.withdraw()  # Hide the main window
    window1.title("Encryption")
    window1.geometry("450x350")
    canv = Canvas(window1, width=445, height=345, bg='#FFFFFF')
    canv.grid(row=2, column=3)
    fontStyle = tkFont.Font(family="Lucida Grande", size=11)
    label_pass = Label(window1, text="Create Cipher Key", bg='#FFFFFF', fg='black', font=fontStyle)
    label_pass.place(x=75, y=60)
    pass1 = Text(window1, height=1, width=18)
    pass1.place(x=200, y=60)
    encryptbtn = Button(window1, text="Choose File to Encrypt", width=18, height=1, command=choosefile1)
    encryptbtn.place(x=145, y=130)
    btn = Button(window1, text="Encrypt", width=14, height=2, command=encrypt)
    btn.place(x=160, y=220)

    def go_back_to_main():
        window1.destroy()
        root.deiconify()  # Show the main window

    back_button = Button(window1, text="Back", command=go_back_to_main)
    back_button.place(x=10, y=10)  # Adjust position as needed
    window1.mainloop()

def openDecrypt():
    global window2
    global pass2
    window2 = Toplevel(root)
    root.withdraw()  # Hide the main window
    window2.title("Decryption")
    window2.geometry("450x370")
    canv = Canvas(window2, width=445, height=365, bg='#fff')
    canv.grid(row=2, column=3)
    fontStyle = tkFont.Font(family="Lucida Grande", size=11)
    decryptbtn = Button(window2, text="Choose File to Decrypt", width=18, height=1, command=choosefile2)
    decryptbtn.place(x=150, y=50)
    label_pass = Label(window2, text="Enter Cipher key", bg='#fff', fg='black', font=fontStyle)
    label_pass.place(x=75, y=130)
    pass2 = Text(window2, height=1, width=18)
    pass2.place(x=195, y=130)
    btn = Button(window2, text="Decrypt", width=14, height=2, command=decrypt)
    btn.place(x=163, y=220)

    def go_back_to_main():
        window2.destroy()
        root.deiconify()  # Show the main window

    back_button = Button(window2, text="Back", command=go_back_to_main)
    back_button.place(x=10, y=10)  # Adjust position as needed
    window2.mainloop()

clear()  # Clear the console
print("Working on files...")

# Load and display background image
img = Image.open("My Edits/Screenshot (3).png")
img = img.resize((395, 385))
bg = ImageTk.PhotoImage(img)
label1 = Label(root, image=bg)
label1.place(x=0, y=0)

# Create buttons to open encryption and decryption windows
btn1 = Button(root, text="Encrypt", width=14, height=2, command=openEncrypt)
btn1.place(x=150, y=127)
btn2 = Button(root, text="Decrypt", width=14, height=2, command=openDecrypt)
btn2.place(x=150, y=225)

root.mainloop()  # Start the Tkinter event loop