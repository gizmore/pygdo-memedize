"use strict";
window.gdo.Memedize = {
    gdo_init: function() {},
};

document.addEventListener('click', function(event) {
    const link = event.target.closest('.memedize-gallery a');
    if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const thumbnail = link.querySelector('img');
    if (!thumbnail || typeof HTMLDialogElement === 'undefined') return;

    const dialog = document.createElement('dialog');
    if (typeof dialog.showModal !== 'function') return;
    event.preventDefault();
    dialog.className = 'memedize-preview';
    dialog.setAttribute('aria-label', thumbnail.alt || 'Meme preview');
    const image = document.createElement('img');
    image.src = link.href;
    image.alt = thumbnail.alt;
    const nav = document.createElement('nav');
    const original = document.createElement('a');
    original.href = link.href;
    original.textContent = 'Original';
    const close = document.createElement('button');
    close.type = 'button';
    close.textContent = '×';
    close.setAttribute('aria-label', 'Close preview');
    close.addEventListener('click', () => dialog.close());
    dialog.addEventListener('click', (e) => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => { dialog.remove(); link.focus(); });
    nav.append(original, close);
    dialog.append(image, nav);
    document.body.append(dialog);
    dialog.showModal();
});
