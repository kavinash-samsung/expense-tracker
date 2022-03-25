const searchField = document.querySelector("#searchField");
const tableOutput = document.querySelector(".table-output");
const appTable = document.querySelector(".app-table");
const pagination = document.querySelector(".pagination-container");
const tbody = document.querySelector(".table-body");
const noElement = document.querySelector(".noElement");
noElement.style.display = "none";
tableOutput.style.display = "none";

searchField.addEventListener('keyup', (e)=>{
    const searchValue = e.target.value;
    if(searchValue.length > 0){
        console.log(searchValue+"inside");
        fetch("search-expenses",{
            body: JSON.stringify({ searchText: searchValue }),
            method:"POST",
        }).then((res)=> res.json())
        .then((data) => {
            console.log("data", data);
            appTable.style.display = "none";
            pagination.style.display = "none";
            tbody.innerHTML = "";
            if(data.length == 0){
                tableOutput.style.display = "none";
                noElement.style.display = "block";
            }else{
                noElement.style.display = "none";
                tableOutput.style.display = "block";
                var counter = 0
                data.forEach((item)=>{
                    counter += 1
                    console.log(item);
                    tbody.innerHTML += `
                    <tr>
                        <td scope="row">${ counter }</td>
                        <td>${item.amount}</td>
                        <td>${item.category}</td>
                        <td>${item.description}</td>
                        <td>${item.date}</td>
                        <td class="mx-2">
                            <a class="btn btn-outline-success px-4" href="edit-expense/${item.id}">Edit</a>    
                            <a class="btn btn-outline-danger px-3" href="delete-expense/${item.id}">Delete</a>
                        </td>
                    </tr>
                    `
                });
                
            }
        });
    }else{
        tableOutput.style.display = "none";
        noElement.style.display = "none";
        appTable.style.display = "block";
        pagination.style.display = "block";
    }

})
