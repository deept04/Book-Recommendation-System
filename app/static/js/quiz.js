// quiz.js

document.getElementById('quiz-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    // Retrieve selected answers for each question
    const answers = {
        q1: document.querySelector('input[name="q1"]:checked').value,
        q2: document.querySelector('input[name="q2"]:checked').value,
        q3: document.querySelector('input[name="q3"]:checked').value,
        q4: document.querySelector('input[name="q4"]:checked').value,
        q5: document.querySelector('input[name="q5"]:checked').value,
        q6: document.querySelector('input[name="q6"]:checked').value,
        q7: document.querySelector('input[name="q7"]:checked').value,
        q8: document.querySelector('input[name="q8"]:checked').value,
        q9: document.querySelector('input[name="q9"]:checked').value,
        q10: document.querySelector('input[name="q10"]:checked').value
    };

    // Calculate the result (example calculation)
    const result = Object.values(answers).reduce((total, answer) => total + parseInt(answer), 0);

    // The Personality according to points calculated
    if (result >= 45) {
        personality = "You have a highly adaptable and outgoing personality!";
    } else if (result >= 35){
        personality = "You have a balanced and sociable personality!";
    } else if (result >= 25) {
        personality = "You have a thoughtful and analytical personality!";
    } else if (result >= 15) {
        personality = "You have a cautious and measured personality!";
    } else {
        personality = "You have an inquisitive and adaptable personality!";
    }

    // Display the result on the UI
    document.getElementById('result').innerText = `Your Personality is: ${personality}`;

     // Send results to the backend
    fetch('/recommend-books', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ personality: personality })
    })
    .then(response => response.json())
    .then(books => displayBooks(books))
    .catch(error => console.error('Error fetching books:', error));
});

function displayBooks(books) {
    const booksContainer = document.createElement('div');

    // Generate HTML for each book
    books.forEach(book => {
        const bookElement = document.createElement('img');
        bookElement.src = book.image
        bookElement.alt = book.title
        bookElement.class="book-cover"
        booksContainer.appendChild(bookElement);
    });

    // Display the list of books on the UI
    const resultContainer = document.getElementById('books-images');
    resultContainer.appendChild(booksContainer);
}
