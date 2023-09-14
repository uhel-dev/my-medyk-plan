document.addEventListener("DOMContentLoaded", function() {



    // Fetch available services from the database and populate the dropdown
    fetchServices()
    // Fetch available plans from the database and populate the table
    fetchPlans()

    // Add Service to Selected Services
    // document.getElementById("addServiceBtn").addEventListener("click", function() {
    //     const selectedServices = document.getElementById("selected_services");
    //     Array.from(document.getElementById("available_services").selectedOptions).forEach(option => {
    //         selectedServices.appendChild(option);
    //     });
    // });

    // Remove Service from Selected Services
    document.getElementById("removeServiceBtn").addEventListener("click", function() {
        const availableServices = document.getElementById("available_services");

        Array.from(document.getElementById("selected_services").selectedOptions).forEach(option => {
            const originalIndex = parseInt(option.dataset.index, 10);
            if (originalIndex >= availableServices.children.length || !availableServices.children[originalIndex]) {
                availableServices.appendChild(option);
            } else {
                availableServices.insertBefore(option, availableServices.children[originalIndex]);
            }
        });
    });

    // Handle form submission
    document.getElementById("addPlanForm").addEventListener("submit", function(e) {
        e.preventDefault();



        // Validation
        const planNameElem = document.getElementById("plan_name");
        const planPriceElem = document.getElementById("plan_price");
        const availableServicesElem = document.getElementById("available_services");
        const selectedServicesElem = document.getElementById("selected_services");

        const elements = document.getElementsByClassName('selectedServiceOption');
        const service_ids = Array.from(elements).map(element => element.value);
        const service_max_usage_count = Array.from(elements).map(element => element.innerText);
        const services_info = Array.from(elements).map(el => {
            return {
                service_id: el.value,
                service_max_usage_count: el.innerText
            }
        })

        const planName = planNameElem.value;
        const planPrice = planPriceElem.value;
        // const selectedServices = Array.from(selectedServicesElem.options);

        if (!planName.trim()) {
            Swal.fire('Error', 'Plan name is required!', 'error');
            return;
        }

        if (!planPrice.trim() || parseFloat(planPrice) <= 0) {
            Swal.fire('Error', 'Plan price must be a positive number!', 'error');
            return;
        }

        if (service_ids.length === 0) {
            Swal.fire('Error', 'At least one service must be selected!', 'error');
            return;
        }

        const planData = {
            plan_name: planName,
            price: planPrice,
            services: service_ids,
            services_info: services_info
        };

        // Post data to the API endpoint
        fetch("/api/plans", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(planData)
        })
        .then(response => response.json())
        .then(data => {
            if(data.status && data.status !== 200) {
                Swal.fire('Error', data.message, 'error');
            } else {
                // Success
                // Swal.fire('Success', data.message, 'success');
                Swal.fire({
                    title: 'Success',
                    text: data.message,
                    icon: 'success',
                    customClass: {
                        popup: 'top-right-corner-alert'
                    },
                    timer: 1000,
                    allowOutsideClick: true //
                });
                // Clear the form fields after successful plan creation
                planNameElem.value = "";
                planPriceElem.value = "";
                while (selectedServicesElem.firstChild) {
                    availableServicesElem.appendChild(selectedServicesElem.firstChild);
                }
                fetchPlans()

            }
        })
        .catch(error => {
            console.error("Error:", error);
            Swal.fire('Error', 'Something went wrong!', 'error');
        });
    });

    const toggleBtn = document.getElementById("togglePlanForm");
    const form = document.getElementById("addPlanForm");

    toggleBtn.addEventListener("click", function() {
        if (form.classList.contains('hidden')) {
            form.classList.remove('hidden');
            toggleBtn.textContent = '-';
        } else {
            form.classList.add('hidden');
            toggleBtn.textContent = '+';
        }
    });

    document.getElementById('addServiceBtn').addEventListener('click', function() {
        const availableServicesSelect = document.getElementById('available_services');
        const selectedServicesContainer = document.getElementById('selected_services');

        Array.from(availableServicesSelect.selectedOptions).forEach(option => {
            // Create a div container for the service
            const serviceDiv = document.createElement('div');
            serviceDiv.className = "selectedServiceOption flex justify-between items-center my-2";

            // Service id
            const serviceID = document.createElement('span');
            serviceID.innerText = option.value;
            serviceID.style.display = 'none';
            serviceDiv.appendChild(serviceID)

            // Service name label
            const serviceName = document.createElement('span');
            serviceName.innerText = option.textContent;
            serviceDiv.appendChild(serviceName);

            // Input field for usage count
            const usageCountInput = document.createElement('input');
            usageCountInput.type = "number";
            usageCountInput.name = `service_usage[${option.value}]`;
            usageCountInput.min = "1";
            usageCountInput.placeholder = "Usage Count";
            usageCountInput.className = "ml-4 px-2 py-1 border rounded-md";
            serviceDiv.appendChild(usageCountInput);

            // Append to selected services container
            selectedServicesContainer.appendChild(serviceDiv);

            // Optionally, remove the selected service from the available services
        option.remove();
        });
    });

    document.getElementById('removeServiceBtn').addEventListener('click', function() {
        // Logic to handle removing services from 'selected_services'
        // and adding them back to 'available_services'. This will be similar
        // to the above logic but in reverse.
        const selectedServicesContainer = document.getElementById('selected_services');
        const availableServicesSelect = document.getElementById('available_services');

        Array.from(selectedServicesContainer.children).forEach(serviceDiv => {
            // Assuming you have a mechanism to select which services to remove
            // For simplicity, let's assume a serviceDiv is to be removed if its input value is empty

            const input = serviceDiv.querySelector('input[type="number"]');
            if (!input || !input.value) {
                // Create a new option for the available services select
                const serviceOption = document.createElement('option');
                serviceOption.value = input.name.match(/\[(\d+)\]/)[1]; // Extracting service ID from input name
                serviceOption.textContent = serviceDiv.querySelector('span').textContent;

                availableServicesSelect.appendChild(serviceOption);

                // Remove the div from selected services
                selectedServicesContainer.removeChild(serviceDiv);
            }
        });
    });



});


