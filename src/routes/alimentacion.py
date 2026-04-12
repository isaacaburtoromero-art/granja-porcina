import asyncio
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("MONGO_URI")


# ------------------------------------------------------------------ #
# TABLA NUTRICIONAL PREDEFINIDA                                        #
# Cada etapa define los requerimientos nutricionales y la ración      #
# diaria como porcentaje del peso vivo del animal.                    #
# ------------------------------------------------------------------ #

TABLA_NUTRICIONAL = {
    "destete": {
        "descripcion": "Lechones destetados (7-28 días, 6-10 kg)",
        "proteina_pct": 20.0,       # % de proteína en el alimento
        "energia_kcal_kg": 3400,    # energía metabolizable kcal/kg
        "vitaminas": "A, D3, E, B12",
        "racion_pct_peso": 0.08,    # 8% del peso vivo por día
        "ganancia_diaria_obj_kg": 0.25,
    },
    "precebo": {
        "descripcion": "Precebo (28-70 días, 10-30 kg)",
        "proteina_pct": 18.0,
        "energia_kcal_kg": 3300,
        "vitaminas": "A, D3, E",
        "racion_pct_peso": 0.06,    # 6% del peso vivo por día
        "ganancia_diaria_obj_kg": 0.45,
    },
    "cebo": {
        "descripcion": "Cebo (70-160 días, 30-80 kg)",
        "proteina_pct": 16.0,
        "energia_kcal_kg": 3200,
        "vitaminas": "A, D3",
        "racion_pct_peso": 0.04,    # 4% del peso vivo por día
        "ganancia_diaria_obj_kg": 0.70,
    },
    "engorde_final": {
        "descripcion": "Engorde final (160+ días, 80-120 kg)",
        "proteina_pct": 14.0,
        "energia_kcal_kg": 3100,
        "vitaminas": "A, D3",
        "racion_pct_peso": 0.03,    # 3% del peso vivo por día
        "ganancia_diaria_obj_kg": 0.80,
    },
}


