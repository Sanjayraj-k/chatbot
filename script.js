document.getElementById('menuButton').addEventListener('click', function () {
    const sidebar = document.getElementById('sidebar');
    // Toggle the width of the sidebar
    if (sidebar.style.width === '250px') {
        sidebar.style.width = '0'; // Close the sidebar
    } else {
        sidebar.style.width = '250px'; // Open the sidebar
    }
});