const fetchServices = () => {
    fetch("/api/services")
    .then(response => response.json())
    .then(data => {
        const servicesDropdown = document.getElementById("available_services");

        if (data.length === 0) {
            const option = document.createElement("option");
            option.value = "";
            option.disabled = true;
            option.textContent = "No treatments available";
            servicesDropdown.appendChild(option);
        } else {
            data.forEach((service, index) => {
                const option = document.createElement("option");
                option.value = service.id;
                option.textContent = service.service_name;
                option.dataset.index = index;  // Store the original index on the option
                servicesDropdown.appendChild(option);
            });
        }
    });
}


// const fetchPlans = () => {
//     fetch("/api/plans")
//     .then(response => response.json())
//     .then(data => {
//         const plansTableBody = document.getElementById("plansTable").querySelector("tbody");
//         const noPlansMessage = document.getElementById("noPlansMessage");
//
//         if (data.length === 0) {
//             noPlansMessage.style.display = "block";
//         } else {
//             noPlansMessage.style.display = "none";
//              // Fetch services for each plan
//             const servicesPromises = data.map(plan =>
//                 fetch(`/api/plans/${plan.id}/services`)
//                     .then(response => response.json())
//                     .then(services => {
//                         plan.services = services;
//                         return plan;
//                     })
//             );
//             Promise.all(servicesPromises).then(completedPlans => {
//                 completedPlans.forEach(plan => {
//                     const row = document.createElement("tr");
//
//                     const nameCell = document.createElement("td");
//                     nameCell.textContent = plan.plan_name;
//                     row.appendChild(nameCell);
//
//                     const priceCell = document.createElement("td");
//                     priceCell.textContent = plan.price;
//                     row.appendChild(priceCell);
//
//                     const actionsCell = document.createElement("td");
//                     actionsCell.className = "text-center";
//
//                     const servicesCell = document.createElement("td");
//                     servicesCell.textContent = plan.services.map(x => x[1]).join(", ");  // services is an array of [id, service_name]
//                     row.appendChild(servicesCell);
//
//                     const deleteButton = document.createElement("img");
//                     deleteButton.src = "/static/images/trash-bin.svg";
//                     deleteButton.className = "cursor-pointer hover:opacity-70 transition duration-300 ease-in-out";
//                     deleteButton.alt = "Delete";
//                     deleteButton.title = "Delete Plan";
//                     deleteButton.style.width = "24px"; // Set the width of the icon
//                     deleteButton.style.height = "24px"; // Set the height of the icon
//
//                     deleteButton.addEventListener("click", function() {
//                             fetch(`/api/plans/${plan.id}`, {
//                                 method: 'DELETE'
//                             })
//                             .then(response => {
//                                 if (!response.ok) {
//                                     throw new Error('Network response was not ok');
//                                 }
//                                 return response.json();
//                             })
//                             .then(data => {
//                                 // remove the plan row from the UI
//                                 row.parentNode.removeChild(row);
//
//                                 // Check if there are any other plans left, if not, display the noPlansMessage
//                                 if (plansTableBody.children.length === 0) {
//                                     noPlansMessage.style.display = "block";
//                                 }
//                             })
//                             .catch(error => {
//                                 console.error("Error deleting the plan:", error);
//                             });
//                     });
//                     actionsCell.appendChild(deleteButton);
//
//                     row.appendChild(actionsCell);
//                     plansTableBody.appendChild(row);
//                 });
//             })
//         }
//     })
//     .catch(error => {
//         console.error("Error:", error);
//     });
// }

