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
import pickle

# Import zip file
def import_images(paths):
    realimgs = []
    fakeimgs = []
    for path in paths:
        with zipfile.ZipFile(path, 'r') as zip:
            for file in zip.namelist():
                if "real" in file.lower():
                        try:
                            image_file = zip.open(file)
                            image_data = image_file.read()
                            image = Image.open(BytesIO(image_data))
                            image = image.crop((0,0,image.size[0]-98, image.size[1]-20)).resize((500,500))
                            realimgs.append(image)
                        except:
                            pass
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

# Define the dataset class
class ImageDataset(Dataset):
    def __init__(self, real_dir, fake_dir, transform=None):
        with open("realimgs", "rb") as txt: 
            self.real_images = pickle.load(txt)
        with open("fakeimgs", "rb") as txt: 
            self.fake_images = pickle.load(txt)
        self.all_images = self.real_images + self.fake_images
        self.labels = [1] * len(self.real_images) + [0] * len(self.fake_images)
        self.transform = transform

    def __len__(self):
        return len(self.all_images)

    def __getitem__(self, idx):
        img_path = self.all_images[idx].convert('RGB')
        label = self.labels[idx]

        if self.transform:
            img_path = self.transform(img_path)

        return img_path, label

if __name__ == "__main__":
    #Run ONLY once!

    realimgs, fakeimgs = import_images(["TrainingDataset1.zip", "TrainingDataset1.zip", "TrainingDataset3.zip"])
    with open("realimgs", "wb") as txt: 
        pickle.dump(realimgs, txt)
    with open("fakeimgs", "wb") as txt: 
        pickle.dump(fakeimgs, txt)
    print(os.path.getsize("realimgs"))
    print(os.path.getsize("fakeimgs"))