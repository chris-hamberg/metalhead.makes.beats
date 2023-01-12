var acc = document.getElementsByClassName("accordion");
var panel = document.getElementsByClassName("panel")[0];
var mfs_html5 = document.getElementById("mfs_html5");


function beatStore() {
    /* Toggle between adding and removing the "active" class,
    to highlight the button that controls the panel */        
    this.classList.toggle("active");
    /* Toggle between hiding and showing the active panel */
    if (panel.style.maxHeight) {
        panel.style.maxHeight = null;
        document.body.style.overflow = "auto";
    } else {
        mfs_html5.style.height = (window.innerHeight * .83) + "px";
        panel.style.maxHeight = (window.innerHeight * .83) + "px";
        window.scrollTo({top: 0, behavior: "smooth"});
        document.body.style.overflow = "hidden";
    }
}


for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", beatStore);
}
