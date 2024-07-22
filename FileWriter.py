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

source_zip_path = "/Users/aditya/Desktop/archive (1).zip"  # Path to the source zip file
destination_zip_path = "/Users/aditya/Desktop/zipfiles"  # Path to the destination zip file

realfiles = 0
fakefiles = 0
realzip = 0
fakezip = 0
zipfiles=[zipfile.ZipFile(destination_zip_path + "/" + str(realzip) + ".zip", 'w')]
real_target_zip = zipfiles[0]
fake_target_zip = zipfiles[0]
with zipfile.ZipFile(source_zip_path, 'r') as source_zip:
    for file in source_zip.namelist():
        if "real" in file.lower() and realzip < 10:
            
            try:
                
                # Read the file from the source zip
                image_file = source_zip.open(file)
                image_data = image_file.read()
                image = Image.open(BytesIO(image_data))
                image = image.crop((0,0,image.size[0]-98, image.size[1]-20)).resize((500,500))
                    
                # Print file size for debugging
                #print(f"Size of {file} in source zip: {len(source_data)} bytes")
                
                # Write the file to the target zip
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')  # You can use other formats like 'JPEG'
                img_byte_arr.seek(0)  # Move the pointer to the beginning of the byte stream
                real_target_zip.writestr('real' + str(realfiles) + '.png', img_byte_arr.getvalue())

                #print(f"Size of {file} in target zip: {len(target_data)} bytes")
                realfiles+= 1
                if realfiles > 190:
                    realfiles = 0
                    realzip += 1
                    if realzip == len(zipfiles):
                        zipfiles.append(zipfile.ZipFile(destination_zip_path + "/" + str(realzip) + ".zip", 'w'))
                    real_target_zip = zipfiles[realzip]
            except:
                pass
        if "fake" in file.lower() and fakezip < 10:
            
            try:
                # Read the file from the source zip
                image_file = source_zip.open(file)
                image_data = image_file.read()
                image = Image.open(BytesIO(image_data))
                image = image.crop((0,0,image.size[0]-98, image.size[1]-20)).resize((500,500))
                    
                # Print file size for debugging
                #print(f"Size of {file} in source zip: {len(source_data)} bytes")
                
                # Write the file to the target zip
                img_byte_arr = io.BytesIO()
                image.save(img_byte_arr, format='PNG')  # You can use other formats like 'JPEG'
                img_byte_arr.seek(0)  # Move the pointer to the beginning of the byte stream
                fake_target_zip.writestr('fake' + str(fakefiles) + '.png', img_byte_arr.getvalue())

                #print(f"Size of {file} in target zip: {len(target_data)} bytes")
                fakefiles+= 1
                if fakefiles > 190:
                    fakefiles = 0
                    fakezip += 1
                    if fakezip == len(zipfiles):
                        zipfiles.append(zipfile.ZipFile(destination_zip_path + "/" + str(fakezip) + ".zip", 'w'))
                    fake_target_zip = zipfiles[fakezip]
            except:
                pass
print("Processing complete.")
