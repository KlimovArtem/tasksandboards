var cols_list = [];
var django_total_form = document.getElementById("id_column-TOTAL_FORMS")
var add_col_btn = document.querySelector("[data-cols-widget-add-col-btn]");
add_col_btn.addEventListener("click", addCol);


/**
* Добавляет введённый пользователем текст в массив cols_list,
* На основании введённого текста и его индекса в массиве формирует елемент fieldset и
* вставляет его в DOM страницы
*/
function addCol() {

  const input = document.querySelector("[data-cols-widget-input]");
  const output = document.querySelector("[data-cols-widget-output]");
  const errors = document.querySelectorAll("ul.errorlist");

  for (error of errors) {
    error.remove();
  }
  if (input.value == "") {
    return
  }

  if (cols_list.includes(input.value)){
    const error_list = document.createElement("ul");
    error_list.setAttribute("class", "errorlist");
    error_list.innerHTML = "<li>Колонка с таким именем уже существует</li>";
    add_col_btn.after(error_list);
    input.value = "";
    return
  }

  cols_list.push(input.value);
  const col_position = cols_list.indexOf(input.value);
  const col = document.createElement("div");
  col.setAttribute("class", "col");
  col.innerHTML = `<input type="text"  name="column-${col_position}-name" class="col-name" value="${input.value}" readonly><input class="col-pos" name="column-${col_position}-position" value=${col_position} readonly><div class="col-order-btns-layout"><button type="button" class="btn" data-cols-widget-up-col-btn>▲</button><button type="button" class="btn" data-cols-widget-down-col-btn>▼</button></div><button type="button" class="del-col-btn btn" data-cols-widget-del-col-btn>X</button>`;
  output.append(col);
  django_total_form.value = cols_list.length
  input.value = "";
}

function updateColsPosition(){
  const output = document.querySelector("[data-cols-widget-output]");
  for (col of output.children) {
    col.querySelector(".col-pos").value = cols_list.indexOf(col.querySelector(".col-name").value);
  }

}

document.querySelector("[data-cols-widget-output]").addEventListener('click', function(event) {
  if (event.target.hasAttribute("data-cols-widget-del-col-btn")) {
    const target = event.target.parentElement;
    cols_list.splice(cols_list.indexOf(target.querySelector(".col-name").value), 1);
    target.remove();
    django_total_form.value = cols_list.length
    updateColsPosition();
  }
  if (event.target.hasAttribute("data-cols-widget-up-col-btn")) {
    const target = event.target.parentElement.parentElement;
    const pop_item_index = target.querySelector(".col-pos").value;
    if (pop_item_index == 0) {
      return
    }
    const pop_item = cols_list.splice(cols_list.indexOf(target.querySelector(".col-name").value), 1)[0];
    cols_list.splice((pop_item_index - 1), 0, pop_item);
    target.previousSibling.before(target);
    updateColsPosition();
  }
  if (event.target.hasAttribute("data-cols-widget-down-col-btn")) {
    const target = event.target.parentElement.parentElement;
    const pop_item_index = target.querySelector(".col-pos").value;
    if (pop_item_index == (cols_list.length-1)) {
      return
    }
    const pop_item = cols_list.splice(cols_list.indexOf(target.querySelector(".col-name").value), 1)[0];
    cols_list.splice((pop_item_index + 1), 0, pop_item);
    target.nextSibling.after(target);
    updateColsPosition();
  }
});
