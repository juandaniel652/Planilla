const API_URL = 'http://localhost:3000';

/* =====================
   LOGIN
===================== */
async function login() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  const res = await fetch(`${API_URL}/api/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email, password })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.error);
    return;
  }

  localStorage.setItem('token', data.token);
  alert(`Bienvenido ${data.nombre}`);
}

/* =====================
   SUMAR
===================== */
async function sumar() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('No estás logueado');
    return;
  }

  const a = Number(document.getElementById('a').value);
  const b = Number(document.getElementById('b').value);

  const res = await fetch(`${API_URL}/api/sumar`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ a, b })
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.error);
    return;
  }

  document.getElementById('resultado').innerText =
    `Resultado: ${data.resultado}`;
}

/* =====================
   HISTORIAL
===================== */
async function cargarHistorial() {
  const token = localStorage.getItem('token');
  if (!token) {
    alert('No estás logueado');
    return;
  }

  const res = await fetch(`${API_URL}/api/historial`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });

  const data = await res.json();

  if (!res.ok) {
    alert(data.error);
    return;
  }

  const ul = document.getElementById('historial');
  ul.innerHTML = '';

  data.forEach(item => {
    const li = document.createElement('li');
    li.textContent = `${item.numero_a} + ${item.numero_b} = ${item.resultado}`;
    ul.appendChild(li);
  });
}
