const passwordInput = document.querySelector('.password-input');
const eyeIcon = document.getElementById('eyeIcon');
const info = document.getElementById('info');

const div = document.querySelector('.hide-password');

div.addEventListener('click', () => {
    if(info.innerText === 'Show') {
        passwordInput.type = 'text';
        eyeIcon.classList.remove('ti-eye-off');
        eyeIcon.classList.add('ti-eye');
        info.innerText = 'Hide';
    }
    else{
        passwordInput.type = 'password';
        eyeIcon.classList.remove('ti-eye');
        eyeIcon.classList.add('ti-eye-off');
        info.innerText = 'Show';
    }
})