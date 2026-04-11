// ==================== HEALTH CARE SYSTEM - JAVASCRIPT ==================== //

document.addEventListener('DOMContentLoaded', function() {
    console.log('Health Care System loaded successfully');
    
    // Initialize all features
    initNavigation();
    initFormHandling();
    initAnimations();
    initModals();
});

// ==================== NAVIGATION ==================== //
function initNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

// ==================== FORM HANDLING ==================== //
function initFormHandling() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    highlightInvalidField(input);
                } else {
                    removeInvalidHighlight(input);
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill all required fields', 'error');
            }
        });
    });
}

function highlightInvalidField(field) {
    field.style.borderColor = '#f44336';
    field.style.boxShadow = '0 0 0 3px rgba(244, 67, 54, 0.1)';
}

function removeInvalidHighlight(field) {
    field.style.borderColor = '#e0e0e0';
    field.style.boxShadow = 'none';
}

// ==================== ANIMATIONS ==================== //
function initAnimations() {
    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe service cards, doctor cards, medicine cards
    document.querySelectorAll('.service-card, .doctor-card, .medicine-card, .blood-card').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
}

// ==================== MODALS ==================== //
function initModals() {
    // Close modal when clicking outside
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal-overlay')) {
            closeModal(e.target.id);
        }
    });
    
    // Close modal on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (modal.style.display === 'block') {
                    modal.style.display = 'none';
                }
            });
        }
    });
}

// ==================== NOTIFICATIONS ==================== //
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
        <span>${message}</span>
    `;
    
    const container = document.body;
    container.insertBefore(notification, container.firstChild);
    
    // Auto-remove notification after 5 seconds
    setTimeout(() => {
        notification.style.animation = 'slideUp 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// ==================== BOOKING FUNCTIONALITY ==================== //
function bookAppointment(doctorId) {
    if (!confirm('Proceed to book appointment with this doctor?')) {
        return;
    }
    
    window.location.href = `/book/?doctor=${doctorId}`;
}

// ==================== MEDICINE ORDERING ==================== //
function orderMedicine(medicineId) {
    const button = event.target;
    
    if (button.disabled) {
        showNotification('This medicine is out of stock', 'error');
        return;
    }
    
    // Show loading state
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    button.disabled = true;
    
    // Simulate order processing
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> Order Placed!';
        showNotification('Medicine order placed successfully!', 'success');
        
        // Reset button after 3 seconds
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 3000);
    }, 1500);
}

// ==================== BLOOD REQUEST ==================== //
function requestBlood(bloodGroup) {
    const button = event.target;
    
    if (button.disabled) {
        showNotification('This blood group is not available', 'error');
        return;
    }
    
    const message = `Emergency blood request for group ${bloodGroup}. Your request has been registered. Our team will contact you shortly.`;
    
    // Show loading state
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fas fa-phone"></i> Contacting...';
    button.disabled = true;
    
    // Simulate request processing
    setTimeout(() => {
        button.innerHTML = '<i class="fas fa-check"></i> Request Sent!';
        showNotification(message, 'success');
        
        // Reset button after 3 seconds
        setTimeout(() => {
            button.innerHTML = originalText;
            button.disabled = false;
        }, 3000);
    }, 1500);
}

// ==================== PASSWORD VALIDATION ==================== //
function validatePasswordMatch() {
    const password = document.getElementById('password');
    const confirmPassword = document.getElementById('confirm_password');
    
    if (password && confirmPassword) {
        confirmPassword.addEventListener('change', function() {
            if (password.value !== confirmPassword.value) {
                highlightInvalidField(confirmPassword);
                confirmPassword.title = 'Passwords do not match';
            } else {
                removeInvalidHighlight(confirmPassword);
                confirmPassword.title = '';
            }
        });
    }
}

// Call on page load
validatePasswordMatch();

// ==================== SMOOTH SCROLLING ==================== //
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ==================== UTILITY FUNCTIONS ==================== //
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'block';
    }
}

// Add smooth page transitions
window.addEventListener('beforeunload', function() {
    document.body.style.opacity = '0.9';
});

window.addEventListener('load', function() {
    document.body.style.opacity = '1';
});

// ==================== DEBUG MODE ==================== //
function enableDebugMode() {
    window.debugMode = true;
    console.log('Debug mode enabled. Healthcare System initialized.');
    console.log('Available functions:');
    console.log('- bookAppointment(doctorId)');
    console.log('- orderMedicine(medicineId)');
    console.log('- requestBlood(bloodGroup)');
    console.log('- showNotification(message, type)');
}

// Uncomment the line below to enable debug mode
// enableDebugMode();

// ==================== REGISTER PAGE MEDIA CARD ==================== //
document.addEventListener('DOMContentLoaded', function() {
    try {
        initRegisterMediaCard();
    } catch (e) {
        // ignore if element not present
    }
});

function initRegisterMediaCard() {
    const card = document.getElementById('register-media-card');
    if (!card) return;

    const inner = card.querySelector('.media-inner');
    const video = card.querySelector('.media-video');

    // Toggle flip on click/tap (keep video playing always)
    card.addEventListener('click', function(e) {
        if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON') return;
        card.classList.toggle('is-flipped');
    });

    // Ensure video attempts to autoplay (muted videos are allowed to autoplay in most browsers)
    if (video) {
        // try to play on load
        video.play().catch(()=>{});
        // if user taps the video, toggle play/pause without stopping flip
        video.addEventListener('click', function(e) {
            e.stopPropagation();
            if (video.paused) video.play(); else video.pause();
        });
    }
}
