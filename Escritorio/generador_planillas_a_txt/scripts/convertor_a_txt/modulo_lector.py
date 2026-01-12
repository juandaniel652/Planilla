from convertor_a_txt.lector_planillas import convertir_archivo_completo
from convertor_a_txt.abridor_archivos import abrir_archivo

# =================================================================
#   PROCESAR PLANILLA DESDE ARCHIVO .TXT
    #1. Ingreso de datos
    
    
    
lista_de_datos_procesados = ["datos_en_formato_texto/41-60/1° Planilla, Casas 41-60; (2024).txt", 
                            "datos_en_formato_texto/41-60/2° Planilla, Casas 41-60; (2024).txt",
                            "datos_en_formato_texto/41-60/1° Planilla, Casas 41-60; (2025).txt"
                            ]    
    
# =================================================================

for i in range (len(lista_de_datos_procesados)):
    
    datos = lista_de_datos_procesados[i]
    archivos = abrir_archivo(datos)

    resultados = convertir_archivo_completo(archivos)

    for r in resultados:
        print(r, ",")
        
# =================================================================