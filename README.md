# Real Versus Fake

## Overview
**Real Versus Fake** is a project designed to detect whether an image is real or fake. It includes a Chrome extension that works seamlessly in the background to analyze all images you view on the internet. The extension automatically sends these images to AI models, which determine the authenticity of each image.

## Features
- **Chrome Extension:** Automatically detects and collects images as you browse the internet, requiring no user input.
- **AI-Powered Detection:** Uses advanced AI models to determine whether an image is real or fake.
- **Real-Time Feedback:** Provides instant feedback on the authenticity of images as you browse.

## Installation

### Chrome Extension
1. Open Chrome and go to chrome://extensions/.
2. Enable Developer Mode.
3. Click on Load unpacked and select the Extension/ directory from the cloned repository.

### Backend
1. Clone the repository:
   git clone https://github.com/pymaster3119/real-versus-fake.git
2. Install dependencies:
   pip install -r requirements.txt
3. Start the AI model server:
   python ExtentionServer.py

## How It Works
- The Chrome extension runs in the background, detecting all images displayed on the web pages you visit.
- These images are sent to the AI model running on the backend, which then analyzes the content of the image.
- Based on factors such as noise patterns, inconsistencies, and known manipulation techniques, the model determines if the image is real or artificially generated.

## Usage
Once installed and activated, the Chrome extension will automatically analyze all images without any manual intervention. It works silently in the background, providing real-time results.

## AI Model
The AI models are trained using a dataset of real and fake images, leveraging deep learning techniques such as convolutional neural networks (CNNs) for image classification.
