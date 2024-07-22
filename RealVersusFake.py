import zipfile
from io import BytesIO
from PIL import Image
import random
import matplotlib.pyplot as plt
import tkinter
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText
import smtpd
import asyncore
import threading

root = tkinter.Tk()
frame = tkinter.Frame(root)
frame.pack()
label = tkinter.Label(frame)
label.grid(row=0, column=0)
tkinter.Button(frame, text="Real", command=lambda: ask_answers("r")).grid(row=1, column=0)
tkinter.Button(frame, text="Fake", command=lambda: ask_answers("f")).grid(row=1, column=1)
imagedescription = tkinter.StringVar(root)
tkinter.Label(frame, textvariable=imagedescription).grid(row=0, column=1)
realimagesright = 0
realimageswrong = 0
fakeimagesright = 0
fakeimageswrong = 0
tk_img = 0
global real
def run_game():
    global label, realimagesright, realimageswrong, fakeimagesright, fakeimageswrong, root, real, tk_img
    with zipfile.ZipFile("/Users/aditya/Desktop/archive (1).zip", 'r') as images:
        imagepath = random.choice(images.namelist())
        with images.open(imagepath) as image_file:
            real = "real" in imagepath
            image_data = image_file.read()
            image = Image.open(BytesIO(image_data))
            image = image.crop((0,0,image.size[0]-98, image.size[1]-20)).resize((500,500))
            tk_img = ImageTk.PhotoImage(image)
            label.configure(image=tk_img)
def ask_answers(userchoice):
    global label, realimagesright, realimageswrong, fakeimagesright, fakeimageswrong, root, real
    if real and (userchoice=="r"):
        realimagesright += 1
    if real and (userchoice=="f"):
        realimageswrong += 1
    if not real and (userchoice=="r"):
        fakeimageswrong += 1
    if not real and (userchoice=="f"):
        fakeimagesright += 1

    create_description()
    root.after(1, run_game)

def create_description():
    global label, realimagesright, realimageswrong, fakeimagesright, fakeimageswrong, root, real
    imagedescription.set(f"Right: {realimagesright + fakeimagesright} \nWrong: {realimageswrong + fakeimageswrong}")
    
def stream_data():
    global label, realimagesright, realimageswrong, fakeimagesright, fakeimageswrong, root, real
    message = MIMEText(f"Real Images Right: {realimagesright} Real Images Wrong: {realimageswrong}\nFake Images Right: {fakeimagesright} Fake Images Wrong: {fakeimageswrong}")
    message["Subject"] = "Real V Fake Results"
    message["From"] = "cygnus3119@gmail.com"
    message["To"] = "cygnus3119@gmail.com"
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login('cygnus3119@gmail.com', "qvry svmr biem zzcg")
    s.sendmail("cygnus3119@gmail.com", ["cygnus3119@gmail.com"], message.as_string())
    s.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", stream_data)
create_description()
root.after(1, run_game)
root.mainloop()