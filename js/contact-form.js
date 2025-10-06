// Contact Form Handler
(function() {
    'use strict';

    const form = document.getElementById('contact-form');
    const formReply = document.querySelector('.form__reply');
    
    if (!form) return;

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });
        
        // Disable submit button
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.querySelector('.btn-caption').textContent;
        submitBtn.disabled = true;
        submitBtn.querySelector('.btn-caption').textContent = 'Sending...';
        
        try {
            const response = await fetch('/send-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                // Show success message
                formReply.classList.add('active');
                form.reset();
                
                // Hide success message after 5 seconds
                setTimeout(() => {
                    formReply.classList.remove('active');
                }, 5000);
            } else {
                // Show error message
                alert('Error: ' + result.message);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to send message. Please try again later.');
        } finally {
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-caption').textContent = originalBtnText;
        }
    });
})();
