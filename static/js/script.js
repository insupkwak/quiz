function toggleScores() {
    const scoresTable = document.getElementById('scores-table');
    if (scoresTable.classList.contains('hidden')) {
        fetchScores();
    } else {
        scoresTable.classList.add('hidden');
    }
}

function fetchScores() {
    fetch("/get_scores")
        .then(response => response.json())
        .then(data => {
            const scoresBody = document.getElementById('scores-body');
            scoresBody.innerHTML = '';
            data.forEach(score => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${score.rank}</td><td>${score.player_name}</td><td>${score.score}</td>`;
                scoresBody.appendChild(row);
            });
            document.getElementById('scores-table').classList.remove('hidden');
        })
        .catch(error => console.error('Error fetching scores:', error));
}
