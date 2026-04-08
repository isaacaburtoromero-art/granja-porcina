from database.mongo import db

class SistemaGranja:

    def __init__(self):
        self.lotes = db["lotes"]

    def registrar_lote(self, lote):
        if self.lotes.find_one({"numero_lote": lote.numero_lote}):
            return {"mensaje": "El lote ya existe"}

        self.lotes.insert_one(lote.to_dict())
        return {"mensaje": "Lote registrado correctamente"}

    def obtener_lotes(self):
        return list(self.lotes.find({}, {"_id": 0}))

    def agregar_registro_sanitario(self, numero_lote, registro):
        self.lotes.update_one(
            {"numero_lote": numero_lote},
            {"$push": {"historial_sanitario": registro.to_dict()}}
        )
        return {"mensaje": "Registro sanitario agregado"}

    def agregar_protocolo(self, numero_lote, protocolo):
        self.lotes.update_one(
            {"numero_lote": numero_lote},
            {"$push": {"historial_sanitario": protocolo.to_dict()}}
        )
        return {"mensaje": "Protocolo agregado"}

    def registrar_mortalidad(self, numero_lote, cantidad):
        self.lotes.update_one(
            {"numero_lote": numero_lote},
            {"$inc": {"mortalidad": cantidad}}
        )
        return {"mensaje": "Mortalidad actualizada"}
