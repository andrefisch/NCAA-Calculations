
window.addEventListener('touchstart', hideAllDropdowns)
window.addEventListener('click', hideAllDropdowns)

function hideAllDropdowns(event) {
    if (!event.target.matches('.dropbtn')) {
      var dropdowns = document.getElementsByClassName("dropdown-content");
      var i;
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
          openDropdown.classList.remove('show');
        }
      }
    }
  }
  
  function hideDropdown(menuid){
  
      
  
      var dropdown = menuid.getElementsByTagName('div')[0];
      if (dropdown.classList.contains('show')){
          dropdown.classList.remove('show'); 
      }
  
  }
  
    function displayWeapon() {
  
      weapon = document.getElementById("weapon")
      linksnav = document.getElementById("linksnav")
      medianav = document.getElementById("medianav")
  
      hideDropdown(linksnav);
      hideDropdown(medianav);
  
      weapon.getElementsByTagName('div')[0].classList.toggle("show");
      document.activeElement.blur()
  }
  
    function displayLinksnav() {
  
      weapon = document.getElementById("weapon")
      linksnav = document.getElementById("linksnav")
      medianav = document.getElementById("medianav")
  
      hideDropdown(weapon);
      hideDropdown(medianav);
      
      linksnav.getElementsByTagName('div')[0].classList.toggle("show");
      document.activeElement.blur()
  }
  
  
    function displayMedianav() {
  
      weapon = document.getElementById("weapon")
      linksnav = document.getElementById("linksnav")
      medianav = document.getElementById("medianav")
  
      hideDropdown(weapon);
      hideDropdown(linksnav);
     
      medianav.getElementsByTagName('div')[0].classList.toggle("show");
      document.activeElement.blur()
  }
  
  
  document.addEventListener("DOMContentLoaded", function() {
    var lazyloadImages = document.querySelectorAll("img.lazy");    
    var lazyloadThrottleTimeout;
    
    function lazyload () {
      if(lazyloadThrottleTimeout) {
        clearTimeout(lazyloadThrottleTimeout);
      }    
      
      lazyloadThrottleTimeout = setTimeout(function() {
          var scrollTop = window.pageYOffset;
          lazyloadImages.forEach(function(img) {
              if(img.offsetTop < (window.innerHeight + scrollTop)) {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
              }
          });
          if(lazyloadImages.length == 0) { 
            document.removeEventListener("scroll", lazyload);
            window.removeEventListener("resize", lazyload);
            window.removeEventListener("orientationChange", lazyload);
          }
      }, 20);
    }
    
    document.addEventListener("scroll", lazyload);
    window.addEventListener("resize", lazyload);
    window.addEventListener("orientationChange", lazyload);
  }); 