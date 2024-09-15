async function performSearch() {
    const searchQuery = document.getElementById('searchInput').value;
    const topK = document.getElementById('topK').value;
    const threshold = document.getElementById('threshold').value;
    const resultsDiv = document.getElementById('results');

    if (!searchQuery) {
        alert('Please enter a search query');
        return;
    }

    resultsDiv.innerHTML = 'Searching...';

    try {
        const response = await fetch('http://localhost:8000/search?user_id=test_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: searchQuery,
                top_k: parseInt(topK),
                threshold: parseFloat(threshold)
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        displayResults(data);
    } catch (error) {
        console.error('Error:', error);
        resultsDiv.innerHTML = `An error occurred: ${error.message}`;
    }
}

function displayResults(results) {
    const resultsDiv = document.getElementById('results');
    if (results.length === 0) {
        resultsDiv.innerHTML = 'No results found.';
        return;
    }

    let resultsHtml = '';
    results.forEach((result, index) => {
        resultsHtml += `
            <div class="result-item">
                <h3>Result ${index + 1}</h3>
                <p>${result.content}</p>
                <p>Score: ${result.score.toFixed(4)}</p>
            </div>
        `;
    });

    resultsDiv.innerHTML = resultsHtml;
}
