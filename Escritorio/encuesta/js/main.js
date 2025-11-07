import { CampañasManager } from "./campañas.js";
import { PreguntasManager } from "./preguntas.js";
import { Estadisticas } from "./estadisticas.js";

// === ELEMENTOS ===
const listaCampanias = document.getElementById("listaCampanias");
const seccionCreador = document.getElementById("seccionCreador"); // 👈 nueva referencia
const seccionPreguntas = document.getElementById("seccionPreguntas");
const tituloCampania = document.getElementById("tituloCampania");
const listaPreguntas = document.getElementById("listaPreguntas");
const resumenEvaluacion = document.getElementById("resumenEvaluacion");

const btnAbrir = document.getElementById("btnAbrir");
const btnCerrar = document.getElementById("btnCerrar");
const formCampania = document.getElementById("formCampania");
const modal = document.getElementById("modal");

const btnNuevaPregunta = document.getElementById("btnNuevaPregunta");
const modalPregunta = document.getElementById("modalPregunta");
const formPregunta = document.getElementById("formPregunta");
const btnCerrarPregunta = document.getElementById("btnCerrarPregunta");

const modoCreador = document.getElementById("modoCreador");
const modoEvaluador = document.getElementById("modoEvaluador");
const modoEstadisticas = document.getElementById("modoEstadisticas");

const seccionEstadisticas = document.getElementById("estadisticas");
const contenedorEstadisticas = document.getElementById("contenedorEstadisticas");

const btnAbrirMenu = document.getElementById("btnAbrirMenu");
const btnCerrarMenu = document.getElementById("btnCerrarMenu");
const sidebar = document.getElementById("sidebar");
const tituloSeccion = document.getElementById("tituloSeccion");

let modoActual = "creador";

// === INSTANCIAS ===
const manager = new CampañasManager(listaCampanias, mostrarPreguntas);
const preguntasManager = new PreguntasManager(
  listaPreguntas,
  tituloCampania,
  resumenEvaluacion,
  manager
);
const estadisticas = new Estadisticas(contenedorEstadisticas, manager);

// === MENÚ LATERAL (HAMBURGUESA) ===
btnAbrirMenu.addEventListener("click", () => sidebar.classList.remove("-translate-x-full"));
btnCerrarMenu.addEventListener("click", () => sidebar.classList.add("-translate-x-full"));

function activarModo(boton) {
  document.querySelectorAll(".nav-btn").forEach((btn) => btn.classList.remove("active"));
  boton.classList.add("active");
}

// === MODO CREADOR ===
modoCreador.addEventListener("click", () => {
  modoActual = "creador";
  activarModo(modoCreador);
  tituloSeccion.textContent = "Crear Campaña";

  seccionCreador.classList.remove("hidden");
  btnAbrir.classList.remove("hidden");

  seccionPreguntas.classList.add("hidden");
  seccionEstadisticas.classList.add("hidden");
  resumenEvaluacion.classList.add("hidden");

  manager.render("creador");
});

// === MODO EVALUADOR ===
modoEvaluador.addEventListener("click", () => {
  modoActual = "evaluador";
  activarModo(modoEvaluador);
  tituloSeccion.textContent = "Evaluar Campañas";

  seccionCreador.classList.remove("hidden");
  btnAbrir.classList.add("hidden");

  seccionPreguntas.classList.add("hidden");
  seccionEstadisticas.classList.add("hidden");
  resumenEvaluacion.classList.add("hidden");

  manager.render("evaluador");
});

// === MODO ESTADÍSTICAS ===
modoEstadisticas.addEventListener("click", () => {
  modoActual = "estadisticas";
  activarModo(modoEstadisticas);
  tituloSeccion.textContent = "Estadísticas Globales";

  seccionCreador.classList.add("hidden");
  seccionPreguntas.classList.add("hidden");

  estadisticas.mostrar();
  seccionEstadisticas.classList.remove("hidden");
});

// === CREAR CAMPAÑA ===
btnAbrir.addEventListener("click", () => modal.classList.remove("hidden"));
btnCerrar.addEventListener("click", () => modal.classList.add("hidden"));

formCampania.addEventListener("submit", (e) => {
  e.preventDefault();
  manager.agregar(
    formCampania.nombre.value,
    formCampania.fechaInicio.value,
    formCampania.fechaFin.value
  );
  formCampania.reset();
  modal.classList.add("hidden");

  // Re-render después de crear
  manager.render("creador");
});

// === CREAR PREGUNTA ===
btnNuevaPregunta.addEventListener("click", () => modalPregunta.classList.remove("hidden"));
btnCerrarPregunta.addEventListener("click", () => modalPregunta.classList.add("hidden"));

formPregunta.addEventListener("submit", (e) => {
  e.preventDefault();
  preguntasManager.agregarPregunta(formPregunta.textoPregunta.value);
  formPregunta.reset();
  modalPregunta.classList.add("hidden");
});

// === MOSTRAR PREGUNTAS ===
function mostrarPreguntas(id, modo) {
  seccionPreguntas.classList.remove("hidden");
  seccionCreador.classList.add("hidden");
  preguntasManager.mostrarPreguntas(id, modo);
}
