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

# Define the CNN model
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 28 * 28, 512)
        self.fc2 = nn.Linear(512, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 128 * 28 * 28)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Set up data transforms
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Create dataset and split into train and validation sets
dataset = ImageDataset('path/to/real/images', 'path/to/fake/images', transform=transform)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

# Create data loaders
batch_size = 32
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

# Initialize the model, loss function, and optimizer
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = CNN().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


# Training loop
num_epochs = 10
train_losses = []
val_losses = []

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    train_loss = running_loss / len(train_loader)
    train_losses.append(train_loss)

    # Validation
    model.eval()
    val_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    val_loss /= len(val_loader)
    val_losses.append(val_loss)
    accuracy = 100 * correct / total

    print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}, Accuracy: {accuracy:.2f}%')

# Plot training and validation loss
plt.figure(figsize=(10, 5))
plt.plot(range(1, num_epochs+1), train_losses, label='Train Loss')
plt.plot(range(1, num_epochs+1), val_losses, label='Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()

# Save the model
torch.save(model.state_dict(), 'cnn_model.pth')

print("Training complete. Model saved as 'cnn_model.pth'")
