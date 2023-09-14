document.addEventListener('DOMContentLoaded', async () => {
    // Assuming you have your subscriptions data in a variable
    // Get all rows from the table body
    var rows = document.querySelectorAll("#subscriptionsTable tbody tr");
    var subscriptions = [];

    var users = await fetchUsers()

    rows.forEach(function (row) {
        var cells = row.querySelectorAll("td");
        var subscription = {
            full_name: cells[0].textContent.trim(),
            email: cells[1].textContent.trim(),
            start_date: cells[2].textContent.trim(),
            end_date: cells[3].textContent.trim(),
            plan_name: cells[4].textContent.trim(),
            price: parseFloat(cells[5].textContent.trim().replace('£', ''))
        };
        subscriptions.push(subscription);
    });

    const plans_data = subscriptions.map(x => x.plan_name).reduce((acc, plan) => {
        acc[plan] = (acc[plan] || 0) + 1;
        return acc;
    }, {});

    // Calculate total monthly earnings
    const monthlyEarnings = subscriptions.reduce(function (acc, subscription) {
        return acc + subscription.price;
    }, 0);

    var ctxMonthlyEarnings = document.getElementById('monthlyEarningsChart').getContext('2d');
    var monthlyEarningsChart = new Chart(ctxMonthlyEarnings, {
        type: 'bar',
        data: {
            labels: ['Predicted Monthly Earnings'],
            datasets: [{
                label: 'Earnings (£)',
                data: [monthlyEarnings],
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
        }
    });

    // Sample data for chart 1
    var ctxSample1 = document.getElementById('sampleChart1').getContext('2d');
    var sampleChart1 = new Chart(ctxSample1, {
        type: 'bar',
        data: {
            labels: [Array.from(new Set(subscriptions.map(sub => getMonthName(sub.start_date))))],
            datasets: [{
                label: 'Number of users',
                data: [users.length],
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: false,
        }
    });

    // Sample data for chart 2
    var ctxSample2 = document.getElementById('sampleChart2').getContext('2d');
    var sampleChart2 = new Chart(ctxSample2, {
        type: 'pie',
        options: {
            responsive: false,
            maintainAspectRatio: true,
            aspectRatio: 1
        },
        data: {
            labels: Object.keys(plans_data),
            datasets: [{
                data: Object.values(plans_data),
                backgroundColor: ['rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)']
            }]
        }
    });
})



async function fetchUsers() {
    try {
        const response = await fetch('/api/users');
        return await response.json();
    }
    catch (e) {
        alert(e)
    }
}
function getMonthName(dateString) {
    const date = new Date(dateString);
    const monthNames = ["January", "February", "March", "April", "May", "June",
                        "July", "August", "September", "October", "November", "December"];

    return monthNames[date.getMonth()];
}