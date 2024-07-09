ws.onmessage = function(event) {
    if (event.data === 'show') {
        document.getElementById('throbber').classList.remove('hidden');

    } else if (event.data === 'hide') {
        document.getElementById('throbber').classList.add('hidden');
    }
};