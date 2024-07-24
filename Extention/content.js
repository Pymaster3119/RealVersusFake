update = function()
{
    // Find all image elements on the page
    const images = document.querySelectorAll('img');

    // Iterate through each image and remove it
    images.forEach(image => {
        image.remove();
    });
}
setInterval(update,1000);