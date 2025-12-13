// Obtener elementos del DOM
const form = document.getElementById("asignacionForm");
const mensaje = document.getElementById("mensaje");
const consultarBtn = document.getElementById("consultarBtn");
const resultadoDiv = document.getElementById("resultadoTerritorio");
const territorioInput = document.getElementById("territorioInput");

// URL base del backend
const BASE_URL = "http://127.0.0.1:8000";

// Función para mostrar mensajes
function mostrarMensaje(texto, tipo = "success") {
  mensaje.textContent = texto;
  mensaje.classList.remove("text-green-600", "text-red-600");
  if (tipo === "success") {
    mensaje.classList.add("text-green-600");
  } else {
    mensaje.classList.add("text-red-600");
  }
}

// ----- CONSULTAR ASIGNACIONES POR TERRITORIO -----
async function consultarAsignaciones(numero) {
  resultadoDiv.innerHTML = "";

  if (!numero) {
    resultadoDiv.innerHTML = "<p class='text-red-600'>Ingrese un número de territorio válido.</p>";
    return;
  }

  try {
    const response = await fetch(`${BASE_URL}/asignaciones/territorio`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ numero_territorio: parseInt(numero) })
    });

    const data = await response.json();

    if (!data.success || !data.asignaciones.length) {
      resultadoDiv.innerHTML = "<p>No se encontraron asignaciones para este territorio.</p>";
      return;
    }

    // Mostrar resultados
    let html = `<h3 class="font-semibold mb-2">Asignaciones del territorio ${numero}</h3>`;
    html += "<ul class='list-disc pl-5'>";
    data.asignaciones.forEach(a => {
      html += `<li class="mb-2">
        Conductor: ${a.conductor} <br>
        Fecha Asignado: ${a.fecha_asignado || '—'} <br>
        Fecha Completado: ${a.fecha_completado || '—'} <br>
        Territorios: ${a.cantidad_abarcado || '—'}
      </li>`;
    });
    html += "</ul>";

    resultadoDiv.innerHTML = html;

  } catch (error) {
    resultadoDiv.innerHTML = `<p class='text-red-600'>Error al consultar: ${error}</p>`;
    console.error("Error real al consultar:", error);
  }
}

// Evento click del botón de consultar
consultarBtn.addEventListener("click", () => {
  const numero = territorioInput.value.trim();
  consultarAsignaciones(numero);
});

// ----- INSERTAR ASIGNACIÓN -----
async function enviarAsignacion(data) {
  try {
    const response = await fetch(`${BASE_URL}/asignaciones`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });

    const result = await response.json();

    if (response.ok) {
      mostrarMensaje(result.message, "success");
      form.reset();

      // Si el territorio insertado coincide con el input de consulta, actualizar la lista automáticamente
      if (territorioInput.value.trim() === String(data.numero_territorio)) {
        consultarAsignaciones(data.numero_territorio);
      }

    } else {
      mostrarMensaje(result.detail || "Error al agregar asignación", "error");
    }
  } catch (error) {
    mostrarMensaje("Error de conexión al backend", "error");
    console.error("Error real al insertar:", error);
  }
}

// Evento submit del formulario
form.addEventListener("submit", (e) => {
  e.preventDefault();

  const asignacion = {
    numero_territorio: parseInt(document.getElementById("numero_territorio").value),
    conductor: document.getElementById("conductor").value.trim(),
    fecha_asignado: document.getElementById("fecha_asignado").value,
    fecha_completado: document.getElementById("fecha_completado").value,
    total_abarcado: document.getElementById("total_abarcado").value.trim()
  };

  if (!asignacion.numero_territorio || !asignacion.conductor || !asignacion.fecha_asignado || !asignacion.fecha_completado || !asignacion.total_abarcado) {
    mostrarMensaje("Por favor completa todos los campos", "error");
    return;
  }

  enviarAsignacion(asignacion);
});
