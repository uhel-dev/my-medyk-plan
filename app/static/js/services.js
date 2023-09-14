document.addEventListener("DOMContentLoaded", function() {
    // Fetch all services on page load
    fetchServices();

    // Add service form submission
    const addServiceForm = document.getElementById('addServiceForm');
    addServiceForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const serviceName = document.getElementById('service_name').value;
        const servicePrice = document.getElementById('price').value;


        if (!serviceName || !servicePrice) {
            alert("Service name and price are required!");
            return;
        }

        fetch('/api/services', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                service_name: serviceName,
                price: servicePrice
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                fetchServices();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Something went wrong. Please try again.');
        });
    });
});

// Function to delete a service
function deleteService(serviceId) {
    fetch(`/api/services/${serviceId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            fetchServices();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    });
}

// Function to fetch all services
async function fetchServices() {
    // Fetch existing services and populate the table
    try {
        const response = await fetch('/api/services');
        const services = await response.json();
        const tableBody = document.getElementById('servicesTable').querySelector('tbody');
        const noServicesMessage = document.getElementById('noServicesMessage');

        // Clear existing rows
        tableBody.innerHTML = '';

        if (services.length > 0) {
            // Hide the no services message
            noServicesMessage.style.display = 'none';

            // Add new rows
            services.forEach(service => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="px-4 py-2">${service.service_name}</td>
                    <td class="px-4 py-2 text-center">${service.price}</td>
                    <td class="px-4 py-2 text-center">
                        <button onclick="deleteService(${service.id})" class="bg-transparent p-2 hover:bg-red-200 rounded transition duration-300 ease-in-out">
                            <img src="/static/images/trash-bin.svg" alt="Delete" width="20">
                        </button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            // Show the no services message
            noServicesMessage.style.display = 'block';
        }

    } catch (error) {
        alert('Error fetching services:', error);
    }
}

