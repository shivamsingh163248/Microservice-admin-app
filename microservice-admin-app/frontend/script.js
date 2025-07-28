// Determine the backend URL based on environment
// When running in Docker, frontend and backend communicate through Docker network
// When accessed from browser, use the exposed port
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' ? 
    'http://localhost:5000' : 
    `http://${window.location.hostname}:5000`;

// User login
document.getElementById('userLoginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById("userUsername").value;
    const password = document.getElementById("userPassword").value;
    
    try {
        const res = await fetch(`${API_BASE_URL}/login`, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        const data = await res.json();
        
        if (res.ok) {
            alert(data.message);
            // Redirect to user dashboard or success page
            window.location.href = "user-dashboard.html";
        } else {
            alert(data.message);
        }
    } catch (error) {
        alert("Error connecting to server. Please try again.");
        console.error('Login error:', error);
    }
});

// Admin login
document.getElementById('adminLoginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById("adminUser").value;
    const password = document.getElementById("adminPass").value;
    
    try {
        const res = await fetch(`${API_BASE_URL}/admin-login`, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        const data = await res.json();
        
        if (res.ok) {
            window.location.href = "admin.html";
        } else {
            alert(data.message);
        }
    } catch (error) {
        alert("Error connecting to server. Please try again.");
        console.error('Admin login error:', error);
    }
});

// User registration
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById("regUser").value;
    const password = document.getElementById("regPass").value;
    
    if (!username || !password) {
        alert("Please fill in all fields");
        return;
    }
    
    try {
        const res = await fetch(`${API_BASE_URL}/register`, {
            method: "POST",
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });
        const data = await res.json();
        
        alert(data.message);
        
        if (res.ok) {
            // Clear form on successful registration
            document.getElementById("regUser").value = '';
            document.getElementById("regPass").value = '';
            // Optionally redirect to login
            setTimeout(() => {
                window.location.href = "index.html";
            }, 1500);
        }
    } catch (error) {
        alert("Error connecting to server. Please try again.");
        console.error('Registration error:', error);
    }
});
