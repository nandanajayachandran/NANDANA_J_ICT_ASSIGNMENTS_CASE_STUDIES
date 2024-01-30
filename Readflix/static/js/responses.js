// Function to get bot response based on user input
function getBotResponse(input) {
    const lowercaseInput = input.toLowerCase();

    if (lowercaseInput.includes('hi') || lowercaseInput.includes('hello')) {
        return "Hello there! Choose between movie and book.";
    } else if (lowercaseInput.includes('goodbye') || lowercaseInput.includes('bye')) {
        return "Talk to you later!";
    } else if (lowercaseInput.includes('movie')) {
        displayButtons(['Action Movie', 'Comedy Movie']);
    } else if (lowercaseInput.includes('book')) {
        displayButtons(['Mystery Book', 'Science Fiction Book']);
    } else {
        return "Try asking something else!";
    }
}
