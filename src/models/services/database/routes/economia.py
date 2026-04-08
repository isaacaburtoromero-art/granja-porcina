import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import pandas as pd
import matplotlib.pyplot as plt

URI = "mongodb+srv://eimmymolina2020_db_user:Qwertyu8@cluster0.bcbxacw.mongodb.net/?appName=Cluster0"

class ModuloEconomia:
    def __init__(self):
        self.client = AsyncIOMotorClient(URI)
        self.db = self.client.granja_porcina
        self.coleccion = self.db.finanzas

    async def registrar_y_reportar(self, datos_lote):
        # 1. Cálculos que te piden en la captura
        costos = sum(datos_lote['costos'].values())
        ingresos = sum(datos_lote['ingresos'].values())
        rentabilidad = ingresos - costos
        
        datos_completos = {
            **datos_lote,
            "calculos": {
                "costo_total": costos,
                "ingreso_total": ingresos,
                "rentabilidad_neta": rentabilidad
            }
        }


        await self.coleccion.insert_one(datos_completos)
        print(f"¡Listo! Rentabilidad calculada: {rentabilidad}")

  
        etiquetas = ['Costos', 'Ingresos']
        valores = [costos, ingresos]
        plt.bar(etiquetas, valores, color=['red', 'green'])
        plt.title(f"Reporte de {datos_lote['lote']}")
        plt.show()


ejemplo_datos = {
    "lote": "Lote #05",
    "costos": {"alimentacion": 800, "sanidad": 200, "mano_obra": 300},
    "ingresos": {"venta_animales": 2500, "subproductos": 200}
}

if __name__ == "__main__":
    modulo = ModuloEconomia()
    asyncio.run(modulo.registrar_y_reportar(ejemplo_datos))
