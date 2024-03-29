document.addEventListener('DOMContentLoaded', () => {
    const getSort = ({ target }) => {
        const order = (target.dataset.order = -(target.dataset.order || -1));
        const index = [...target.parentNode.cells].indexOf(target);
        const collator = new Intl.Collator(['en', 'ru'], { numeric: true });
        const comparator = (index, order) => (a, b) => order * collator.compare(
            a.children[index].innerHTML,
            b.children[index].innerHTML,
            );
        for(const tBody of target.closest('table').tBodies)
            tBody.append(...[...tBody.rows].sort(comparator(index, order)));
        for(const cell of target.parentNode.cells)
        cell.classList.toggle('sorted', cell === target);
        // document.querySelectorAll('.mainTable tbody tr td:first-child').forEach((el, i) => el.textContent = i + " ");
    };
    document.querySelectorAll('.mainTable thead').forEach(tableTH => tableTH.addEventListener('click', () => getSort(event)));
});

function checkboxes_sel_all(obj)
{
let items = obj.form.getElementsByTagName("input"), len, i;

for (i = 0, len = items.length; i < len; i += 1)
    {
    if (items.item(i).type && items.item(i).type === "checkbox")
    {
    if (obj.checked)
        {
        items.item(i).checked = true;
        }
    else
        {
        items.item(i).checked = false;
        }      
    }
    }
}


let tableElements = document.querySelectorAll("tbody > tr"), arrayWithData = [];

Array.from(tableElements, e => {
  let childNodes = e.getElementsByTagName("td");
  arrayWithData.push({
    name: childNodes[1].textContent
  });
});

let result = arrayWithData.map(a => a.name);
result = String(result).replace(/[a-zа-яё]/gi, '');

// Values123 = Array.from(document.getElementsByName('meas_result'), c=> c.value);
// console.log(Values123);



console.log(result)

document.getElementById("tableBox").addEventListener("input",
function (e) {
    var inp = e.target;
    if (inp.tagName === "INPUT") {
        let mass = 60;
        var td = inp.parentElement.parentElement;
        td.querySelector(".column_data_x2").textContent = inp.value - result
    }
  }
);

let postfixes = ["п", "н", "мк", "м", "к", "М", "Г", "Т"]
var MeasResult = document.getElementById("MeasResult")
new_meas = String(MeasResult).replace()
