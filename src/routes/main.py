import asyncio
import sys
import os

# Agregar el directorio raíz al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from animales import ModuloAnimales
from alimentacion import ModuloAlimentacion
from sanidad import ModuloSanidad
from produccion import ModuloProduccion
from economia import ModuloEconomia


def mostrar_menu_principal():
    print("\n" + "=" * 55)
    print("   🐷  SISTEMA DE GESTIÓN DE GRANJA PORCINA  🐷")
    print("              PorkToYou Ltda.")
    print("=" * 55)
    print("  1. Gestión de Animales")
    print("  2. Alimentación")
    print("  3. Sanidad y Bioseguridad")
    print("  4. Producción e Indicadores")
    print("  5. Economía y Rentabilidad")
    print("  6. Reportes y Gráficos")
    print("  0. Salir")
    print("=" * 55)




def menu_animales():
    print("\n--- GESTIÓN DE ANIMALES ---")
    print("  1. Registrar nuevo lote")
    print("  2. Consultar lote")
    print("  3. Listar lotes activos")
    print("  4. Actualizar peso de lote")
    print("  5. Actualizar etapa productiva")
    print("  6. Registrar salida a mercado")
    print("  0. Volver al menú principal")


def menu_alimentacion():
    print("\n--- ALIMENTACIÓN ---")
    print("  1. Ver tabla nutricional")
    print("  2. Registrar plan de alimentación")
    print("  3. Consultar plan de alimentación")
    print("  4. Registrar consumo de alimento")
    print("  5. Ver consumo total de un lote")
    print("  0. Volver al menú principal")


def menu_sanidad():
    print("\n--- SANIDAD Y BIOSEGURIDAD ---")
    print("  1. Registrar vacuna o tratamiento")
    print("  2. Consultar historial sanitario")
    print("  3. Registrar protocolo de bioseguridad")
    print("  4. Consultar protocolos de bioseguridad")
    print("  5. Registrar muerte de animales")
    print("  6. Consultar mortalidad de un lote")
    print("  7. Ver mortalidad total de la granja")
    print("  0. Volver al menú principal")


def menu_produccion():
    print("\n--- PRODUCCIÓN E INDICADORES ---")
    print("  1. Registrar pesaje")
    print("  2. Consultar historial de pesajes")
    print("  3. Consultar indicadores de un lote")
    print("  4. Comparar indicadores entre lotes")
    print("  0. Volver al menú principal")


def menu_economia():
    print("\n--- ECONOMÍA Y RENTABILIDAD ---")
    print("  1. Registrar datos económicos de un lote")
    print("  2. Ver gráfico costos vs ingresos")
    print("  3. Ver gráfico de engorde")
    print("  4. Ver consumo de alimento (gráfico)")
    print("  0. Volver al menú principal")


def menu_reportes():
    print("\n--- REPORTES Y GRÁFICOS ---")
    print("  1. Gráfico de mortalidad de la granja")
    print("  2. Tabla comparativa de rentabilidad")
    print("  3. Comparación de rentabilidad entre lotes")
    print("  0. Volver al menú principal")




async def flujo_animales(animales: ModuloAnimales):
    while True:
        menu_animales()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            numero_lote = input("Número de lote: ").strip()
            cantidad = int(input("Cantidad de animales: "))
            edad = int(input("Edad en días: "))
            peso = float(input("Peso promedio (kg): "))
            print("Etapas: destete | precebo | cebo | engorde_final")
            etapa = input("Etapa productiva: ").strip()
            await animales.registrar_lote(numero_lote, cantidad, edad, peso, etapa)

        elif opcion == "2":
            numero_lote = input("Número de lote a consultar: ").strip()
            await animales.consultar_lote(numero_lote)

        elif opcion == "3":
            await animales.listar_lotes_activos()

        elif opcion == "4":
            numero_lote = input("Número de lote: ").strip()
            nuevo_peso = float(input("Nuevo peso promedio (kg): "))
            await animales.actualizar_peso(numero_lote, nuevo_peso)

        elif opcion == "5":
            numero_lote = input("Número de lote: ").strip()
            print("Etapas: destete | precebo | cebo | engorde_final")
            nueva_etapa = input("Nueva etapa productiva: ").strip()
            await animales.actualizar_etapa(numero_lote, nueva_etapa)

        elif opcion == "6":
            numero_lote = input("Número de lote: ").strip()
            await animales.registrar_salida_mercado(numero_lote)

        elif opcion == "0":
            break
        else:
            print("⚠ Opción no válida.")


