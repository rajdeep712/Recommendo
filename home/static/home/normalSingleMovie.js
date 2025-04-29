const trailerBtn = document.querySelector('.trailer-btn');
const closeBtn = document.querySelector('.close-btn');
const trailerOverlay = document.querySelector('.overlay');
const iframe = document.querySelector('.video-frame');




trailerBtn.addEventListener('click', () => {
    trailerOverlay.style.display = 'block';
    document.body.style.overflow = 'hidden';

    closeBtn.addEventListener('click', () => {
        trailerOverlay.style.display = 'none';
        document.body.style.overflow = 'auto';
        iframe.src = iframe.src;
    })
})