class Lote:
    def __init__(self, numero_lote, fecha_ingreso, edad, peso_promedio, etapa_productiva):
        self.numero_lote = numero_lote
        self.fecha_ingreso = fecha_ingreso
        self.edad = edad
        self.peso_promedio = peso_promedio
        self.etapa_productiva = etapa_productiva
        self.historial_sanitario = []
        self.mortalidad = 0

    def to_dict(self):
        return {
            "numero_lote": self.numero_lote,
            "fecha_ingreso": self.fecha_ingreso,
            "edad": self.edad,
            "peso_promedio": self.peso_promedio,
            "etapa_productiva": self.etapa_productiva,
            "historial_sanitario": self.historial_sanitario,
            "mortalidad": self.mortalidad
        }