class ModuloAlimentacion:

    def __init__(self):
        self.client = AsyncIOMotorClient(URI)
        self.db = self.client.granja_porcina
        self.coleccion_planes = self.db.planes_alimentacion
        self.coleccion_consumo = self.db.consumo_alimento

    # ------------------------------------------------------------------ #
    # CONSULTA DE TABLA NUTRICIONAL                                        #
    # ------------------------------------------------------------------ #

    def consultar_tabla_nutricional(self):
        """Muestra la tabla nutricional completa con todas las etapas."""

        print("\n===== TABLA NUTRICIONAL — GRANJA PORCINA =====")
        print(f"{'Etapa':<16} {'Proteína %':<12} {'Energía kcal/kg':<18} {'Ración % peso':<15} {'GDP objetivo kg/día'}")
        print("-" * 80)
        for etapa, datos in TABLA_NUTRICIONAL.items():
            print(
                f"{etapa:<16} "
                f"{datos['proteina_pct']:<12} "
                f"{datos['energia_kcal_kg']:<18} "
                f"{datos['racion_pct_peso'] * 100:.0f}%{'':<11} "
                f"{datos['ganancia_diaria_obj_kg']}"
            )

    # ------------------------------------------------------------------ #
    # GENERACIÓN AUTOMÁTICA DE RACIÓN DIARIA                              #
    # ------------------------------------------------------------------ #

    def calcular_racion_diaria(
        self,
        etapa_productiva: str,
        peso_promedio_kg: float,
        cantidad_animales: int,
    ) -> dict:
        """
        Calcula automáticamente la ración diaria para un lote.

        Fórmula:
            ración por animal (kg) = peso_promedio_kg × racion_pct_peso
            ración total lote (kg) = ración por animal × cantidad_animales

        Retorna un diccionario con todos los valores calculados.
        """

        if etapa_productiva not in TABLA_NUTRICIONAL:
            print(f"⚠ Etapa '{etapa_productiva}' no válida.")
            return {}

        nutricion = TABLA_NUTRICIONAL[etapa_productiva]

        racion_por_animal_kg = round(peso_promedio_kg * nutricion["racion_pct_peso"], 2)
        racion_total_lote_kg = round(racion_por_animal_kg * cantidad_animales, 2)

        resultado = {
            "etapa": etapa_productiva,
            "peso_promedio_kg": peso_promedio_kg,
            "cantidad_animales": cantidad_animales,
            "racion_por_animal_kg": racion_por_animal_kg,
            "racion_total_lote_kg": racion_total_lote_kg,
            "proteina_pct": nutricion["proteina_pct"],
            "energia_kcal_kg": nutricion["energia_kcal_kg"],
            "vitaminas": nutricion["vitaminas"],
            "ganancia_diaria_obj_kg": nutricion["ganancia_diaria_obj_kg"],
        }

        return resultado

    # ------------------------------------------------------------------ #
    # REGISTRO DE PLAN DE ALIMENTACIÓN                                     #
    # ------------------------------------------------------------------ #

    async def registrar_plan_alimentacion(
        self,
        numero_lote: str,
        etapa_productiva: str,
        peso_promedio_kg: float,
        cantidad_animales: int,
    ):
        """
        Genera automáticamente y guarda el plan de alimentación
        de un lote en MongoDB.
        """

        racion = self.calcular_racion_diaria(
            etapa_productiva, peso_promedio_kg, cantidad_animales
        )

        if not racion:
            return

        plan = {
            "numero_lote": numero_lote,
            "fecha_plan": datetime.now().strftime("%Y-%m-%d"),
            "etapa_productiva": etapa_productiva,
            "peso_promedio_kg": peso_promedio_kg,
            "cantidad_animales": cantidad_animales,
            "racion_por_animal_kg": racion["racion_por_animal_kg"],
            "racion_total_lote_kg": racion["racion_total_lote_kg"],
            "proteina_pct": racion["proteina_pct"],
            "energia_kcal_kg": racion["energia_kcal_kg"],
            "vitaminas": racion["vitaminas"],
            "ganancia_diaria_objetivo_kg": racion["ganancia_diaria_obj_kg"],
        }

        await self.coleccion_planes.insert_one(plan)

        print(f"\n✔ Plan de alimentación registrado para '{numero_lote}'.")
        print(f"  Etapa            : {etapa_productiva}")
        print(f"  Ración/animal    : {racion['racion_por_animal_kg']} kg/día")
        print(f"  Ración total lote: {racion['racion_total_lote_kg']} kg/día")
        print(f"  Proteína         : {racion['proteina_pct']}%")
        print(f"  Energía          : {racion['energia_kcal_kg']} kcal/kg")
        print(f"  Vitaminas        : {racion['vitaminas']}")
        print(f"  GDP objetivo     : {racion['ganancia_diaria_obj_kg']} kg/día")

    async def consultar_plan_alimentacion(self, numero_lote: str):
        """Muestra el plan de alimentación más reciente de un lote."""

        planes = await self.coleccion_planes.find(
            {"numero_lote": numero_lote}
        ).to_list(100)

        if not planes:
            print(f"No hay planes de alimentación para el lote '{numero_lote}'.")
            return None

        # Mostrar el más reciente
        plan = planes[-1]

        print(f"\n===== PLAN DE ALIMENTACIÓN — {numero_lote} =====")
        print(f"  Fecha del plan     : {plan['fecha_plan']}")
        print(f"  Etapa productiva   : {plan['etapa_productiva']}")
        print(f"  Peso promedio (kg) : {plan['peso_promedio_kg']}")
        print(f"  Cantidad animales  : {plan['cantidad_animales']}")
        print(f"  Ración/animal/día  : {plan['racion_por_animal_kg']} kg")
        print(f"  Ración total/día   : {plan['racion_total_lote_kg']} kg")
        print(f"  Proteína           : {plan['proteina_pct']}%")
        print(f"  Energía            : {plan['energia_kcal_kg']} kcal/kg")
        print(f"  Vitaminas          : {plan['vitaminas']}")
        print(f"  GDP objetivo       : {plan['ganancia_diaria_objetivo_kg']} kg/día")

        return plan

    # ------------------------------------------------------------------ #
    # REGISTRO DE CONSUMO REAL                                             #
    # ------------------------------------------------------------------ #

    async def registrar_consumo(
        self,
        numero_lote: str,
        fecha: str,
        kg_consumidos: float,
        precio_kg: float,
    ):
        """
        Registra el consumo real de alimento de un lote en un día.

        Parámetros:
            numero_lote  : identificador del lote
            fecha        : fecha del consumo 'YYYY-MM-DD'
            kg_consumidos: kilogramos consumidos ese día
            precio_kg    : precio por kilogramo del alimento ($)
        """

        costo_dia = round(kg_consumidos * precio_kg, 2)

        consumo = {
            "numero_lote": numero_lote,
            "fecha": fecha,
            "kg_consumidos": kg_consumidos,
            "precio_kg": precio_kg,
            "costo_dia": costo_dia,
        }

        await self.coleccion_consumo.insert_one(consumo)
        print(f"✔ Consumo registrado: {kg_consumidos} kg el {fecha} — Costo: ${costo_dia}")

    async def consumo_total_lote(self, numero_lote: str):
        """Calcula y muestra el consumo total acumulado de alimento de un lote."""

        registros = await self.coleccion_consumo.find(
            {"numero_lote": numero_lote}
        ).to_list(500)

        if not registros:
            print(f"No hay registros de consumo para el lote '{numero_lote}'.")
            return 0, 0

        total_kg = round(sum(r["kg_consumidos"] for r in registros), 2)
        total_costo = round(sum(r["costo_dia"] for r in registros), 2)

        print(f"\n===== CONSUMO TOTAL DE ALIMENTO — {numero_lote} =====")
        print(f"{'Fecha':<12} {'Kg consumidos':<16} {'Precio/kg':<12} {'Costo día'}")
        print("-" * 55)
        for r in registros:
            print(
                f"{r['fecha']:<12} "
                f"{r['kg_consumidos']:<16} "
                f"${r['precio_kg']:<11} "
                f"${r['costo_dia']}"
            )
        print("-" * 55)
        print(f"  TOTAL KG   : {total_kg} kg")
        print(f"  COSTO TOTAL: ${total_costo}")

        return total_kg, total_costo


