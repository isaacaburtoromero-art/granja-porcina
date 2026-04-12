import asyncio
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("MONGO_URI")


class ModuloSanidad:

    def __init__(self):
        self.client = AsyncIOMotorClient(URI)
        self.db = self.client.granja_porcina
        self.coleccion_historial = self.db.historial_sanitario
        self.coleccion_bioseguridad = self.db.bioseguridad
        self.coleccion_mortalidad = self.db.mortalidad



    async def registrar_vacuna_o_tratamiento(
        self,
        numero_lote: str,
        tipo_medicamento: str,
        fecha_aplicacion: str,
        dosis: str,
        observaciones: str,
    ):
        """
        Registra una vacuna o tratamiento aplicado a un lote.

        Parámetros:
            numero_lote      : identificador del lote (ej: 'Lote 01')
            tipo_medicamento : nombre del medicamento o vacuna
            fecha_aplicacion : fecha en formato 'YYYY-MM-DD'
            dosis            : dosis aplicada (ej: '2 ml por animal')
            observaciones    : notas adicionales del veterinario
        """

        registro = {
            "numero_lote": numero_lote,
            "tipo_medicamento": tipo_medicamento,
            "fecha_aplicacion": fecha_aplicacion,
            "dosis": dosis,
            "observaciones": observaciones,
            "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }

        await self.coleccion_historial.insert_one(registro)
        print(f"✔ Tratamiento '{tipo_medicamento}' registrado para el lote '{numero_lote}'.")

    async def consultar_historial_sanitario(self, numero_lote: str):
        """Muestra todo el historial de vacunas y tratamientos de un lote."""

        registros = await self.coleccion_historial.find(
            {"numero_lote": numero_lote}
        ).to_list(100)

        if not registros:
            print(f"No hay historial sanitario para el lote '{numero_lote}'.")
            return

        print(f"\n===== HISTORIAL SANITARIO — {numero_lote} =====")
        print(f"{'Medicamento':<25} {'Fecha':<12} {'Dosis':<20} {'Observaciones'}")
        print("-" * 80)
        for r in registros:
            print(
                f"{r['tipo_medicamento']:<25} "
                f"{r['fecha_aplicacion']:<12} "
                f"{r['dosis']:<20} "
                f"{r['observaciones']}"
            )



    async def registrar_protocolo_bioseguridad(
        self,
        numero_lote: str,
        tipo_protocolo: str,
        observaciones: str = "",
    ):
        """
        Registra un protocolo de bioseguridad aplicado a un lote.

        Tipos de protocolo válidos:
            - 'limpieza'
            - 'desinfeccion_corral'
            - 'manejo_residuos_aguas'
            - 'acceso_personal'
            - 'acceso_visitantes'
        """

        tipos_validos = [
            "limpieza",
            "desinfeccion_corral",
            "manejo_residuos_aguas",
            "acceso_personal",
            "acceso_visitantes",
        ]

        if tipo_protocolo not in tipos_validos:
            print(f"⚠ Tipo de protocolo no válido. Opciones: {tipos_validos}")
            return

        protocolo = {
            "numero_lote": numero_lote,
            "tipo_protocolo": tipo_protocolo,
            "fecha_aplicacion": datetime.now().strftime("%Y-%m-%d"),
            "observaciones": observaciones,
        }

        await self.coleccion_bioseguridad.insert_one(protocolo)
        print(f"✔ Protocolo '{tipo_protocolo}' registrado para el lote '{numero_lote}'.")

    async def consultar_protocolos_bioseguridad(self, numero_lote: str):
        """Muestra todos los protocolos de bioseguridad de un lote."""

        protocolos = await self.coleccion_bioseguridad.find(
            {"numero_lote": numero_lote}
        ).to_list(100)

        if not protocolos:
            print(f"No hay protocolos de bioseguridad para el lote '{numero_lote}'.")
            return

        print(f"\n===== PROTOCOLOS DE BIOSEGURIDAD — {numero_lote} =====")
        print(f"{'Tipo de protocolo':<25} {'Fecha':<12} {'Observaciones'}")
        print("-" * 65)
        for p in protocolos:
            print(
                f"{p['tipo_protocolo']:<25} "
                f"{p['fecha_aplicacion']:<12} "
                f"{p['observaciones']}"
            )

    
    
    

    async def registrar_muerte(
        self,
        numero_lote: str,
        cantidad_muertos: int,
        causa: str,
    ):
        """
        Registra la muerte de animales en un lote.

        Parámetros:
            numero_lote      : identificador del lote
            cantidad_muertos : número de animales muertos en este evento
            causa            : causa de la muerte (ej: 'enfermedad respiratoria')
        """

        registro = {
            "numero_lote": numero_lote,
            "cantidad_muertos": cantidad_muertos,
            "causa": causa,
            "fecha": datetime.now().strftime("%Y-%m-%d"),
        }

        await self.coleccion_mortalidad.insert_one(registro)
        print(f"✔ Mortalidad registrada: {cantidad_muertos} animal(es) en lote '{numero_lote}'. Causa: {causa}")

    async def consultar_mortalidad_lote(self, numero_lote: str):
        """Muestra el historial de muertes de un lote y el total acumulado."""

        registros = await self.coleccion_mortalidad.find(
            {"numero_lote": numero_lote}
        ).to_list(100)

        if not registros:
            print(f"No hay registros de mortalidad para el lote '{numero_lote}'.")
            return 0

        total = sum(r["cantidad_muertos"] for r in registros)

        print(f"\n===== MORTALIDAD ACUMULADA — {numero_lote} =====")
        print(f"{'Fecha':<12} {'Muertos':<10} {'Causa'}")
        print("-" * 50)
        for r in registros:
            print(f"{r['fecha']:<12} {r['cantidad_muertos']:<10} {r['causa']}")
        print("-" * 50)
        print(f"  TOTAL ACUMULADO: {total} animales muertos")

        return total

    async def mortalidad_total_granja(self):
        """Calcula y muestra la mortalidad acumulada de toda la granja."""

        registros = await self.coleccion_mortalidad.find().to_list(500)

        if not registros:
            print("No hay registros de mortalidad en la granja.")
            return

        
        resumen = {}
        for r in registros:
            lote = r["numero_lote"]
            resumen[lote] = resumen.get(lote, 0) + r["cantidad_muertos"]

        print("\n===== MORTALIDAD TOTAL DE LA GRANJA =====")
        print(f"{'Lote':<15} {'Total muertos'}")
        print("-" * 30)
        for lote, total in resumen.items():
            print(f"{lote:<15} {total}")
        print("-" * 30)
        print(f"  GRAN TOTAL: {sum(resumen.values())} animales")




async def main():

    sanidad = ModuloSanidad()

    
    await sanidad.registrar_vacuna_o_tratamiento(
        numero_lote="Lote 01",
        tipo_medicamento="Vacuna Circovirus",
        fecha_aplicacion="2026-03-15",
        dosis="2 ml por animal",
        observaciones="Aplicada sin complicaciones",
    )

    await sanidad.registrar_vacuna_o_tratamiento(
        numero_lote="Lote 01",
        tipo_medicamento="Antibiótico Amoxicilina",
        fecha_aplicacion="2026-03-20",
        dosis="1 ml por cada 10 kg",
        observaciones="Tratamiento preventivo por brote leve",
    )

    
    await sanidad.consultar_historial_sanitario("Lote 01")

    
    await sanidad.registrar_protocolo_bioseguridad(
        numero_lote="Lote 01",
        tipo_protocolo="limpieza",
        observaciones="Limpieza general del corral",
    )

    await sanidad.registrar_protocolo_bioseguridad(
        numero_lote="Lote 01",
        tipo_protocolo="desinfeccion_corral",
        observaciones="Desinfección con formol al 2%",
    )

    
    await sanidad.consultar_protocolos_bioseguridad("Lote 01")

    
    await sanidad.registrar_muerte(
        numero_lote="Lote 01",
        cantidad_muertos=2,
        causa="Enfermedad respiratoria",
    )

    
    await sanidad.consultar_mortalidad_lote("Lote 01")


    await sanidad.mortalidad_total_granja()


if __name__ == "__main__":
    asyncio.run(main())