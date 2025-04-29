const gif = document.querySelector('.gif');
const instruction = document.querySelector('.instruction');

setTimeout(() => {
    gif.style.display = 'none';
    instruction.classList.add('animate');
},1500)