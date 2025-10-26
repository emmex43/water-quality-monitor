// Handle registration form
document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');
    
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Get form data
            const formData = new FormData(this);
            const userData = {
                name: formData.get('name'),
                email: formData.get('email'),
                password: formData.get('password'),
                address: formData.get('address'),
                telephone: formData.get('telephone'),
                organization: formData.get('organization'),
                role: formData.get('role')
            };

            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="bi bi-arrow-repeat spinner"></i> Creating account...';
            submitBtn.disabled = true;

            try {
                const result = await AuthAPI.register(userData);
                
                if (result.success) {
                    // Show success message
                    alert('Registration successful! Redirecting to login...');
                    
                    // 🚀 REDIRECT TO LOGIN PAGE
                    setTimeout(() => {
                        window.location.href = '/login';
                    }, 1500);
                    
                } else {
                    alert('Error: ' + (result.data.error || 'Registration failed'));
                }
            } catch (error) {
                alert('Network error: ' + error.message);
            } finally {
                // Reset button
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }
        });
    }
});