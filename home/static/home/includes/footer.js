const footerAnimate = Array.from(document.querySelectorAll('.uplift'));

const observer = new IntersectionObserver((entries,observer) => {
    entries.forEach(entry => {
        if(entry.isIntersecting) {
            entry.target.classList.add('visible');

            observer.unobserve(entry.target);
        }
    });
},{
    threshold:0.2
})


footerAnimate.forEach(div => {
    observer.observe(div);
})