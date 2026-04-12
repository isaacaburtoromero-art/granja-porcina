import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("MONGO_URI")


class ModuloEconomia:

    def __init__(self):
        self.client = AsyncIOMotorClient(URI)
        self.db = self.client.granja_porcina
        self.coleccion = self.db.finanzas

    

    async def registrar_datos(self, datos_lote: dict):
        """Calcula indicadores económicos y guarda el lote en MongoDB."""

        costo_total = sum(datos_lote["costos"].values())
        ingreso_total = sum(datos_lote["ingresos"].values())
        rentabilidad = ingreso_total - costo_total
        engorde = datos_lote["peso_final"] - datos_lote["peso_inicial"]
        mortalidad = datos_lote["cantidad_inicial"] - datos_lote["cantidad_final"]

        datos_lote["calculos"] = {
            "costo_total": costo_total,
            "ingreso_total": ingreso_total,
            "rentabilidad_neta": rentabilidad,
            "engorde": engorde,
            "mortalidad": mortalidad,
        }

        await self.coleccion.insert_one(datos_lote)
        print(f"✔ Lote '{datos_lote['lote']}' guardado en MongoDB.")
        print(f"  Rentabilidad neta: {rentabilidad}")

    

    async def grafico_costos_vs_ingresos(self, nombre_lote: str):
        """Gráfico de barras: costos vs ingresos de un lote específico."""

        lote = await self.coleccion.find_one({"lote": nombre_lote})
        if not lote:
            print(f"No se encontró el lote '{nombre_lote}'.")
            return

        valores = [lote["calculos"]["costo_total"], lote["calculos"]["ingreso_total"]]
        etiquetas = ["Costos", "Ingresos"]

        plt.figure()
        plt.bar(etiquetas, valores, color=["#e74c3c", "#2ecc71"])
        plt.title(f"Costos vs Ingresos — {nombre_lote}")
        plt.ylabel("Monto ($)")
        plt.tight_layout()
        plt.show()

    async def grafico_engorde_lote(self, nombre_lote: str):
        """Gráfico de engorde (peso inicial vs final) de un lote específico."""

        lote = await self.coleccion.find_one({"lote": nombre_lote})
        if not lote:
            print(f"No se encontró el lote '{nombre_lote}'.")
            return

        plt.figure()
        plt.bar(
            ["Peso inicial (kg)", "Peso final (kg)"],
            [lote["peso_inicial"], lote["peso_final"]],
            color=["#3498db", "#f39c12"],
        )
        plt.title(f"Engorde — {nombre_lote}")
        plt.ylabel("Peso promedio (kg)")
        plt.tight_layout()
        plt.show()

    async def grafico_consumo_alimento_lote(self, nombre_lote: str):
        """Muestra el consumo total de alimento de un lote."""

        lote = await self.coleccion.find_one({"lote": nombre_lote})
        if not lote:
            print(f"No se encontró el lote '{nombre_lote}'.")
            return

        print(f"\nConsumo total de alimento — {nombre_lote}: {lote['consumo_alimento']} kg")

        plt.figure()
        plt.bar([nombre_lote], [lote["consumo_alimento"]], color="#9b59b6")
        plt.title(f"Consumo total de alimento — {nombre_lote}")
        plt.ylabel("Kilogramos")
        plt.tight_layout()
        plt.show()



    async def grafico_mortalidad_granja(self):
        """Gráfico de mortalidad acumulada de todos los lotes de la granja."""

        datos = await self.coleccion.find().to_list(100)
        if not datos:
            print("No hay datos registrados.")
            return

        lotes = [d["lote"] for d in datos]
        muertes = [d["calculos"].get("mortalidad", 0) for d in datos]

        plt.figure()
        plt.bar(lotes, muertes, color="#e67e22")
        plt.title("Mortalidad por lote — Granja completa")
        plt.ylabel("Animales muertos")
        plt.xlabel("Lote")
        plt.tight_layout()
        plt.show()



    async def tabla_comparativa_rentabilidad(self, nombres_lotes: list = None):
        """
        Tabla y gráfico comparativo de rentabilidad.
        Si se pasa una lista de nombres de lotes, filtra solo esos.
        Si no se pasa nada, muestra todos.
        """

        if nombres_lotes:
            datos = await self.coleccion.find(
                {"lote": {"$in": nombres_lotes}}
            ).to_list(100)
        else:
            datos = await self.coleccion.find().to_list(100)

        if not datos:
            print("No hay datos para los lotes indicados.")
            return

        df = pd.DataFrame([
            {
                "Lote": d["lote"],
                "Costo total ($)": d["calculos"]["costo_total"],
                "Ingreso total ($)": d["calculos"]["ingreso_total"],
                "Rentabilidad neta ($)": d["calculos"]["rentabilidad_neta"],
            }
            for d in datos
        ])

        print("\n===== TABLA COMPARATIVA DE RENTABILIDAD =====")
        print(df.to_string(index=False))

        # Gráfico comparativo
        plt.figure()
        x = range(len(df))
        ancho = 0.3
        plt.bar([i - ancho for i in x], df["Costo total ($)"], width=ancho, label="Costos", color="#e74c3c")
        plt.bar(x, df["Ingreso total ($)"], width=ancho, label="Ingresos", color="#2ecc71")
        plt.bar([i + ancho for i in x], df["Rentabilidad neta ($)"], width=ancho, label="Rentabilidad", color="#3498db")
        plt.xticks(list(x), df["Lote"])
        plt.title("Comparación de rentabilidad entre lotes")
        plt.ylabel("Monto ($)")
        plt.legend()
        plt.tight_layout()
        plt.show()




async def main():

    ejemplo_datos = {
        "lote": "Lote 05",
        "peso_inicial": 20,
        "peso_final": 95,
        "cantidad_inicial": 50,
        "cantidad_final": 48,
        "consumo_alimento": 1200,
        "costos": {
            "alimentacion": 800,
            "sanidad": 200,
            "mano_obra": 300,
            "infraestructura": 150,
            "otros": 100,
        },
        "ingresos": {
            "venta_animales": 2500,
            "subproductos": 200,
            "subsidios": 300,
        },
    }

    economia = ModuloEconomia()

 
    await economia.registrar_datos(ejemplo_datos)


    await economia.grafico_costos_vs_ingresos("Lote 05")
    await economia.grafico_engorde_lote("Lote 05")
    await economia.grafico_consumo_alimento_lote("Lote 05")


    await economia.grafico_mortalidad_granja()

  
    await economia.tabla_comparativa_rentabilidad()

  
    await economia.tabla_comparativa_rentabilidad(["Lote 05", "Lote 03"])


if __name__ == "__main__":
    asyncio.run(main())