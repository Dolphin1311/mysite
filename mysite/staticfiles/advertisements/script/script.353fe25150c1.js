window.addEventListener('load', function(){
    new Glider(document.querySelector('.glider'), {
        slidesToShow: 3,
        slidesToScroll: 3,
        draggable: true,
        dots: '#dots',
        arrows:{
            prev: '.catalog-button-prev',
            next: '.catalog-button-next'
        }
    })
  });