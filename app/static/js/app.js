// Wait until the public page has loaded before adding small interface enhancements.
document.addEventListener("DOMContentLoaded", () => {
    // Find every navigation link that points to the current page.
    const currentPath = window.location.pathname;

    // Highlight the current public navigation item.
    document.querySelectorAll(".navbar .nav-link").forEach((link) => {
        // Compare the link path with the current browser path.
        if (new URL(link.href, window.location.origin).pathname === currentPath) {
            // Add a subtle gold underline effect.
            link.style.color = "#f5df9b";
        }
    });

    // Automatically dismiss Bootstrap alerts after a short delay.
    document.querySelectorAll(".alert").forEach((alert) => {
        // Wait ten seconds before hiding the alert.
        setTimeout(() => {
            // Hide the alert with Bootstrap's component API when available.
            if (window.bootstrap) {
                // Create the Bootstrap alert controller.
                const instance = bootstrap.Alert.getOrCreateInstance(alert);
                // Close the alert.
                instance.close();
            }
        }, 10000);
    });
});
