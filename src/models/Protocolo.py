class ProtocoloBioseguridad:
    def __init__(self, tipo, fecha, observaciones):
        self.tipo = tipo
        self.fecha = fecha
        self.observaciones = observaciones

    def to_dict(self):
        return self.__dict__
