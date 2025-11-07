export class CampañasManager {
  constructor(listaCampanias, mostrarPreguntasCallback) {
    this.listaCampanias = listaCampanias;
    this.mostrarPreguntas = mostrarPreguntasCallback;
    this.campanias = JSON.parse(localStorage.getItem("campanias")) || [];
    this.render();
  }

  agregar(nombre, inicio, fin) {
    const nueva = { id: Date.now(), nombre, inicio, fin, preguntas: [] };
    this.campanias.push(nueva);
    this.guardar();
    this.render();
  }

  guardar() {
    localStorage.setItem("campanias", JSON.stringify(this.campanias));
  }

  render(modo = "creador") {
    this.listaCampanias.innerHTML = "";
    if (this.campanias.length === 0) {
      this.listaCampanias.innerHTML = '<p class="text-gray-500">No hay campañas creadas.</p>';
      return;
    }

    this.campanias.forEach((c) => {
      const btn = document.createElement("button");
      btn.textContent = `${c.nombre}`;
      btn.className =
        "bg-indigo-500 hover:bg-indigo-600 text-white font-semibold py-2 px-3 rounded-lg shadow";
      btn.addEventListener("click", () => this.mostrarPreguntas(c.id, modo));
      this.listaCampanias.appendChild(btn);
    });
  }

  obtener(id) {
    return this.campanias.find((c) => c.id === id);
  }

  actualizar(campania) {
    const i = this.campanias.findIndex((c) => c.id === campania.id);
    if (i !== -1) {
      this.campanias[i] = campania;
      this.guardar();
    }
  }
}
