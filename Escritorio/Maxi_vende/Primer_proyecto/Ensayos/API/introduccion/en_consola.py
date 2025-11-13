import requests

# URL de la API
url = "https://jsonplaceholder.typicode.com/posts"

# Hacer la solicitud GET (obtener datos)
response = requests.get(url)

# Verificamos si la respuesta fue exitosa
if response.status_code == 200:
    datos = response.json()  # Convertimos la respuesta en un diccionario/lista
    for post in datos[:5]:  # Mostramos solo los primeros 5
        print(f"Título: {post['title']}\nContenido: {post['body']}\n")
else:
    print("Error al obtener los datos:", response.status_code)
