import asyncio
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("MONGO_URI")


class ModuloProduccion:

    def __init__(self):
        self.client = AsyncIOMotorClient(URI)
        self.db = self.client.granja_porcina
        self.coleccion_pesajes = self.db.pesajes
        self.coleccion_indicadores = self.db.indicadores_produccion
        # Colecciones de otros módulos (para cruzar datos)
        self.coleccion_consumo = self.db.consumo_alimento
        self.coleccion_mortalidad = self.db.mortalidad

    

    async def registrar_pesaje(
        self,
        numero_lote: str,
        peso_promedio_kg: float,
        cantidad_animales_pesados: int,
    ):
        """
        Registra un pesaje programado del lote (cada dos semanas).
        Después de guardar el pesaje, calcula y guarda los indicadores
        automáticamente.

        Parámetros:
            numero_lote              : identificador del lote
            peso_promedio_kg         : peso promedio del lote en este pesaje
            cantidad_animales_pesados: número de animales que se pesaron
        """

        pesaje = {
            "numero_lote": numero_lote,
            "fecha_pesaje": datetime.now().strftime("%Y-%m-%d"),
            "peso_promedio_kg": peso_promedio_kg,
            "cantidad_animales_pesados": cantidad_animales_pesados,
        }

        await self.coleccion_pesajes.insert_one(pesaje)
        print(f"✔ Pesaje registrado para '{numero_lote}': {peso_promedio_kg} kg promedio ({cantidad_animales_pesados} animales).")

        # Calcular y guardar indicadores automáticamente
        await self.calcular_y_guardar_indicadores(numero_lote, peso_promedio_kg)

    async def consultar_pesajes(self, numero_lote: str):
        """Muestra el historial de pesajes de un lote."""

        pesajes = await self.coleccion_pesajes.find(
            {"numero_lote": numero_lote}
        ).to_list(100)

        if not pesajes:
            print(f"No hay pesajes registrados para el lote '{numero_lote}'.")
            return []

        print(f"\n===== HISTORIAL DE PESAJES — {numero_lote} =====")
        print(f"{'Fecha':<12} {'Peso promedio (kg)':<22} {'Animales pesados'}")
        print("-" * 55)
        for p in pesajes:
            print(
                f"{p['fecha_pesaje']:<12} "
                f"{p['peso_promedio_kg']:<22} "
                f"{p['cantidad_animales_pesados']}"
            )

        return pesajes



    async def calcular_y_guardar_indicadores(
        self,
        numero_lote: str,
        peso_actual_kg: float,
    ):
        """
        Calcula automáticamente todos los indicadores de producción
        y los guarda en MongoDB.

        Indicadores calculados:
            - GDP  : Ganancia Diaria de Peso
            - CA   : Conversión Alimenticia
            - Mortalidad acumulada
            - Peso proyectado a mercado
        """

        
        
        pesajes = await self.coleccion_pesajes.find(
            {"numero_lote": numero_lote}
        ).to_list(100)

        gdp = None
        if len(pesajes) >= 2:
            pesaje_anterior = pesajes[-2]
            pesaje_actual = pesajes[-1]

            peso_anterior = pesaje_anterior["peso_promedio_kg"]
            fecha_anterior = datetime.strptime(pesaje_anterior["fecha_pesaje"], "%Y-%m-%d")
            fecha_actual = datetime.strptime(pesaje_actual["fecha_pesaje"], "%Y-%m-%d")
            dias_transcurridos = (fecha_actual - fecha_anterior).days

            if dias_transcurridos > 0:
                gdp = round((peso_actual_kg - peso_anterior) / dias_transcurridos, 3)

        consumos = await self.coleccion_consumo.find(
            {"numero_lote": numero_lote}
        ).to_list(500)

        ca = None
        if consumos and gdp is not None:
            total_kg_alimento = sum(r["kg_consumidos"] for r in consumos)
            # Peso ganado total = GDP × días totales desde primer pesaje
            fecha_primer_pesaje = datetime.strptime(pesajes[0]["fecha_pesaje"], "%Y-%m-%d")
            fecha_ultimo_pesaje = datetime.strptime(pesajes[-1]["fecha_pesaje"], "%Y-%m-%d")
            dias_totales = (fecha_ultimo_pesaje - fecha_primer_pesaje).days

            if dias_totales > 0:
                peso_inicial = pesajes[0]["peso_promedio_kg"]
                peso_ganado_total = peso_actual_kg - peso_inicial
                if peso_ganado_total > 0:
                    ca = round(total_kg_alimento / peso_ganado_total, 2)

        
        muertes = await self.coleccion_mortalidad.find(
            {"numero_lote": numero_lote}
        ).to_list(500)

        mortalidad_acumulada = sum(r["cantidad_muertos"] for r in muertes)
        
        peso_objetivo_kg = 110
        dias_para_mercado = None

        if gdp and gdp > 0 and peso_actual_kg < peso_objetivo_kg:
            kg_faltantes = peso_objetivo_kg - peso_actual_kg
            dias_para_mercado = round(kg_faltantes / gdp)

        
        indicadores = {
            "numero_lote": numero_lote,
            "fecha_calculo": datetime.now().strftime("%Y-%m-%d"),
            "peso_actual_kg": peso_actual_kg,
            "gdp_kg_dia": gdp,
            "conversion_alimenticia": ca,
            "mortalidad_acumulada": mortalidad_acumulada,
            "dias_estimados_para_mercado": dias_para_mercado,
            "peso_objetivo_kg": peso_objetivo_kg,
        }

        await self.coleccion_indicadores.insert_one(indicadores)

        
        print(f"\n===== INDICADORES DE PRODUCCIÓN — {numero_lote} =====")
        print(f"  Peso actual              : {peso_actual_kg} kg")
        print(f"  GDP (ganancia diaria)    : {gdp if gdp is not None else 'Se necesita otro pesaje'} kg/día")
        print(f"  Conversión alimenticia   : {ca if ca is not None else 'Pendiente'}")
        print(f"  Mortalidad acumulada     : {mortalidad_acumulada} animales")

        if dias_para_mercado is not None:
            print(f"  Días estimados a mercado : {dias_para_mercado} días")
        elif peso_actual_kg >= peso_objetivo_kg:
            print(f"  Peso proyectado a mercado: ✔ Lote listo para venta ({peso_actual_kg} kg ≥ {peso_objetivo_kg} kg)")
        else:
            print(f"  Peso proyectado a mercado: Pendiente (se necesita GDP calculado)")


    async def consultar_indicadores(self, numero_lote: str):
        """Muestra los indicadores más recientes de un lote."""

        indicadores = await self.coleccion_indicadores.find(
            {"numero_lote": numero_lote}
        ).to_list(100)

        if not indicadores:
            print(f"No hay indicadores calculados para el lote '{numero_lote}'.")
            return None

        ind = indicadores[-1]  # El más reciente

        print(f"\n===== ÚLTIMO REPORTE DE INDICADORES — {numero_lote} =====")
        print(f"  Fecha del cálculo        : {ind['fecha_calculo']}")
        print(f"  Peso actual (kg)         : {ind['peso_actual_kg']}")
        print(f"  GDP (kg/día)             : {ind['gdp_kg_dia']}")
        print(f"  Conversión alimenticia   : {ind['conversion_alimenticia']}")
        print(f"  Mortalidad acumulada     : {ind['mortalidad_acumulada']} animales")
        print(f"  Días estimados a mercado : {ind['dias_estimados_para_mercado']}")
        print(f"  Peso objetivo mercado    : {ind['peso_objetivo_kg']} kg")

        return ind

    async def comparar_indicadores_lotes(self, nombres_lotes: list):
        """
        Compara los indicadores de producción entre varios lotes.

        Parámetros:
            nombres_lotes: lista de lotes a comparar (ej: ['Lote 01', 'Lote 02'])
        """

        print("\n===== COMPARACIÓN DE INDICADORES ENTRE LOTES =====")
        print(f"{'Lote':<12} {'Peso (kg)':<12} {'GDP kg/día':<14} {'CA':<10} {'Mortalidad':<12} {'Días a mercado'}")
        print("-" * 75)

        for nombre in nombres_lotes:
            indicadores = await self.coleccion_indicadores.find(
                {"numero_lote": nombre}
            ).to_list(100)

            if not indicadores:
                print(f"{nombre:<12} Sin datos")
                continue

            ind = indicadores[-1]
            print(
                f"{nombre:<12} "
                f"{ind['peso_actual_kg']:<12} "
                f"{str(ind['gdp_kg_dia']):<14} "
                f"{str(ind['conversion_alimenticia']):<10} "
                f"{ind['mortalidad_acumulada']:<12} "
                f"{ind['dias_estimados_para_mercado']}"
            )


async def main():

    produccion = ModuloProduccion()

    
    await produccion.registrar_pesaje(
        numero_lote="Lote 01",
        peso_promedio_kg=15.0,
        cantidad_animales_pesados=50,
    )

    
    await produccion.registrar_pesaje(
        numero_lote="Lote 01",
        peso_promedio_kg=24.5,
        cantidad_animales_pesados=48,
    )

    
    await produccion.consultar_pesajes("Lote 01")

    
    await produccion.consultar_indicadores("Lote 01")

    
    await produccion.comparar_indicadores_lotes(["Lote 01", "Lote 02"])


if __name__ == "__main__":
    asyncio.run(main())