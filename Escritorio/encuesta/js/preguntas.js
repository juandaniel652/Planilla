export class PreguntasManager {
  constructor(contenedor, titulo, resumen, campañasManager) {
    this.contenedor = contenedor;
    this.titulo = titulo;
    this.resumen = resumen;
    this.campañasManager = campañasManager;
    this.campania = null;
    this.modo = "creador";
  }

  mostrarPreguntas(id, modo) {
    this.modo = modo;
    this.campania = this.campañasManager.obtener(id);
    this.titulo.textContent = `Campaña: ${this.campania.nombre}`;
    this.resumen.classList.add("hidden");
    this.contenedor.innerHTML = "";

    if (this.campania.preguntas.length === 0) {
      this.contenedor.innerHTML = "<p class='text-gray-500'>Sin preguntas todavía.</p>";
      return;
    }

    this.campania.preguntas.forEach((p) => this.agregarPreguntaDOM(p));
    document.getElementById("seccionPreguntas").classList.remove("hidden");
  }

  agregarPregunta(texto) {
    if (!this.campania) return;
    const nueva = { id: Date.now(), texto, valor: 0, votos: [] };
    this.campania.preguntas.push(nueva);
    this.campañasManager.actualizar(this.campania);
    this.agregarPreguntaDOM(nueva);
  }

  agregarPreguntaDOM(p) {
    const div = document.createElement("div");
    div.className =
      "p-4 border rounded-lg shadow-sm hover:shadow-md transition bg-white";

    const texto = document.createElement("p");
    texto.textContent = p.texto;
    texto.className = "font-medium mb-3 text-gray-800";

    div.appendChild(texto);

    const rating = document.createElement("div");
    rating.className = "flex gap-3 text-3xl justify-center";

    // Escala de 1 a 5 con emojis
    const emojis = ["😡", "😕", "😐", "🙂", "😍"];

    emojis.forEach((emoji, index) => {
      const span = document.createElement("span");
      span.textContent = emoji;
      span.className =
        "cursor-pointer transform hover:scale-125 transition-transform";
      span.dataset.valor = index + 1;

      if (this.modo === "evaluador") {
        span.addEventListener("click", () =>
          this.valorar(p.id, index + 1, rating)
        );
      } else {
        span.classList.add("opacity-40");
      }

      rating.appendChild(span);
    });

    div.appendChild(rating);
    this.contenedor.appendChild(div);
  }

  valorar(idPregunta, valor, contenedor) {
    const pregunta = this.campania.preguntas.find((x) => x.id === idPregunta);
    if (!pregunta) return;
    pregunta.votos.push(valor);
    pregunta.valor = this.promedio(pregunta.votos);
    this.campañasManager.actualizar(this.campania);
    this.mostrarPromedios();

    // Actualiza el estado visual
    contenedor.querySelectorAll("span").forEach((span, i) => {
      span.classList.toggle("opacity-100", i + 1 === valor);
      span.classList.toggle("opacity-50", i + 1 !== valor);
    });
  }

  mostrarPromedios() {
    const total = this.campania.preguntas.reduce(
      (sum, p) => sum + (p.valor || 0),
      0
    );
    const promedio = total / this.campania.preguntas.length || 0;
    this.resumen.classList.remove("hidden");
    this.resumen.innerHTML = `
      <p class="text-lg font-semibold text-gray-700">Promedio general:
        <span class="text-yellow-500 text-xl">${promedio.toFixed(1)} / 5</span>
      </p>`;
  }

  promedio(arr) {
    return arr.reduce((a, b) => a + b, 0) / arr.length;
  }
}
