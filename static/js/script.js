document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Hide previous results
    document.getElementById('resultSection').style.display = 'none';
    document.getElementById('errorSection').style.display = 'none';
    
    // Get form data
    const formData = {
        month: parseInt(document.getElementById('month').value),
        day_of_week: parseInt(document.getElementById('day_of_week').value),
        time_of_day: parseInt(document.getElementById('time_of_day').value),
        is_holiday: parseInt(document.getElementById('is_holiday').value),
        beach_id: parseInt(document.getElementById('beach_id').value),
        registered_volunteers: parseInt(document.getElementById('registered_volunteers').value),
        organizer_rating: parseFloat(document.getElementById('organizer_rating').value)
    };
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok && data.status === 'success') {
            document.getElementById('predictionValue').textContent = Math.round(data.prediction);
            document.getElementById('resultSection').style.display = 'block';
        } else {
            document.getElementById('errorMessage').textContent = data.error || 'An error occurred';
            document.getElementById('errorSection').style.display = 'block';
        }
    } catch (error) {
        document.getElementById('errorMessage').textContent = 'Failed to connect to server';
        document.getElementById('errorSection').style.display = 'block';
    }
});
