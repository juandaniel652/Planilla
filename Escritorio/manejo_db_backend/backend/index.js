require('dotenv').config();
const express = require('express');
const cors = require('cors');
const supabase = require('./supabase');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const auth = require('./middleware/auth');


const app = express();

app.use(cors({
  origin: '*',
  methods: ['GET', 'POST', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

app.use(express.json());

/* =====================
   REGISTRO
===================== */
app.post('/api/register', async (req, res) => {
  const { nombre, email, password } = req.body;

  if (!nombre || !email || !password) {
    return res.status(400).json({ error: 'Faltan datos' });
  }

  const password_hash = await bcrypt.hash(password, 10);

  const { error } = await supabase
    .from('usuarios')
    .insert([{
      nombre,
      email,
      password: password_hash
    }]);

  if (error) {
    console.error(error);
    return res.status(500).json({ error: 'No se pudo registrar' });
  }

  res.json({ ok: true });
});

/* =====================
   LOGIN
===================== */
app.post('/api/login', async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.status(400).json({ error: 'Faltan datos' });
  }

  const { data: usuario, error } = await supabase
    .from('usuarios')
    .select('id, nombre, email, password')
    .eq('email', email)
    .single();

  if (error || !usuario) {
    return res.status(401).json({ error: 'Usuario no encontrado' });
  }

  const passwordOk = await bcrypt.compare(password, usuario.password);

  if (!passwordOk) {
    return res.status(401).json({ error: 'Contraseña incorrecta' });
  }

  const token = jwt.sign(
    { usuario_id: usuario.id },
    process.env.JWT_SECRET,
    { expiresIn: '2h' }
  );

  res.json({
    token,
    nombre: usuario.nombre,
    email: usuario.email
  });
});

/* =====================
   SUMAR (sin JWT aún)
===================== */
app.post('/api/sumar', auth, async (req, res) => {
  const { a, b } = req.body;
  const usuario_id = req.usuario_id;

  const resultado = a + b;

  const { error } = await supabase
    .from('calculos')
    .insert([{
      numero_a: a,
      numero_b: b,
      resultado,
      usuario_id
    }]);

  if (error) {
    console.error(error);
    return res.status(500).json({ error: error.message });
  }

  res.json({ resultado });
});


/* =====================
   HISTORIAL
===================== */
app.get('/api/historial', auth, async (req, res) => {
  const usuario_id = req.usuario_id;

  const { data, error } = await supabase
    .from('calculos')
    .select('*')
    .eq('usuario_id', usuario_id)
    .order('fecha', { ascending: false });

  if (error) {
    console.error(error);
    return res.status(500).json({ error: error.message });
  }

  res.json(data);
});

/* =====================
   START SERVER
===================== */
app.listen(3000, () => {
  console.log('Backend escuchando en puerto 3000');
});