async def flujo_alimentacion(alimentacion: ModuloAlimentacion):
    while True:
        menu_alimentacion()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            alimentacion.consultar_tabla_nutricional()

        elif opcion == "2":
            numero_lote = input("Número de lote: ").strip()
            print("Etapas: destete | precebo | cebo | engorde_final")
            etapa = input("Etapa productiva: ").strip()
            peso = float(input("Peso promedio (kg): "))
            cantidad = int(input("Cantidad de animales: "))
            await alimentacion.registrar_plan_alimentacion(numero_lote, etapa, peso, cantidad)

        elif opcion == "3":
            numero_lote = input("Número de lote: ").strip()
            await alimentacion.consultar_plan_alimentacion(numero_lote)

        elif opcion == "4":
            numero_lote = input("Número de lote: ").strip()
            fecha = input("Fecha (YYYY-MM-DD): ").strip()
            kg = float(input("Kg consumidos: "))
            precio = float(input("Precio por kg ($): "))
            await alimentacion.registrar_consumo(numero_lote, fecha, kg, precio)

        elif opcion == "5":
            numero_lote = input("Número de lote: ").strip()
            await alimentacion.consumo_total_lote(numero_lote)

        elif opcion == "0":
            break
        else:
            print("⚠ Opción no válida.")


async def flujo_sanidad(sanidad: ModuloSanidad):
    while True:
        menu_sanidad()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            numero_lote = input("Número de lote: ").strip()
            medicamento = input("Tipo de medicamento/vacuna: ").strip()
            fecha = input("Fecha de aplicación (YYYY-MM-DD): ").strip()
            dosis = input("Dosis: ").strip()
            obs = input("Observaciones: ").strip()
            await sanidad.registrar_vacuna_o_tratamiento(numero_lote, medicamento, fecha, dosis, obs)

        elif opcion == "2":
            numero_lote = input("Número de lote: ").strip()
            await sanidad.consultar_historial_sanitario(numero_lote)

        elif opcion == "3":
            numero_lote = input("Número de lote: ").strip()
            print("Tipos: limpieza | desinfeccion_corral | manejo_residuos_aguas | acceso_personal | acceso_visitantes")
            tipo = input("Tipo de protocolo: ").strip()
            obs = input("Observaciones: ").strip()
            await sanidad.registrar_protocolo_bioseguridad(numero_lote, tipo, obs)

        elif opcion == "4":
            numero_lote = input("Número de lote: ").strip()
            await sanidad.consultar_protocolos_bioseguridad(numero_lote)

        elif opcion == "5":
            numero_lote = input("Número de lote: ").strip()
            cantidad = int(input("Cantidad de animales muertos: "))
            causa = input("Causa de muerte: ").strip()
            await sanidad.registrar_muerte(numero_lote, cantidad, causa)

        elif opcion == "6":
            numero_lote = input("Número de lote: ").strip()
            await sanidad.consultar_mortalidad_lote(numero_lote)

        elif opcion == "7":
            await sanidad.mortalidad_total_granja()

        elif opcion == "0":
            break
        else:
            print("⚠ Opción no válida.")


async def flujo_produccion(produccion: ModuloProduccion):
    while True:
        menu_produccion()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            numero_lote = input("Número de lote: ").strip()
            peso = float(input("Peso promedio actual (kg): "))
            cantidad = int(input("Cantidad de animales pesados: "))
            await produccion.registrar_pesaje(numero_lote, peso, cantidad)

        elif opcion == "2":
            numero_lote = input("Número de lote: ").strip()
            await produccion.consultar_pesajes(numero_lote)

        elif opcion == "3":
            numero_lote = input("Número de lote: ").strip()
            await produccion.consultar_indicadores(numero_lote)

        elif opcion == "4":
            entrada = input("Ingrese los lotes a comparar separados por coma (ej: Lote 01, Lote 02): ")
            lotes = [l.strip() for l in entrada.split(",")]
            await produccion.comparar_indicadores_lotes(lotes)

        elif opcion == "0":
            break
        else:
            print("⚠ Opción no válida.")


