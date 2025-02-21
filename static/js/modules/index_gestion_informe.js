function filterPatients() {
    const input = document.getElementById('search-input').value.toLowerCase();
    const cards = document.querySelectorAll('.patient-card');

    cards.forEach(card => {
      const name = card.getAttribute('data-name').toLowerCase();
      const dni = card.getAttribute('data-dni').toLowerCase();

      card.style.display = (name.includes(input) || dni.includes(input)) ? 'block' : 'none';
    });
  }