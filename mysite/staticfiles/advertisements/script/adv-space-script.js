function showDeleteDiv(){
    delete_div = document.getElementsByClassName('delete-div')[0];
    delete_div.style.display = 'block';

    gray_div = document.getElementsByClassName('gray-screen')[0];
    gray_div.style.display = 'block'
}

function hideDeleteDiv(){
    delete_div = document.getElementsByClassName('delete-div')[0];
    delete_div.style.display = 'none';

    gray_div = document.getElementsByClassName('gray-screen')[0];
    gray_div.style.display = 'none'
}

var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
    showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
    showSlides(slideIndex = n);
}

function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("adv-space-image");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
}