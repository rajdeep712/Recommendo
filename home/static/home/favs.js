const heading = document.querySelector('.heading');
const castName = heading.id;
const box = document.querySelector('.movie-grid');
const movieLoader = document.querySelector('.movie-loader');
page = 1;


function fetchAndAdd(url) {
    fetch(url).then((response) => {
        return response.json();
    }).then((data) => {
        if(data.has_next === false) {
            window.removeEventListener('scroll',handleScroll);
        }
        data.movies.forEach((movie) => {
            const movieHTML = `
            <a href="/home/${movie.code}">
            <article class="movie-card">
            <img
            src="${movie.poster}"
            alt="${movie.title}"
            class="movie-image"
            />
            <div class="movie-card-overlay">
                <div class="movie-info">
                <span>${movie.year}</span>
                <div class="rating">
                <svg width="12" height="13" viewBox="0 0 12 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M11.7214 4.8126C11.7214 4.91082 11.6634 5.01796 11.5474 5.13403L9.1188 7.50457L9.69417 10.8528C9.69863 10.884 9.70086 10.9287 9.70086 10.9867C9.70086 11.0805 9.67745 11.1597 9.63061 11.2244C9.58378 11.2892 9.51576 11.3215 9.42656 11.3215C9.34181 11.3215 9.25261 11.2947 9.15894 11.2412L6.15494 9.66082L3.15093 11.2412C3.05281 11.2947 2.9636 11.3215 2.88332 11.3215C2.78965 11.3215 2.7194 11.2892 2.67257 11.2244C2.62574 11.1597 2.60232 11.0805 2.60232 10.9867C2.60232 10.9599 2.60678 10.9153 2.6157 10.8528L3.19108 7.50457L0.755762 5.13403C0.644255 5.0135 0.588501 4.90635 0.588501 4.8126C0.588501 4.64743 0.713389 4.54475 0.963165 4.50457L4.32176 4.01573L5.82711 0.968855C5.91185 0.785819 6.02113 0.694301 6.15494 0.694301C6.28875 0.694301 6.39802 0.785819 6.48277 0.968855L7.98811 4.01573L11.3467 4.50457C11.5965 4.54475 11.7214 4.64743 11.7214 4.8126Z" fill="#F1F1F1"/>
                </svg>
                <span>${movie.rating}</span>
            </div>
            </div>
            <h3 class="movie-card-title">${movie.title}</h3>
            </div>
            </article>
            </a>
            `
            box.innerHTML += movieHTML;
        })
        movieLoader.style.display = 'none';
    });
}

document.addEventListener('DOMContentLoaded',() => {
    movieLoader.style.display = 'block';
    const url = `/home/movies/?name=${encodeURIComponent(castName)}&page=${page}`
    page += 1;
    fetchAndAdd(url);
})


function handleScroll() {
    if(window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
        movieLoader.style.display = 'block';
        const url = `/home/movies/?name=${encodeURIComponent(castName)}&page=${page}`;
        
        page = page+1;

        fetchAndAdd(url);
    }
}

window.addEventListener('scroll',handleScroll);