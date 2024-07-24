const processedImages = new Set();

// Function to convert image to data URL
function getImageDataURL(img) {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0);
    
    return canvas.toDataURL('image/png');
}

async function sendImageToServer(dataURL) {
    const response = await fetch('/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ image: dataURL })
    });
    
    const result = await response.json();
    console.log(result);
}

sendImageToServer();


function processImage(image) {
    if (processedImages.has(image)) return;
    data = getImageDataURL(image);
    sendImageToServer(data);
    // Create a button element
    const button = document.createElement('button');
    button.innerHTML = '<h1>This image looks AI generated<\h1><p><br><br>Show text anyway<\p>';
    button.style.position = 'absolute';
    button.style.backgroundColor = '#007bff'; // Blue background
    button.style.color = 'white'; // White text
    button.style.border = 'none';
    button.style.padding = '0'; // Remove padding
    button.style.fontSize = '16px'; // Adjust font size
    button.style.cursor = 'pointer';
    button.style.textAlign = 'center';
    button.style.zIndex = '1'; // Ensure button is on top of the image

    // Style the button to fill the image space
    image.style.position = 'relative'; // Ensure the parent container is positioned
    button.style.width = `${image.width}px`; // Match button width to image width
    button.style.height = `${image.height}px`; // Match button height to image height

    // Hide the image initially
    image.style.display = 'none';

    // Insert the button before the image
    image.parentNode.insertBefore(button, image);

    // Check if the image is inside a link
    const link = image.closest('a');
    if (link) {
        // Prevent the default action of the link
        button.addEventListener('click', (event) => {
            event.preventDefault();
            event.stopPropagation(); // Stop click event from bubbling up
            image.style.display = 'block';
            button.style.display = 'none';
        });

        // Prevent the link from being followed
        link.addEventListener('click', (event) => {
            event.preventDefault();
        }, { capture: true }); // Use capture phase to catch early
    } else {
        // If no link, just reveal the image
        button.addEventListener('click', () => {
            image.style.display = 'block';
            button.style.display = 'none';
        });
    }

    // Mark this image as processed
    processedImages.add(image);

    // Observe changes in the image size
    const observer = new MutationObserver(() => {
        button.style.width = `${image.width}px`;
        button.style.height = `${image.height}px`;
    });

    observer.observe(image, { attributes: true, attributeFilter: ['width', 'height'] });
}

function update() {
    // Find all image elements on the page
    const images = document.querySelectorAll('img');
    images.forEach(processImage);
}

// Initial run
update();

// Observe the document for added images
const observer = new MutationObserver(() => {
    update();
});

observer.observe(document.body, {
    childList: true,
    subtree: true
});
