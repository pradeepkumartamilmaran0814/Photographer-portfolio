/**
 * PORTAVIA FRONTEND JAVASCRIPT
 * Handles AJAX forms, toast notifications, mobile nav, and smooth interactions.
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Toast Notification Helper
    window.showToast = function(message, type = 'success') {
        const existingToast = document.querySelector('.toast-alert');
        if (existingToast) existingToast.remove();

        const toast = document.createElement('div');
        toast.className = `toast-alert toast-${type}`;
        toast.innerHTML = `
            <span style="font-size: 1.2rem;">${type === 'success' ? '✓' : '⚠'}</span>
            <span>${message}</span>
            <button onclick="this.parentElement.remove()" style="background:none; border:none; color:#888; cursor:pointer; margin-left:12px; font-size:1.1rem;">×</button>
        `;
        document.body.appendChild(toast);

        setTimeout(() => {
            if (toast && toast.parentElement) {
                toast.style.transition = 'opacity 0.5s ease';
                toast.style.opacity = '0';
                setTimeout(() => toast.remove(), 500);
            }
        }, 5000);
    };

    // 2. AJAX Contact Form
    const contactForms = document.querySelectorAll('.framer-contact-form');
    contactForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Send Message';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = 'Sending...';
            }

            const formData = new FormData(form);
            try {
                const response = await fetch(form.action || '/contact/submit/', {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: formData
                });

                const data = await response.json();
                if (response.ok && data.status === 'success') {
                    showToast(data.message, 'success');
                    form.reset();
                } else {
                    const errorMsg = data.message || 'Error sending message. Please try again.';
                    showToast(errorMsg, 'error');
                }
            } catch (err) {
                console.error('Contact form submission error:', err);
                showToast('Failed to send message. Please check your network and try again.', 'error');
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnText;
                }
            }
        });
    });

    // 3. AJAX Newsletter Form
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn ? submitBtn.innerHTML : 'Subscribe';
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '...';
            }

            const formData = new FormData(form);
            try {
                const response = await fetch(form.action || '/newsletter/subscribe/', {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: formData
                });

                const data = await response.json();
                if (response.ok && data.status === 'success') {
                    showToast(data.message, 'success');
                    form.reset();
                } else {
                    showToast(data.message || 'Subscription failed.', 'error');
                }
            } catch (err) {
                console.error('Newsletter error:', err);
                showToast('Network error subscribing. Please try again.', 'error');
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }
            }
        });
    });

    // 4. Mobile Navigation Toggle
    const mobileToggle = document.querySelector('.mobile-nav-toggle');
    const navLinks = document.querySelector('.nav-links');
    if (mobileToggle && navLinks) {
        mobileToggle.addEventListener('click', () => {
            const isVisible = navLinks.style.display === 'flex';
            if (isVisible) {
                navLinks.style.display = 'none';
            } else {
                navLinks.style.display = 'flex';
                navLinks.style.flexDirection = 'column';
                navLinks.style.position = 'absolute';
                navLinks.style.top = '70px';
                navLinks.style.left = '20px';
                navLinks.style.right = '20px';
                navLinks.style.background = 'rgba(20, 20, 24, 0.95)';
                navLinks.style.backdropFilter = 'blur(20px)';
                navLinks.style.borderRadius = '16px';
                navLinks.style.padding = '20px';
                navLinks.style.border = '1px solid rgba(255, 255, 255, 0.1)';
            }
        });
    }
});
