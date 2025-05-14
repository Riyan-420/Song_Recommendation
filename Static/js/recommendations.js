document.addEventListener('DOMContentLoaded', function() {
    // Star rating functionality
    const stars = document.querySelectorAll('.star');
    
    stars.forEach(star => {
        star.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            const recId = this.getAttribute('data-rec-id');
            
            // Set visual state
            const starsForThisRec = document.querySelectorAll(`.star[data-rec-id="${recId}"]`);
            starsForThisRec.forEach(s => {
                if (parseInt(s.getAttribute('data-value')) <= value) {
                    s.classList.add('active');
                } else {
                    s.classList.remove('active');
                }
            });
            
            // Send rating to server
            fetch(`/recommendations/rate/${recId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `rating=${value}`
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    console.error('Error rating:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});