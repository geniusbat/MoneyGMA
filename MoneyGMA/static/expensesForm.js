
function deselectAll() {
    let elements = document.getElementById("id_pools").options;

    for(var i = 0; i < elements.length; i++){
      elements[i].selected = false;
    }
}