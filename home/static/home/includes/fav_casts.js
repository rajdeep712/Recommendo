const castGrid = document.querySelector('.coverlay-cast-grid');
const castContainer = document.querySelector('.coverlay-container-outer');
const successDiv = document.querySelector('.success');

successDiv.style.display = 'none';
document.body.style.overflow = 'hidden';

const url = '/home/getcasts/';
fetch(url).then(response => {
    return response.json();
}).then(data => {
    casts = data.casts;
    casts.forEach((cast) => {
        cast_html = `
        <div class="coverlay-cast-card" data-cast-id="${cast.id}" onclick="toggleSelection(this)">
          <img
            class="coverlay-cast-image"
            src="${cast.image_url}"
            alt="${cast.name}."
          />
          <div class="coverlay-cast-info">
            <h2 class="coverlay-cast-name">${cast.name}</h2>
          </div>
        </div>
        `;
        
        castGrid.innerHTML += cast_html;
    });
});


selectedCasts = [];


function toggleSelection(card) {
    card.classList.toggle("selected");

    const castId = card.dataset.castId;
    if(!selectedCasts.includes(castId)) {
        selectedCasts.push(castId);
    }
    else{
        const index = selectedCasts.indexOf(castId);
        selectedCasts.splice(index,1);
    }
}
  
function saveSelections() {
    castContainer.style.display = 'none';
    successDiv.style.display = 'block';
    const url = `/home/clear-first-login/?selectedCasts=${encodeURIComponent(selectedCasts.join(','))}`;
    fetch(url).then(response => {
        return response.json();
    }).then(data => {
        if(data.status === 'SUCCESS') {
            window.location.href = '/home'
            return;
        }
    })
}