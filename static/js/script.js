// Alterar a tela de registro para o modo dark

const mode = document.getElementById('mode_icon');

mode.addEventListener('click', () => {
   if (mode.classList.contains('fa-solid fa-moon')) {
       mode.classList.remove('fa-solid fa-moon');
       mode.classList.add('fa-solid fa-sun');
   }
});