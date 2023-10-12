document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the default form submission.

    // Get the values entered by the user.
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;

    // Define the hardcoded email addresses and the common password.
    var hardcodedEmails = ['christinebird@watson.com', 'yhenry@williams.com', 'wilsonpatrick@wilson.info'];
    var commonPassword = '1234';

    // Check if the entered email and password match any of the hardcoded values.
    if (hardcodedEmails.includes(email) && password === commonPassword) {
        // Redirect to the dashboard page on successful login.
        window.location.href = 'dashboard.html?email='+email;
    } else {
        document.getElementById('loginMessage').textContent = 'Login failed. Please check your email and password.';
    }
});
