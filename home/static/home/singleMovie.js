const favButton = document.querySelector('.favorite-btn')
const trailerBtn = document.querySelector('.trailer-btn');
const closeBtn = document.querySelector('.close-btn');
const trailerOverlay = document.querySelector('.overlay');
const iframe = document.querySelector('.video-frame');
const commentBtn = document.querySelector('.comment-btn');
const commentsList = document.querySelector('.comments-list');
const trashUrl = document.querySelector('.trash-svg').dataset.trashUrl;

function showPopup(message) {
    const popup = document.getElementById('popup');
    popup.textContent = message;
    popup.classList.add('show');
    
    setTimeout(() => {
      popup.classList.remove('show');
    }, 3000);
}
  
function toggleFavourite(button) {
    button.classList.toggle('active');
    const isFavorite = button.classList.contains('active');
    showPopup(isFavorite ? 'Added to favorites' : 'Removed from favorites');
    button.innerHTML = `
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="${isFavorite ? 'currentColor' : 'none'}" stroke="currentColor" stroke-width="2" class="heart-icon">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
        </svg>
        ${isFavorite? 'Remove from favourites' : 'Add to favourites'}
    `;
}


favButton.addEventListener('click' , function() {
    toggleFavourite(this);
    mov_code = this.dataset.code;
    url = `/home/addtofavourites/?mov_code=${mov_code}`;
    fetch(url).then((response) => {
        return response.json();
    }).then((data) => {
        if(data.status === "success") {
            return;
        }
    })
})

trailerBtn.addEventListener('click', () => {
    trailerOverlay.style.display = 'block';
    document.body.style.overflow = 'hidden';

    closeBtn.addEventListener('click', () => {
        trailerOverlay.style.display = 'none';
        document.body.style.overflow = 'auto';
        iframe.src = iframe.src;
    })
})



commentBtn.addEventListener('click' , () => {
    const category = commentBtn.parentElement.querySelector('.category').value;
    const code = commentBtn.parentElement.querySelector('.code').value;
    const comment = commentBtn.parentElement.querySelector('.comment-input').value;
    const input = commentBtn.parentElement.querySelector('.comment-input')

    commentBtn.parentElement.querySelector('.comment-input').value = '';
    commentBtn.style.cursor = "not-allowed";
    commentBtn.disabled = true;
    input.disabled = true;
    input.style.cursor = "not-allowed";

    showPopup("Your words now grace the film's legacy");

    const url = `/home/toggleComment/?category=${encodeURIComponent(category)}&code=${code}&comment=${encodeURIComponent(comment)}`;
    fetch(url).then((response) => {
        return response.json();
    }).then((data) => {
        comment_html = `
            <div class="comment">
              <div class="upper">
                <div class="comment-header">
                  <div class="comment-avatar">${data.avatar}</div>
                  <span class="comment-author">${data.name}</span>
                </div>
                
                <div>
                  <input type="hidden" name="category" value="delete" class="category">
                  <input type="hidden" name="code" value=${data.code} class="code">
                  <input type="hidden" name="comment-id" value=${data.comment_id} class="comment-id">
                  <button type="submit" style="background:transparent;border:none;" class="delete-btn">
                    <img src="${trashUrl}" alt="" height="25px" width="25px">
                  </button>
                </div>

              </div>
              <div class="line"></div>
              <p>${data.comment}</p>
            </div>
        `

        commentsList.innerHTML = comment_html + commentsList.innerHTML;
        deleteBtnsListener();
    })
    commentBtn.style.cursor = 'default';
    commentBtn.disabled = false;
    input.disabled = false;
    input.style.cursor = 'default';
})

function deleteBtnsListener() {
    const deleteBtns = Array.from(document.querySelectorAll('.delete-btn'));
    deleteBtns.forEach((deleteBtn) => {
        deleteBtn.addEventListener('click', function() {
            const category = this.parentElement.querySelector('.category').value;
            const commentId = this.parentElement.querySelector('.comment-id').value;
            const url = `/home/toggleComment/?category=${encodeURIComponent(category)}&commentId=${encodeURIComponent(commentId)}`;
            showPopup("Your comment has been gracefully removed");
            fetch(url).then(response => response.json()).then((data) => {
                if(data.status === "SUCCESS") {
                    return;
                }
            })
            this.parentElement.parentElement.parentElement.remove();
        })
    })
}

deleteBtnsListener();
