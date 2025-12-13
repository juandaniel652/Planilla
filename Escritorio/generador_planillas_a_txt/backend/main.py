import sys
import os

# Agregar la carpeta raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from db_modules.planillas.conexion_mysql import procesar_asignaciones, conectar_db, errores

app = FastAPI(title="Gestor de Asignaciones")

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5501"],  # puerto del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos
class Asignacion(BaseModel):
    numero_territorio: int
    conductor: str
    fecha_asignado: str
    fecha_completado: str
    total_abarcado: str

class ConsultaTerritorio(BaseModel):
    numero_territorio: int

# Endpoint seguro de inserción
@app.post("/asignaciones")
def crear_asignacion(asig: Asignacion):
    conexion = None
    cursor = None
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()

        # Suponiendo que ya tenés la lógica para obtener los IDs correctos:
        sql = """
        INSERT INTO Asignaciones (territorio_id, conductor_id, fecha_asignado, fecha_completado, cantidad_abarcado)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            asig.numero_territorio, 
            asig.conductor, 
            asig.fecha_asignado, 
            asig.fecha_completado, 
            asig.total_abarcado
        ))

        conexion.commit()  # CONFIRMA cambios
        return {"success": True, "message": "Asignación agregada correctamente."}

    except Exception as e:
        if conexion:
            conexion.rollback()  # REVERSA cambios si falla
        print("Error real al insertar:", e)
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()

# Endpoint para procesar todas las asignaciones
@app.post("/asignaciones/procesar")
def procesar():
    try:
        procesar_asignaciones()
        return {"success": True, "message": "Asignaciones procesadas correctamente.", "errores": errores}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint de consulta por territorio
@app.post("/asignaciones/territorio")
def consultar_asignaciones(consulta: ConsultaTerritorio):
    conexion = None
    cursor = None
    try:
        conexion = conectar_db()
        cursor = conexion.cursor()
        sql = """
        SELECT 
            c.nombre_completo AS conductor,
            a.fecha_asignado,
            a.fecha_completado,
            a.cantidad_abarcado
        FROM Asignaciones a
        JOIN Territorios t ON a.territorio_id = t.id
        JOIN Conductores c ON a.conductor_id  = c.id
        WHERE t.numero = %s;
        """
        cursor.execute(sql, (consulta.numero_territorio,))
        filas = cursor.fetchall()

        resultado = []
        for f in filas:
            resultado.append({
                "conductor": f[0],
                "fecha_asignado": f[1].strftime("%Y-%m-%d") if f[1] else None,
                "fecha_completado": f[2].strftime("%Y-%m-%d") if f[2] else None,
                "cantidad_abarcado": f[3]
            })

        resultado.sort(key=lambda x: datetime.strptime(x["fecha_asignado"], "%Y-%m-%d") if x["fecha_asignado"] else datetime.max)

        return {"success": True, "asignaciones": resultado}

    except Exception as e:
        print("Error real:", e)
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if cursor:
            cursor.close()
        if conexion and conexion.is_connected():
            conexion.close()
# Para correr el servidor:


#Backend
#source .venv/bin/activate
#uvicorn backend.main:app --reload --port 8000

#Frontend
#cd frontend
#python -m http.server 5501
