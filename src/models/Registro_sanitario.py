class RegistroSanitario:
    def __init__(self, tipo, medicamento, fecha, dosis, observaciones):
        self.tipo = tipo
        self.medicamento = medicamento
        self.fecha = fecha
        self.dosis = dosis
        self.observaciones = observaciones

    def to_dict(self):
        return self.__dict__
