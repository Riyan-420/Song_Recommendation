document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('questionnaire-form');
    const progressBar = document.getElementById('progress-bar');
    const questions = document.querySelectorAll('.question');
    
    // Calculate progress when radio buttons are clicked
    form.addEventListener('change', function() {
        const totalQuestions = questions.length;
        let answeredQuestions = 0;
        
        // Count how many questions have been answered
        questions.forEach(question => {
            const radioInputs = question.querySelectorAll('input[type="radio"]');
            const selectInputs = question.querySelectorAll('select');
            
            // Check if any radio button in this question is checked
            let questionAnswered = false;
            
            radioInputs.forEach(input => {
                if (input.checked) {
                    questionAnswered = true;
                }
            });
            
            // Check if any select in this question has a value
            selectInputs.forEach(select => {
                if (select.value) {
                    questionAnswered = true;
                }
            });
            
            if (questionAnswered) {
                answeredQuestions++;
            }
        });
        
        // Update progress bar
        const progressPercentage = (answeredQuestions / totalQuestions) * 100;
        progressBar.style.width = progressPercentage + '%';
    });
});