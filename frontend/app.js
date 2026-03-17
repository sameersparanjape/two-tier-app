async function fetchNumber() {
    const numEl = document.getElementById('number');
    const loadEl = document.getElementById('loading');
    const errEl = document.getElementById('error');
    const btn = document.getElementById('refresh');

    btn.disabled = true;
    loadEl.classList.remove('d-none');
    errEl.classList.add('d-none');
    numEl.textContent = '';

    try {
        const res = await fetch('/api/random');
        if (!res.ok) {
            throw new Error('Error: HTTP ' + res.status);
        }
        const data = await res.json();
        numEl.textContent = data.number;
    } catch (e) {
        errEl.textContent = e.message.includes('HTTP') ? e.message : 'Service unavailable';
        errEl.classList.remove('d-none');
    } finally {
        loadEl.classList.add('d-none');
        btn.disabled = false;
    }
}

fetchNumber();
