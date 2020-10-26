window.addEventListener('DOMContentLoaded', function (){
    //Navbar
const toogle_button = document.getElementsByClassName("toogle-menu")[0]
const navbar_links = document.getElementsByClassName("navbar-links")[0]


toogle_button.addEventListener("click", ()=>{
    //adds the active class to navbar-link if not exixts and vice versa
    navbar_links.classList.toggle("active")
})



})