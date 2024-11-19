document.querySelector('.search-bar').onsubmit = function(event) {
    event.preventDefault();
    const query = document.querySelector('.search-input').value;
    fetch(`/api/search?q=${query}`)
        .then(response => response.json())
        .then(data => {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = ''; // Очищуємо попередні результати
            data.forEach(film => {
                const filmElement = document.createElement('div');
                filmElement.textContent = film.name;
                resultsDiv.appendChild(filmElement);
            });
        })
        .catch(error => console.error('Error:', error));
};