async def flujo_economia(economia: ModuloEconomia):
    while True:
        menu_economia()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            numero_lote = input("Número de lote: ").strip()
            peso_inicial = float(input("Peso inicial (kg): "))
            peso_final = float(input("Peso final (kg): "))
            cantidad_inicial = int(input("Cantidad inicial de animales: "))
            cantidad_final = int(input("Cantidad final de animales: "))
            consumo = float(input("Consumo total de alimento (kg): "))

            print("\n--- COSTOS ---")
            alimentacion_c = float(input("Costo alimentación ($): "))
            sanidad_c = float(input("Costo sanidad ($): "))
            mano_obra = float(input("Costo mano de obra ($): "))
            infraestructura = float(input("Costo infraestructura ($): "))
            otros = float(input("Otros costos ($): "))

            print("\n--- INGRESOS ---")
            venta = float(input("Ingresos por venta de animales ($): "))
            subproductos = float(input("Ingresos por subproductos ($): "))
            subsidios = float(input("Subsidios o bonificaciones ($): "))

            datos_lote = {
                "lote": numero_lote,
                "peso_inicial": peso_inicial,
                "peso_final": peso_final,
                "cantidad_inicial": cantidad_inicial,
                "cantidad_final": cantidad_final,
                "consumo_alimento": consumo,
                "costos": {
                    "alimentacion": alimentacion_c,
                    "sanidad": sanidad_c,
                    "mano_obra": mano_obra,
                    "infraestructura": infraestructura,
                    "otros": otros,
                },
                "ingresos": {
                    "venta_animales": venta,
                    "subproductos": subproductos,
                    "subsidios": subsidios,
                },
            }
            await economia.registrar_datos(datos_lote)

        elif opcion == "2":
            nombre_lote = input("Número de lote: ").strip()
            await economia.grafico_costos_vs_ingresos(nombre_lote)

        elif opcion == "3":
            nombre_lote = input("Número de lote: ").strip()
            await economia.grafico_engorde_lote(nombre_lote)

        elif opcion == "4":
            nombre_lote = input("Número de lote: ").strip()
            await economia.grafico_consumo_alimento_lote(nombre_lote)

        elif opcion == "0":
            break
        else:
            print("⚠ Opción no válida.")


async def flujo_reportes(economia: ModuloEconomia):
    while True:
        menu_reportes()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            await economia.grafico_mortalidad_granja()

        elif opcion == "2":
            await economia.tabla_comparativa_rentabilidad()

        elif opcion == "3":
            entrada = input("Ingrese los lotes a comparar separados por coma (ej: Lote 01, Lote 02): ")
            lotes = [l.strip() for l in entrada.split(",")]
            await economia.tabla_comparativa_rentabilidad(lotes)

        elif opcion == "0":
            break
        else:
            print("⚠ Opción no válida.")




async def main():

    # Inicializar todos los módulos
    animales = ModuloAnimales()
    alimentacion = ModuloAlimentacion()
    sanidad = ModuloSanidad()
    produccion = ModuloProduccion()
    economia = ModuloEconomia()

    print("\n✔ Conexión con MongoDB Atlas establecida.")

    while True:
        mostrar_menu_principal()
        opcion = input("\nSeleccione una opción: ").strip()

        if opcion == "1":
            await flujo_animales(animales)
        elif opcion == "2":
            await flujo_alimentacion(alimentacion)
        elif opcion == "3":
            await flujo_sanidad(sanidad)
        elif opcion == "4":
            await flujo_produccion(produccion)
        elif opcion == "5":
            await flujo_economia(economia)
        elif opcion == "6":
            await flujo_reportes(economia)
        elif opcion == "0":
            print("\n👋 Saliendo del sistema. ¡Hasta luego!")
            break
        else:
            print("⚠ Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    asyncio.run(main())