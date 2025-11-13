import tkinter as tk
import requests

def obtener_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    if response.status_code == 200:
        datos = response.json()
        texto.delete("1.0", tk.END)  # Borramos el contenido anterior
        for post in datos[:5]:
            texto.insert(tk.END, f"Título: {post['title']}\n{post['body']}\n\n")
    else:
        texto.insert(tk.END, "Error al obtener los datos.")

# Crear la ventana
ventana = tk.Tk()
ventana.title("Lector de API")

boton = tk.Button(ventana, text="Cargar Posts", command=obtener_posts)
boton.pack(pady=10)

texto = tk.Text(ventana, wrap="word", width=60, height=20)
texto.pack()

ventana.mainloop()
