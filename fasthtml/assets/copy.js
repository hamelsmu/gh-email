function copyToClipboard(event, email) {
    event.preventDefault();
    navigator.clipboard.writeText(email)
      .then(() => {
        const btn = event.target.closest('.copy-btn');
        btn.classList.add('copied');
        const textSpan = btn.querySelector('.button-text');
        textSpan.textContent = 'Copied';
                  
        const icon = btn.querySelector('i');
        icon.classList = 'fas fa-check green-check';
                  
        setTimeout(() => {
          btn.classList.remove('copied');
          textSpan.textContent = 'Copy';
          icon.classList = 'fas fa-copy';
        }, 1500);
      })
      .catch(err => {
        console.error('Failed to copy text: ', err);
      });
}
