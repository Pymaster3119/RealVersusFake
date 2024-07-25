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
        self.zips = {
            "TrainingDataset1.zip": zipfile.ZipFile("TrainingDataset1.zip", "r"),
            "TrainingDataset2.zip": zipfile.ZipFile("TrainingDataset2.zip", "r"),
            "TrainingDataset3.zip": zipfile.ZipFile("TrainingDataset3.zip", "r")
        }

    def __len__(self):
        return len(self.all_images)

    def __getitem__(self, idx):
        img_path = self.all_images[idx]
        if isinstance(img_path, str):
            match = re.match(self.pattern, img_path)
            if match:
                zipf = self.zips[match.group(2)]
                with zipf.open(match.group(1)) as file:
                    image_data = file.read()
                    img = Image.open(BytesIO(image_data))
                    img = img.convert("RGB")
                    label = self.labels[idx]

                    if self.transform:
                        img = self.transform(img)
                    return img, label
            else:
                return None
        else:
            img = img_path.convert("RGB")
            label = self.labels[idx]
            if self.transform:
                img = self.transform(img)
            return img, label
# Import zip file
def import_images(paths, toMemory):
    realimgs = []
    fakeimgs = []
    for path in paths:
        print(f"Processing path: {path}")
        with zipfile.ZipFile(path, 'r') as zipf:
            for file in zipf.namelist():
                if "real" in file.lower():
                    realimgs.append(file + "\:FLAG:/" + path)
                if "fake" in file.lower():
                    fakeimgs.append(file + "\:FLAG:/" + path)

    for path in toMemory:
        print(f"Processing path to memory: {path}")
        with zipfile.ZipFile(path, 'r') as zipf:
            for file in zipf.namelist():
                if "real" in file.lower():
                    try:
                        with zipf.open(file) as image_file:
                            image_data = image_file.read()
                            image = Image.open(BytesIO(image_data))
                            realimgs.append(image)
                    except Exception as e:
                        print(f"Error processing {file} in {path}: {e}")
                if "fake" in file.lower():
                    try:
                        with zipf.open(file) as image_file:
                            image_data = image_file.read()
                            image = Image.open(BytesIO(image_data))
                            fakeimgs.append(image)
                    except Exception as e:
                        print(f"Error processing {file} in {path}: {e}")
    return (realimgs, fakeimgs)

if __name__ == "__main__":
    # Run ONLY once!
    realimgs, fakeimgs = import_images(["TrainingDataset1.zip", "TrainingDataset2.zip", "TrainingDataset3.zip"], [])
    print("Here")
    with open("realimgs", "wb") as txt:
        pickle.dump(realimgs, txt)
    with open("fakeimgs", "wb") as txt:
        pickle.dump(fakeimgs, txt)
    print(len(realimgs), len(fakeimgs))
