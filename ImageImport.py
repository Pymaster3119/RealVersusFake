import zipfile
import hashlib
from io import BytesIO
from PIL import Image

def import_images(path):
    #Imports images from zip file at path provided
    #Returns a tuple containing (real, fake)
    realimgs = []
    fakeimgs = []
    with zipfile.ZipFile(path, 'r') as zip:
        for file in zip.namelist():
            if "real" in file.lower():
                    image_file = zip.open(file)
                    image_data = image_file.read()
                    image = Image.open(BytesIO(image_data))
                    image = image.crop((0,0,image.size[0]-98, image.size[1]-20)).resize((500,500))
                    realimgs.append(image)
            if "fake" in file.lower():
                try:
                    image_file = zip.open(file)
                    image_data = image_file.read()
                    image = Image.open(BytesIO(image_data))
                    image = image.crop((0,0,image.size[0]-98, image.size[1]-20)).resize((500,500))
                    fakeimgs.append(image)
                except:
                    pass
    return (realimgs, fakeimgs)

#Merge them all!!!
index = 0
with zipfile.ZipFile("/Users/aditya/Desktop/archive (1).zip", "a") as bigboi:
    with zipfile.ZipFile("/Users/aditya/Desktop/AiArtData (checked).zip", "r") as zip1:
            with zipfile.ZipFile("/Users/aditya/Desktop/Archive.zip", "r") as zip2:
                with zipfile.ZipFile("/Users/aditya/Desktop/AI watermark.zip", "r") as zip3:
                    with zipfile.ZipFile("/Users/aditya/Desktop/Real Watermark.zip", "r") as zip4:
                        with zipfile.ZipFile("/Users/aditya/Desktop/AI Production.zip", "w") as aiproduction:
                            with zipfile.ZipFile("/Users/aditya/Desktop/Real Production.zip", "w") as realproduction:
                                for file in zip1.namelist():
                                    try:
                                        print(index)
                                        ifile = zip1.open(file)
                                        image = Image.open(ifile)
                                        img_byte_arr = BytesIO()
                                        image.save(img_byte_arr, format = "PNG")
                                        img_byte_arr.seek(0)
                                        bigboi.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "fake" + str(index) + '.png', img_byte_arr.getvalue())
                                        aiproduction.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "fake" + str(index) + '.png', img_byte_arr.getvalue())
                                        index += 1
                                    except Exception as e:
                                        pass
                                for file in zip2.namelist():
                                    print(index)
                                    try:
                                        print(index)
                                        ifile = zip1.open(file)
                                        image = Image.open(ifile)
                                        img_byte_arr = BytesIO()
                                        image.save(img_byte_arr, format="PNG")
                                        img_byte_arr.seek(0)
                                        if("ai" in file.lower()):
                                            bigboi.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "fake" + str(index) + '.png', img_byte_arr.getvalue())
                                            realproduction.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "real" + str(index) + '.png', img_byte_arr.getvalue())
                                            index += 1
                                        elif("camera" in file.lower()):
                                            bigboi.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "real" + str(index) + '.png', img_byte_arr.getvalue())
                                            aiproduction.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "fake" + str(index) + '.png', img_byte_arr.getvalue())
                                            index += 1
                                        else:
                                            raise Exception("Unidentified file: " + file)
                                    except:
                                        pass
                                for file in zip3.namelist():
                                    try:
                                        print(index)
                                        ifile = zip3.open(file)
                                        image = Image.open(ifile)
                                        img_byte_arr = BytesIO()
                                        image.save(img_byte_arr, format = "PNG")
                                        img_byte_arr.seek(0)
                                        bigboi.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "fake" + str(index) + '.png', img_byte_arr.getvalue())
                                        aiproduction.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "fake" + str(index) + '.png', img_byte_arr.getvalue())
                                        index += 1
                                    except Exception as e:
                                        pass
                                for file in zip4.namelist():
                                    try:
                                        print(index)
                                        ifile = zip4.open(file)
                                        image = Image.open(ifile)
                                        img_byte_arr = BytesIO()
                                        image.save(img_byte_arr, format = "PNG")
                                        img_byte_arr.seek(0)
                                        bigboi.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "real" + str(index) + '.png', img_byte_arr.getvalue())
                                        realproduction.writestr(str(hashlib.sha256(file.encode()).hexdigest) + "real" + str(index) + '.png', img_byte_arr.getvalue())
                                        index += 1
                                    except Exception as e:
                                        pass
