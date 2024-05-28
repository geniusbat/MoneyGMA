
function deselectAll() {
    let elements = document.getElementById("id_pools").options;

    for(var i = 0; i < elements.length; i++){
      elements[i].selected = false;
    }
}

function addToExpense() {
  let quantInput = document.getElementById("addToExpenseInput");
  let moneyInput = document.getElementById("id_money");
  moneyInput.value = parseFloat(moneyInput.value) + parseFloat(quantInput.value);
  quantInput.value = 0;
}