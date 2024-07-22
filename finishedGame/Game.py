import os
os.system("pip3 install matplotlib")
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import zipfile
from PIL import Image
import zipfile
from PIL import Image
import random
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import smtplib
from email.mime.text import MIMEText


class ImageGuessingGame:
   def __init__(self, master):
       self.master = master
       self.master.title("AI or Real Image Game")
       self.master.geometry("600x500")


       self.current_image_path = ""
       self.is_ai_image = False
       self.guesses = 0


       self.aizip = "finishedGame/AIProduction.zip"
       self.realzip = "finishedGame/RealProduction.zip"


       self.score = 0
       self.total_guesses = 0


       self.realimagesright = 0
       self.realimageswrong = 0
       self.fakeimagesright = 0
       self.fakeimageswrong = 0


       self.feedbackvar = tk.StringVar()


       self.create_widgets()
       self.load_random_image()


   def create_widgets(self):
       self.image_label = tk.Label(self.master)
       self.image_label.pack(pady=10)


       self.question_label = tk.Label(self.master, text="Is this image AI-generated or real?", font=("Arial", 14))
       self.question_label.pack(pady=10)


       self.button_frame = tk.Frame(self.master)
       self.button_frame.pack(pady=10)


       self.ai_button = tk.Button(self.button_frame, text="AI", command=lambda: self.check_guess(True), width=10)
       self.ai_button.pack(side=tk.LEFT, padx=10)


       self.real_button = tk.Button(self.button_frame, text="Real", command=lambda: self.check_guess(False), width=10)
       self.real_button.pack(side=tk.LEFT, padx=10)


       self.score_label = tk.Label(self.master, text="Score: 0/0", font=("Arial", 12))
       self.score_label.pack(pady=10)
       self.feedback = tk.Label(self.master, textvariable=self.feedbackvar)
       self.feedback.pack()


   def load_random_image(self):
       image_files = []
       if random.choice([True, False]):
           zip = zipfile.ZipFile(self.aizip,"r")
           self.is_ai_image = True
       else:
           zip = zipfile.ZipFile(self.realzip,"r")
           self.is_ai_image = False


       image_files = [Image.open(zip.open(f)) for f in zip.namelist() if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
       if not image_files:
           messagebox.showerror("Error", f"Try again. Nothing found in {zip}")
           return


       image = random.choice(image_files)
       image = image.resize((400, 300), Image.LANCZOS)
       photo = ImageTk.PhotoImage(image)


       self.image_label.config(image=photo)
       self.image_label.image = photo


   def check_guess(self, guessed_ai):
       self.total_guesses += 1
       if guessed_ai == self.is_ai_image:
           self.score += 1
           result = "Correct!"
       else:
           result = "Incorrect."
      
       if guessed_ai and self.is_ai_image:
           self.fakeimagesright += 1
       if guessed_ai and not self.is_ai_image:
           self.fakeimageswrong += 1
       if not guessed_ai and self.is_ai_image:
           self.fakeimageswrong += 1
       if not guessed_ai and not self.is_ai_image:
           self.realimagesright += 1   
      




       self.score_label.config(text=f"Score: {self.score}/{self.total_guesses}")
       self.feedbackvar.set(f"{result} The image was {'AI-generated' if self.is_ai_image else 'real'}.")
       self.guesses += 1
       if self.guesses < 20:
           self.load_random_image()
       else:
           stream_data(self)
           root.destroy()


def stream_data(self):
   global label, realimagesright, realimageswrong, fakeimagesright, fakeimageswrong, root, real
   message = MIMEText(f"Real Images Right: {self.realimagesright} Real Images Wrong: {self.realimageswrong}\nFake Images Right: {self.fakeimagesright} Fake Images Wrong: {self.fakeimageswrong}")
   message["Subject"] = "Real V Fake Results"
   message["From"] = "cygnus3119@gmail.com"
   message["To"] = "cygnus3119@gmail.com"
   s = smtplib.SMTP('smtp.gmail.com', 587)
   s.starttls()
   key = open("finishedGame/systeminfo.txt", "r")
   s.login('cygnus3119@gmail.com', key.readline().removesuffix("\n"))
   key.close()
   s.sendmail("cygnus3119@gmail.com", ["cygnus3119@gmail.com"], message.as_string())
   s.quit()
   root.destroy()


if __name__ == "__main__":
   root = tk.Tk()
   game = ImageGuessingGame(root)
   root.protocol("WM_DELETE_WINDOW", lambda: stream_data(game))
   root.mainloop()
