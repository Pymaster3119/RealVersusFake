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
import io
import hashlib

zips = ["70gb.zip", "archive (7).zip"]
with zipfile.ZipFile('Training Dataset.zip', "w") as origional:
    for zip in zips:
        with zipfile.ZipFile(zip, "r") as tocopy:
            for file in tocopy.namelist():
                if "real" in file.lower():
                    
                    try:
                        # Read the file from the source zip
                        image_file = tocopy.open(file)
                        image_data = image_file.read()
                        image = Image.open(BytesIO(image_data))
                        image = image.crop((0,0,image.size[0]-98, image.size[1]-20)).resize((500,500))
                            
                        # Print file size for debugging
                        #print(f"Size of {file} in source zip: {len(source_data)} bytes")
                        
                        # Write the file to the target zip
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format='PNG')  # You can use other formats like 'JPEG'
                        img_byte_arr.seek(0)  # Move the pointer to the beginning of the byte stream
                        tocopy.writestr('real' + hashlib.sha384(file.encode()).hexdigest() + '.png', img_byte_arr.getvalue())
                    except:
                        pass
                if "fake" in file.lower():
                    
                    try:
                        # Read the file from the source zip
                        image_file = tocopy.open(file)
                        image_data = image_file.read()
                        image = Image.open(BytesIO(image_data))
                        image = image.crop((0,0,image.size[0]-98, image.size[1]-20)).resize((500,500))
                            
                        # Print file size for debugging
                        #print(f"Size of {file} in source zip: {len(source_data)} bytes")
                        
                        # Write the file to the target zip
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format='PNG')  # You can use other formats like 'JPEG'
                        img_byte_arr.seek(0)  # Move the pointer to the beginning of the byte stream
                        tocopy.writestr('fake' + hashlib.sha384(file.encode()).hexdigest() + '.png', img_byte_arr.getvalue())
                    except:
                        pass