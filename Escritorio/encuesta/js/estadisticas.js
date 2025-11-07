export class Estadisticas {
  constructor(contenedor, campañasManager) {
    this.contenedor = contenedor;
    this.campañasManager = campañasManager;
  }

  mostrar() {
    const campanias = this.campañasManager.campanias;
    this.contenedor.innerHTML = "";

    if (campanias.length === 0) {
      this.contenedor.innerHTML =
        "<p class='text-gray-500'>No hay campañas para mostrar estadísticas.</p>";
      return;
    }

    campanias.forEach((c) => {
      const promedioCampania = this.calcularPromedioCampania(c);
      const card = document.createElement("div");
      card.className =
        "p-4 border rounded-xl bg-white shadow-md hover:shadow-lg transition-all w-full max-w-md mx-auto";

      card.innerHTML = `
        <h3 class="text-lg font-semibold text-indigo-700 mb-2">${c.nombre}</h3>
        <p class="text-sm text-gray-500 mb-2">Rango: ${c.inicio} a ${c.fin}</p>
        ${
          promedioCampania
            ? `<p class="text-lg font-bold text-yellow-600">Promedio general: ${promedioCampania.toFixed(2)} / 5</p>`
            : `<p class="text-gray-400 italic">Sin respuestas aún</p>`
        }
      `;

      this.contenedor.appendChild(card);
    });
  }

  calcularPromedioCampania(campania) {
    if (!campania.preguntas || campania.preguntas.length === 0) return null;

    let total = 0;
    let cantidad = 0;

    campania.preguntas.forEach((p) => {
      if (p.votos && p.votos.length > 0) {
        const promedioPregunta = p.votos.reduce((a, b) => a + b, 0) / p.votos.length;
        total += promedioPregunta;
        cantidad++;
      }
    });

    return cantidad > 0 ? total / cantidad : null;
  }
}
