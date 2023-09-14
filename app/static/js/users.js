document.addEventListener("DOMContentLoaded", function() {
    // Fetch all users on page load
    fetchUsers();
});

// Function to fetch all users
async function fetchUsers() {
    try {
        const response = await fetch('/api/users');
        const users = await response.json();
        const tableBody = document.getElementById('usersTable').querySelector('tbody');
        const noUsersMessage = document.getElementById('noUsersMessage');

        // Clear existing rows
        tableBody.innerHTML = '';

        if (users.length > 0) {
            noUsersMessage.style.display = 'none';
            users.forEach(user => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td class="px-4 py-2">${user.full_name}</td>
                    <td class="px-4 py-2">${user.email}</td>
                    <td class="px-4 py-2 text-center">
                         <button onclick="deleteUser(${user.id})" class="bg-transparent p-2 hover:bg-red-200 rounded transition duration-300 ease-in-out">
                            <img src="/static/images/trash-bin.svg" alt="Delete" width="20">
                        </button>
                        <a href="../edit/user/${user.id}">
                            <button class="bg-transparent p-2 hover:bg-red-200 rounded transition duration-300 ease-in-out">
                                <img src="/static/images/pen.svg" alt="Delete" width="20">
                            </button>
                        </a>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        } else {
            noUsersMessage.style.display = 'block';
        }
    } catch (error) {
        alert('Error fetching users:', error);
    }
}



// Function to delete a service
function deleteUser(userId) {
    fetch(`/api/users/${userId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            fetchUsers();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Something went wrong. Please try again.');
    });
}
