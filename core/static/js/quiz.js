document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('quiz-form');
    const timerElement = document.getElementById('timer');
    
    // Set quiz duration (20 minutes)
    const quizDuration = 20 * 60; // in seconds
    let timeLeft = quizDuration;
    
    // Start the timer
    const timer = setInterval(function() {
        timeLeft--;
        
        // Update timer display
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `Time remaining: ${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        // Check if time is up
        if (timeLeft <= 0) {
            clearInterval(timer);
            form.submit();
        }
    }, 1000);
    
    // Disable form submission while submitting to prevent double submissions
    form.addEventListener('submit', function() {
        const submitButton = form.querySelector('button[type="submit"]');
        submitButton.disabled = true;
        
        // Disable all radio inputs
        const radioInputs = form.querySelectorAll('input[type="radio"]');
        radioInputs.forEach(input => input.disabled = true);
        
        // Stop the timer
        clearInterval(timer);
    });
});
