// Use a set to track processed images
const processedImages = new Set();

function update() {
    // Find all image elements on the page
    const images = document.querySelectorAll('img');

    images.forEach(image => {
        // Check if this image has already been processed
        if (processedImages.has(image)) return;

        // Create a button element
        const button = document.createElement('button');
        button.textContent = 'Show Image';
        button.style.display = 'block';
        button.style.marginBottom = '10px';

        // Hide the image initially
        image.style.display = 'none';

        // Insert the button before the image
        image.parentNode.insertBefore(button, image);

        // When the button is clicked, reveal the image and hide the button
        button.addEventListener('click', () => {
            image.style.display = 'block';
            button.style.display = 'none';
        });

        // Mark this image as processed
        processedImages.add(image);
    });
}

// Run the update function every second
setInterval(update, 1000);
