
document.addEventListener('DOMContentLoaded', function() {
  
  function goToLoginIfNeeded() {
    // Find the Brochure button
    const brochureBtn = document.querySelector('.request-brochure-btn"');
    
    // If no button found, safely skip
    if (!brochureBtn) return;
    
    // Get the button text (trim spaces & lowercase)
    const text = brochureBtn.textContent.trim().toLowerCase();
    
    // ✅ Only redirect if text is NOT "download brochure"
    if (text !== 'download brochure') {
      window.location.href = "{% url 'login' %}";  // Django login URL
    }
  }

  // ⏱️ Run every 2 minutes (120,000 ms)
  setInterval(goToLoginIfNeeded, 2 * 60 * 1000);

});

