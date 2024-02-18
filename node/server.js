const Tesseract = require('tesseract.js');

const imagePath = './image/image222.jpeg'; // The path to your image

Tesseract.recognize(
    imagePath,
    'eng', // Specify the language
    {
        logger: m => console.log(m) // Log progress messages
    }
).then(({ data: { text } }) => {
    console.log("Raw OCR Output:", text); // Output the raw recognized text

    // Use a regular expression to find temperature readings
    const tempRegex = /\b\d{2}\.\d°C\b/g;
    const temperatures = text.match(tempRegex);

    if (temperatures) {
        console.log("Extracted Temperatures:", temperatures);
    } else {
        console.log("No temperatures found.");
    }
}).catch(error => {
    console.error(error);
});
