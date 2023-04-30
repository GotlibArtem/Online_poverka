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

function searchGR() {
    let input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("tableId1");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
        tds = tr[i].getElementsByTagName("td")
        let foundInRow = false;
        for (j = 0; j < tds.length; j++) {
            if (foundInRow)
                continue;
            td = tr[i].getElementsByTagName("td")[j];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    foundInRow = true;
                    tr[i].style.display = "";
                } else {
                    tr[i].style.display = "none";
                }
            }
        }
    }
}

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
