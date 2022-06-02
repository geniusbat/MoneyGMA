
let currentlyDisplaying = null;

function categoryClick(divId) {
    if (currentlyDisplaying==divId) {
        document.getElementById(currentlyDisplaying).style.display="none";
        currentlyDisplaying=null;
    }
    else {
        if (!(currentlyDisplaying==null)) {
            document.getElementById(currentlyDisplaying).style.display="none";
            currentlyDisplaying=null;
        }
        currentlyDisplaying=divId;
        document.getElementById(divId).style.display="block";
    }
}

function showMoreClicked() {
    element = document.getElementById("showMore");
    //Show
    if (element.innerHTML.normalize() == "Click for more:".normalize()) {
        element.innerHTML = "Click to hide:";
        ShowMoreData();
    }
    //Hide
    else {
        element.innerHTML = "Click for more:";
        HideMoreData();
    }
}

function HideMoreData() {
    element = document.getElementById("showMore-data");
    element.style.display="none";
}
function ShowMoreData() {
    element = document.getElementById("showMore-data");
    element.style.display="block";
}