# ------------------------------------------------------------------ #
# EJECUCIÓN DE PRUEBA                                                  #
# ------------------------------------------------------------------ #

async def main():

    alimentacion = ModuloAlimentacion()

    # Ver la tabla nutricional completa
    alimentacion.consultar_tabla_nutricional()

    # Generar y registrar plan de alimentación para un lote
    await alimentacion.registrar_plan_alimentacion(
        numero_lote="Lote 01",
        etapa_productiva="precebo",
        peso_promedio_kg=15.0,
        cantidad_animales=50,
    )

    await alimentacion.registrar_plan_alimentacion(
        numero_lote="Lote 02",
        etapa_productiva="cebo",
        peso_promedio_kg=55.0,
        cantidad_animales=40,
    )

    # Consultar el plan de un lote
    await alimentacion.consultar_plan_alimentacion("Lote 01")

    # Registrar consumo real de alimento
    await alimentacion.registrar_consumo(
        numero_lote="Lote 01",
        fecha="2026-04-01",
        kg_consumidos=45.0,
        precio_kg=0.85,
    )

    await alimentacion.registrar_consumo(
        numero_lote="Lote 01",
        fecha="2026-04-02",
        kg_consumidos=46.5,
        precio_kg=0.85,
    )

    # Ver consumo total acumulado
    await alimentacion.consumo_total_lote("Lote 01")


if __name__ == "__main__":
    asyncio.run(main())