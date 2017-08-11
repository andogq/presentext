var currentSlide = 0;
var lastSlide = 2;

var slideShow = {
     show: function(slideNum) {
          var slide = document.getElementById("slide" + slideNum);
          slide.classList.remove("offScreen");
          slide.classList.add("active");
     },
     hide: function(slideNum) {
          var slide = document.getElementById("slide" + slideNum);
          slide.classList.remove("active");
          slide.classList.add("offScreen");
     },
     next: function() {
          if (currentSlide < lastSlide) {
               slideShow.show(currentSlide + 1);
               slideShow.hide(currentSlide);
               currentSlide += 1;
          }
     },
     prev: function() {
          if (currentSlide > 0) {
               // Shows previous slide
               var prevSlide = document.getElementById("slide" + (currentSlide - 1));
               prevSlide.classList.remove("offScreen");
               prevSlide.classList.add("active");
               currentSlide -= 1
               // Hides next slide
               var nextSlide = document.getElementById("slide" + (currentSlide + 1));
               nextSlide.classList.remove("active");
               nextSlide.classList.add("offScreen");
          }
     }
}


document.onkeydown = function(event) {
     if (event.key == "ArrowRight" || event.key == " ") {
          slideShow.next();
     } else if (event.key == "ArrowLeft") {
          slideShow.prev();
     }
}
