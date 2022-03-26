const sidebarButton = document.querySelector(".toggle-button");
const sidebarMenu = document.querySelector("#sidebarMenu");

sidebarButton.addEventListener("click", toggle);

function toggle(){
    if(sidebarMenu.style.display ==="none"){
        sidebarMenu.style.display = "block";
    }else{
        sidebarMenu.style.display = "none";
    }
}

document.onload = onstartFunction();

function onstartFunction(){
    sidebarMenu.style.display = "none";
}