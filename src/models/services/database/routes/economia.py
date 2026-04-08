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


    async def registrar_datos(self, datos_lote):


        costo_total = sum(datos_lote["costos"].values())
        ingreso_total = sum(datos_lote["ingresos"].values())
        rentabilidad = ingreso_total - costo_total

        engorde = datos_lote["peso_final"] - datos_lote["peso_inicial"]

        mortalidad = (
            datos_lote["cantidad_inicial"]
            - datos_lote["cantidad_final"]
        )

        datos_lote["calculos"] = {
            "costo_total": costo_total,
            "ingreso_total": ingreso_total,
            "rentabilidad_neta": rentabilidad,
            "engorde": engorde,
            "mortalidad": mortalidad
        }


        await self.coleccion.insert_one(datos_lote)

        print("Datos guardados correctamente en MongoDB")
        print("Rentabilidad:", rentabilidad)

        plt.bar(
            ["Costos", "Ingresos"],
            [costo_total, ingreso_total]
        )

        plt.title(f"Costos vs Ingresos ({datos_lote['lote']})")
        plt.show()

        plt.bar(
            ["Peso inicial", "Peso final"],
            [datos_lote["peso_inicial"], datos_lote["peso_final"]]
        )

        plt.title(f"Engorde del {datos_lote['lote']}")
        plt.show()


        plt.bar(
            ["Inicial", "Final"],
            [
                datos_lote["cantidad_inicial"],
                datos_lote["cantidad_final"]
            ]
        )

        plt.title(f"Mortalidad del {datos_lote['lote']}")
        plt.show()


        print(
            "Consumo total de alimento:",
            datos_lote["consumo_alimento"]
        )


    async def generar_reporte_comparativo(self):

        datos = await self.coleccion.find().to_list(100)

        if not datos:
            print("No hay datos registrados.")
            return


        df = pd.DataFrame([

            {
                "Lote": d["lote"],
                "Costo total": d["calculos"]["costo_total"],
                "Ingreso total": d["calculos"]["ingreso_total"],
                "Rentabilidad": d["calculos"]["rentabilidad_neta"]
            }

            for d in datos

        ])


        print("\nTABLA COMPARATIVA DE RENTABILIDAD")
        print(df)


        plt.bar(
            df["Lote"],
            df["Rentabilidad"]
        )

        plt.title("Comparación de Rentabilidad entre Lotes")
        plt.ylabel("Ganancia Neta")

        plt.show()

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
        "otros": 100
    },


    "ingresos": {

        "venta_animales": 2500,
        "subproductos": 200,
        "subsidios": 300
    }

}


async def main():

    economia = ModuloEconomia()

    await economia.registrar_datos(ejemplo_datos)

    await economia.generar_reporte_comparativo()


if __name__ == "__main__":
    asyncio.run(main())
