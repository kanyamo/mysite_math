const open_btn = document.getElementById('open-button');
const navbar_list = document.getElementById('navbar-list');
const help_text = document.getElementById('help-text');
open_btn.addEventListener('click', ()=>{
    navbar_list.classList.toggle('navbar-list-hidden');
    open_btn.classList.toggle('active');
});