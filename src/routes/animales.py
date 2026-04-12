from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("MONGO_URI")


class ModuloAnimales:

    def __init__(self):
        self.client = AsyncIOMotorClient(URI)
        self.db = self.client.granja_porcina
        self.coleccion = self.db.animales

 

    async def registrar_lote(
        self,
        numero_lote: str,
        cantidad_animales: int,
        edad_dias: int,
        peso_promedio_kg: float,
        etapa_productiva: str,
    ):
        """
        Registra un nuevo lote de cerdos en el sistema.

        Etapas productivas válidas:
            - 'destete'       (7 - 28 días, 6 - 10 kg)
            - 'precebo'       (28 - 70 días, 10 - 30 kg)
            - 'cebo'          (70 - 160 días, 30 - 100 kg)
            - 'engorde_final' (160+ días, 100 - 120 kg)
        """

        etapas_validas = ["destete", "precebo", "cebo", "engorde_final"]
        if etapa_productiva not in etapas_validas:
            print(f"⚠ Etapa no válida. Opciones: {etapas_validas}")
            return

        # Verificar si el lote ya existe
        existente = await self.coleccion.find_one({"numero_lote": numero_lote})
        if existente:
            print(f"⚠ El lote '{numero_lote}' ya está registrado.")
            return

        lote = {
            "numero_lote": numero_lote,
            "fecha_ingreso": datetime.now().strftime("%Y-%m-%d"),
            "cantidad_animales": cantidad_animales,
            "edad_dias": edad_dias,
            "peso_promedio_kg": peso_promedio_kg,
            "etapa_productiva": etapa_productiva,
            "estado": "activo",  # activo | vendido | baja
        }

        await self.coleccion.insert_one(lote)
        print(f"✔ Lote '{numero_lote}' registrado exitosamente.")
        print(f"  Animales: {cantidad_animales} | Peso promedio: {peso_promedio_kg} kg | Etapa: {etapa_productiva}")



    async def consultar_lote(self, numero_lote: str):
        """Muestra la información completa de un lote."""

        lote = await self.coleccion.find_one({"numero_lote": numero_lote})
        if not lote:
            print(f"No se encontró el lote '{numero_lote}'.")
            return None

        print(f"\n===== INFORMACIÓN DEL LOTE: {numero_lote} =====")
        print(f"  Fecha de ingreso   : {lote['fecha_ingreso']}")
        print(f"  Cantidad de animales: {lote['cantidad_animales']}")
        print(f"  Edad (días)        : {lote['edad_dias']}")
        print(f"  Peso promedio (kg) : {lote['peso_promedio_kg']}")
        print(f"  Etapa productiva   : {lote['etapa_productiva']}")
        print(f"  Estado             : {lote['estado']}")
        return lote

    async def listar_lotes_activos(self):
        """Lista todos los lotes que están activos en la granja."""

        lotes = await self.coleccion.find({"estado": "activo"}).to_list(100)
        if not lotes:
            print("No hay lotes activos registrados.")
            return

        print("\n===== LOTES ACTIVOS EN LA GRANJA =====")
        print(f"{'Lote':<12} {'Ingreso':<12} {'Animales':<10} {'Peso (kg)':<12} {'Etapa':<15} {'Estado'}")
        print("-" * 70)
        for lote in lotes:
            print(
                f"{lote['numero_lote']:<12} "
                f"{lote['fecha_ingreso']:<12} "
                f"{lote['cantidad_animales']:<10} "
                f"{lote['peso_promedio_kg']:<12} "
                f"{lote['etapa_productiva']:<15} "
                f"{lote['estado']}"
            )

 

    async def actualizar_peso(self, numero_lote: str, nuevo_peso_kg: float):
        """Actualiza el peso promedio de un lote."""

        resultado = await self.coleccion.update_one(
            {"numero_lote": numero_lote},
            {"$set": {"peso_promedio_kg": nuevo_peso_kg}}
        )
        if resultado.modified_count > 0:
            print(f"✔ Peso del lote '{numero_lote}' actualizado a {nuevo_peso_kg} kg.")
        else:
            print(f"No se encontró el lote '{numero_lote}'.")

    async def actualizar_etapa(self, numero_lote: str, nueva_etapa: str):
        """Actualiza la etapa productiva de un lote."""

        etapas_validas = ["destete", "precebo", "cebo", "engorde_final"]
        if nueva_etapa not in etapas_validas:
            print(f"⚠ Etapa no válida. Opciones: {etapas_validas}")
            return

        resultado = await self.coleccion.update_one(
            {"numero_lote": numero_lote},
            {"$set": {"etapa_productiva": nueva_etapa}}
        )
        if resultado.modified_count > 0:
            print(f"✔ Etapa del lote '{numero_lote}' actualizada a '{nueva_etapa}'.")
        else:
            print(f"No se encontró el lote '{numero_lote}'.")

    async def registrar_salida_mercado(self, numero_lote: str):
        """Marca un lote como vendido (salida a mercado)."""

        resultado = await self.coleccion.update_one(
            {"numero_lote": numero_lote},
            {
                "$set": {
                    "estado": "vendido",
                    "fecha_salida": datetime.now().strftime("%Y-%m-%d"),
                }
            }
        )
        if resultado.modified_count > 0:
            print(f"✔ Lote '{numero_lote}' marcado como vendido.")
        else:
            print(f"No se encontró el lote '{numero_lote}'.")




async def main():

    animales = ModuloAnimales()

    
    await animales.registrar_lote(
        numero_lote="Lote 01",
        cantidad_animales=50,
        edad_dias=30,
        peso_promedio_kg=12.5,
        etapa_productiva="precebo",
    )

    await animales.registrar_lote(
        numero_lote="Lote 02",
        cantidad_animales=40,
        edad_dias=90,
        peso_promedio_kg=55.0,
        etapa_productiva="cebo",
    )

    await animales.consultar_lote("Lote 01")

    
    await animales.listar_lotes_activos()


    await animales.actualizar_peso("Lote 01", 18.0)
    await animales.actualizar_etapa("Lote 01", "cebo")

    
    await animales.registrar_salida_mercado("Lote 02")


if __name__ == "__main__":
    asyncio.run(main())