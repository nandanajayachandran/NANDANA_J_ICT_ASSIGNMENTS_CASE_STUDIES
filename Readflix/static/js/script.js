//TOGGLE

function toggleDarkMode() {
  const body = document.body;

  const toggle = document.querySelector('.toggle');
  const toggleBall = document.querySelector('.toggle-ball');

  body.classList.toggle('dark-mode');
  toggle.classList.toggle('active');
  toggleBall.classList.toggle('active');
}

// Target both buttons using a single function
function openLinkInNewTab(buttonId, linkUrl) {
  const button = document.getElementById(buttonId);
  button.addEventListener('click', function () {
    window.open(linkUrl, '_blank', 'noopener'); // Enhanced security with 'noopener'
  });
}

// Call the function for each button-link pair
openLinkInNewTab('top-book-button', 'https://www.goodreads.com/en/book/show/62039166');
openLinkInNewTab('top-movie-button', 'https://www.amazon.com/Oppenheimer-Cillian-Murphy/dp/B0CKRXGGQB');



// Target all "READ" buttons
const readButtons = document.querySelectorAll('.book-list-item-button');

// Array to store book links (replace with actual links)
const bookLinks = [
  'https://www.goodreads.com/en/book/show/60784729',
  'https://www.goodreads.com/en/book/show/60784757',
  'https://www.goodreads.com/en/book/show/121561903',
  'https://www.goodreads.com/en/book/show/77920745'
];

// Attach click event listeners to each button
readButtons.forEach((button, index) => {
  button.addEventListener('click', function () {
    // Open the corresponding book link in a new tab
    window.open(bookLinks[index], '_blank', 'noopener');
  });
});

// Target all "WATCH" buttons
const watchButtons = document.querySelectorAll('.movie-list-item-button');

// Array to store movie links (replace with actual links)
const movieLinks = [
  'https://en.wikipedia.org/wiki/Poor_Things_(film)',
  'https://www.hotstar.com/in/movies/guardians-of-the-galaxy-vol-3/1260143699',
  'https://www.primevideo.com/dp/amzn1.dv.gti.bab3987b-0cf1-466e-9fe6-50f208bee6f0?autoplay=0&ref_=atv_cf_strg_wb',
  'https://www.primevideo.com/dp/amzn1.dv.gti.17f2bd91-afd8-4ae8-8dbc-9c49066e771c?autoplay=0&ref_=atv_cf_strg_wb'
];

// Attach click event listeners to each button
watchButtons.forEach((button, index) => {
  button.addEventListener('click', function () {
    // Open the corresponding movie link in a new tab
    window.open(movieLinks[index], '_blank', 'noopener');
  });
});


// JavaScript code to handle "Read More" button click
var buttons = document.querySelectorAll('.card_btn');

buttons.forEach(function (button) {
  button.addEventListener('click', function () {
    var cardContent = this.closest('.card_content');
    var paragraph = cardContent.querySelector('.additional_text');

    if (!paragraph) {
      // Create and append the paragraph if it doesn't exist
      paragraph = document.createElement('p');
      paragraph.className = 'additional_text';
      paragraph.textContent = 'Additional information about the movie. Lorem ipsum dolor sit amet, consectetur adipiscing elit.';
      cardContent.appendChild(paragraph);
    } else {
      // Toggle the visibility of the paragraph
      paragraph.style.display = (paragraph.style.display === 'none' || !paragraph.style.display) ? 'block' : 'none';
    }
  });
});


