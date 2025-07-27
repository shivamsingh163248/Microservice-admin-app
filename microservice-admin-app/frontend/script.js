// Admin login
document.getElementById('adminLoginForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById("adminUser").value;
  const password = document.getElementById("adminPass").value;
  const res = await fetch("http://backend:5000/admin-login", {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  });
  const data = await res.json();
  if (res.ok) window.location.href = "admin.html";
  else alert(data.message);
});

// User registration
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const username = document.getElementById("regUser").value;
  const password = document.getElementById("regPass").value;
  const res = await fetch("http://backend:5000/register", {
    method: "POST",
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  });
  const data = await res.json();
  alert(data.message);
});
