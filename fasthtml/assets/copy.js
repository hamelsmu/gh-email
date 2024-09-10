function copyToClipboard(event, email) {
    halt(event);
    navigator.clipboard.writeText(email)
      .then(() => {
        const btn = me('.copy-btn').classAdd('copied');
        const textSpan = me('.button-text').textContent('Copied');                  
        const icon = btn('i').classAdd('fas fa-check green-check');
                  
        sleep(1500, () => {
          btn.classRemove('copied');
          textSpan.textContent = 'Copy';
          icon.classList = 'fas fa-copy';
        });
      })
      .catch(err => {console.error('Failed to copy text: ', err)});
}
