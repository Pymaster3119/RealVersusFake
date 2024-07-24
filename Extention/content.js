const processedImages = new Set();

function processImage(image) {
    if (processedImages.has(image)) return;

    // Create a button element
    const button = document.createElement('button');
    button.innerHTML = 'This image looks AI generated\nShow text anyway';
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
