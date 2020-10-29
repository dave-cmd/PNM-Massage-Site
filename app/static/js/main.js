//SLIDER

//start point or start index

var i = 0
var images = []
var time = 4000

//Images list
images[0] = 'static/images/massage1.jpg'
images[1] = 'static/images/massage2.jpg'
images[2] = 'static/images/massage4.jpg'
images[3] = 'static/images/massage5.jpg'
images[4] = 'static/images/massage7.jpg'
images[5] = 'static/images/massage8.jpg'
images[6] = 'static/images/massage9.jpg'


// Change Image
function changeImg(){
	document.slide.src = images[i];
	document.slide.className = "dimmer";

	// Check If Index Is Under Max
	if(i < images.length - 1){
	  // Add 1 to Index
	  i++; 
	} else { 
		// Reset Back To O
		i = 0;
	}

	// Run function every x seconds
	setTimeout("changeImg()", time);
}

// Run function when page loads
window.onload=changeImg;



window.addEventListener('DOMContentLoaded', function (){
    //Navbar
const toogle_button = document.getElementsByClassName("toogle-menu")[0]
const navbar_links = document.getElementsByClassName("navbar-links")[0]


toogle_button.addEventListener("click", ()=>{
    //adds the active class to navbar-link if not exixts and vice versa
    navbar_links.classList.toggle("active")
})


})