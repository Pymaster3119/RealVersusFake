import os
import pandas as pd
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms
from PIL import Image
import zipfile
from io import BytesIO
from PIL import Image
print("Hi")

# Define the dataset class
class ImageDataset(Dataset):
    def __init__(self, real_dir, fake_dir, transform=None):
        imagelist = import_images("/Users/aditya/Desktop/Training Dataset.zip")
        self.real_images = imagelist[0]
        self.fake_images = imagelist[1]
        self.all_images = self.real_images + self.fake_images
        self.labels = [1] * len(self.real_images) + [0] * len(self.fake_images)
        self.transform = transform

    def len(self):
        return len(self.all_images)

    def getitem(self, idx):
        img_path = self.all_images[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label


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


realimgs, fakeimgs = import_images()
print(len(realimgs))
print(len(fakeimgs))