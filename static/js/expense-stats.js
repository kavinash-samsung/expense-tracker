
const renderChart = (data, labels)=>{
    
    const ctx = document.getElementById('myChart').getContext('2d');
    console.log(data);
    console.log(labels);
    const myChart = new Chart(ctx, {
        type: 'polarArea',
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

const getChartData = ()=>{
    fetch('expense-category-summary').then(res=>res.json()).then((results)=>{
        var categoryData = results.expense_category_data;
        var [labels, data] = [Object.keys(categoryData), Object.values(categoryData)]
        renderChart(data, labels);
    });
    console.log("getchart data");
}


document.onload = getChartData()