const ctx = document.getElementById('scoreChart');
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Skill Match', 'BERT Match', 'Final Score'],
        datasets: [{
            data: [skillMatch, bertScore, finalScore]
        }]
    }
});
