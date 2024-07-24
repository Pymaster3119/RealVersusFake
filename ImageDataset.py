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
import re
from tqdm import tqdm

# Import zip file
def import_images(paths):
    realimgs = []
    fakeimgs = []
    for path in paths:
        print(path)
        with zipfile.ZipFile(path, 'r') as zip:
            for file in tqdm(zip.namelist(), desc="Downloading files"):
                if "real" in file.lower():
                        realimgs.append(file + "\:FLAG:/" + path)
                if "fake" in file.lower():
                    try:
                        fakeimgs.append(file + "\:FLAG:/" + path)
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
        self.pattern = r'^(.*)\\:FLAG:/([^/]*)$'
        self.zips = {"TrainingDataset1.zip":zipfile.ZipFile("TrainingDataset1.zip", "r"),"TrainingDataset2.zip":zipfile.ZipFile("TrainingDataset2.zip", "r"),"TrainingDataset3.zip":zipfile.ZipFile("TrainingDataset3.zip", "r")}

    def __len__(self):
        return len(self.all_images)

    def __getitem__(self, idx):
        img_path = self.all_images[idx]
        match = re.match(self.pattern, img_path)
        if match:
            zip = self.zips[match.group(2)]
            file = zip.open(match.group(1))
            image_data = file.read()
            img = Image.open(BytesIO(image_data))
            img = img.convert("RGB")
            label = self.labels[idx]

            if self.transform:
                img = self.transform(img)
            return img, label

if __name__ == "__main__":
    #Run ONLY once!

    realimgs, fakeimgs = import_images(["TrainingDataset1.zip", "TrainingDataset2.zip", "TrainingDataset3.zip"])
    with open("realimgs", "wb") as txt: 
        pickle.dump(realimgs, txt)
    with open("fakeimgs", "wb") as txt: 
        pickle.dump(fakeimgs, txt)
    print(len(realimgs), len(fakeimgs))