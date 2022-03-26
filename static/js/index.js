
const renderChart1 = (data, labels)=>{
    
    const ctx = document.getElementById('ExpenseChart').getContext('2d');
    console.log(data);
    console.log(labels);
    const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: labels,
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title:{
                display:true,
                text: "Expenses By Category",
            }
        }
    });

}

const getChartData1 = ()=>{
    fetch('expenses/expense-category-summary').then(res=>res.json()).then((results)=>{
        var categoryData = results.expense_category_data;
        var [labels, data] = [Object.keys(categoryData), Object.values(categoryData)]
        renderChart1(data, labels);
    });
    console.log("getchart data");
}


const renderChart2 = (data, labels)=>{
    
    const ctx = document.getElementById('IncomeChart').getContext('2d');
    console.log(data);
    console.log(labels);
    const myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: labels,
                data: data,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            title:{
                display:true,
                text: "Income by Source",
            }
        }
    });

}

const getChartData2 = ()=>{
    fetch('income/income-source-summary').then(res=>res.json()).then((results)=>{
        var sourceData = results.income_source_data;
        var [labels, data] = [Object.keys(sourceData), Object.values(sourceData)]
        renderChart2(data, labels);
    });
    console.log("getchart data");
}


document.onload = getChartData1()
document.onload = getChartData2()