const fetchPlans = () => {
    fetch("/api/plans")
    .then(response => response.json())
    .then(data => {
        const plansContainer = document.getElementById("plansContainer");
        const noPlansMessage = document.getElementById("noPlansMessage");
        const planCardTemplate = document.getElementById("planCardTemplate");

        // Clear existing plan cards
        plansContainer.innerHTML = '';

        if (data.length === 0) {
            noPlansMessage.style.display = "block";
        } else {
            noPlansMessage.style.display = "none";

            // Fetch services for each plan
            const servicesPromises = data.map(plan =>
                fetch(`/api/plans/${plan.id}/services`)
                    .then(response => response.json())
                    .then(services => {
                        plan.services = services;
                        return plan;
                    })
            );

            Promise.all(servicesPromises).then(completedPlans => {
                completedPlans.forEach(plan => {
                    const planCard = planCardTemplate.querySelector('.planCard').cloneNode(true);

                    planCard.querySelector('.planName').textContent = plan.plan_name;
                    planCard.querySelector('.planPrice').textContent = `£${plan.price}`;
                    // planCard.querySelector('.planServices').textContent = "Included Services: " + plan.services.map(x => x[1]).join(", "); // services is an array of [id, service_name]

                    const servicesContainer = planCard.querySelector('.planServices');
                    plan.services.forEach(service => {
                        const serviceDiv = document.createElement('div');
                        serviceDiv.className = 'serviceItem bg-blue-200 rounded p-4 text-sm text-gray-700'; // Added a basic styling, you can customize as per your requirements
                        serviceDiv.textContent = service[1];  // service_name from the [id, service_name] structure
                        servicesContainer.appendChild(serviceDiv);
                    });

                    const deleteButton = planCard.querySelector('.deletePlanBtn');
                    deleteButton.addEventListener("click", function() {
                        fetch(`/api/plans/${plan.id}`, {
                            method: 'DELETE'
                        })
                        .then(response => {
                            if (!response.ok) {
                                throw new Error('Network response was not ok');
                            }
                            return response.json();
                        })
                        .then(data => {
                            // remove the plan card from the UI
                            plansContainer.removeChild(planCard);

                            // Check if there are any other plans left, if not, display the noPlansMessage
                            if (plansContainer.children.length === 0) {
                                noPlansMessage.style.display = "block";
                            }
                        })
                        .catch(error => {
                            console.error("Error deleting the plan:", error);
                        });
                    });

                    plansContainer.appendChild(planCard);
                });
            })
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
}
