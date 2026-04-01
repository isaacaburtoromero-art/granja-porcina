from pymongo import MongoClient
from datetime import datetime

URI='mongodb+srv://Maikel:Maikelbq@cluster0.aqorakb.mongodb.net/?appName=Cluster0'
client= MongoClient(URI)

class ConexionDB:
    def __init__(self, uri, db_name="granja"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, name):
        return self.db[name]


class Lote:
    #Bd y tabla a administrar
    collection = client['granja']['lotes']
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

class RegistroSanitario:
    def __init__(self, tipo, medicamento, fecha, dosis, observaciones):
        self.tipo = tipo  # vacuna o tratamiento
        self.medicamento = medicamento
        self.fecha = fecha
        self.dosis = dosis
        self.observaciones = observaciones

    def to_dict(self):
        return self.__dict__

class ProtocoloBioseguridad:
    def __init__(self, tipo, fecha, observaciones):
        self.tipo = tipo
        self.fecha = fecha
        self.observaciones = observaciones

    def to_dict(self):
        return self.__dict__


#servicos
class SistemaGranja:
    def __init__(self, db):
        self.lotes = db.get_collection("lotes")

  
    #Gestion de lotes
    def registrar_lote(self, lote: Lote):
        if self.lotes.find_one({"numero_lote": lote.numero_lote}):
            print("El lote ya existe")
            return
        self.lotes.insert_one(lote.to_dict())
        print("Lote registrado correctamente")

    def mostrar_lotes(self):
        for lote in self.lotes.find():
            print(lote)

    #Sanidad
    def agregar_registro_sanitario(self, numero_lote, registro: RegistroSanitario):
        self.lotes.update_one(
            {"numero_lote": numero_lote},
            {"$set": {"historial_sanitario": registro.to_dict()}}
        )
        print("Registro sanitario agregado")

    def agregar_protocolo(self, numero_lote, protocolo: ProtocoloBioseguridad):
        self.lotes.update_one(
            {"numero_lote": numero_lote},
            {"$set": {"historial_sanitario": protocolo.to_dict()}}
        )
        print("Protocolo agregado")

    def registrar_mortalidad(self, numero_lote, cantidad):
        self.lotes.update_one(
            {"numero_lote": numero_lote},
            {"$inc": {"mortalidad": cantidad}}
        )
        print("Mortalidad actualizada")


#interfaz
def menu():
    print("\n Sistema granja ")
    print("1. Registrar lote")
    print("2. Mostrar lotes")
    print("3. Agregar vacuna/tratamiento")
    print("4. Agregar protocolo")
    print("5. Registrar mortalidad")
    print("0. Salir")

#Main
if __name__ == "__main__":
    URI = 'mongodb+srv://Maikel:Maikelbq@cluster0.aqorakb.mongodb.net/?appName=Cluster0'

    conexion = ConexionDB(URI)
    sistema = SistemaGranja(conexion)

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            lote = Lote(
                numero_lote=input("Número de lote: "),
                fecha_ingreso=str(datetime.now()),
                edad=int(input("Edad: ")),
                peso_promedio=float(input("Peso promedio: ")),
                etapa_productiva=input("Etapa productiva: ")
            )
            sistema.registrar_lote(lote)

        elif opcion == "2":
            sistema.mostrar_lotes()

        elif opcion == "3":
            registro = RegistroSanitario(
                tipo=input("Tipo (vacuna/tratamiento): "),
                medicamento=input("Medicamento: "),
                fecha=str(datetime.now()),
                dosis=input("Dosis: "),
                observaciones=input("Observaciones: ")
            )
            sistema.agregar_registro_sanitario(input("Número de lote: "), registro)

        elif opcion == "4":
            protocolo = ProtocoloBioseguridad(
                tipo=input("Tipo protocolo: "),
                fecha=str(datetime.now()),
                observaciones=input("Observaciones: ")
            )
            sistema.agregar_protocolo(input("Número de lote: "), protocolo)

        elif opcion == "5":
            sistema.registrar_mortalidad(
                input("Número de lote: "),
                int(input("Cantidad: "))
            )

        elif opcion == "0":
            break

        else:
            print("Opción inválida")

#main
p1=Lote("2", "2026-03-31", 4, 34, "2", "69cc71f9c4894d7629dd4154")
#insertar el producto en la base de datos
#id=p1.insertar() 
#print(f"Producto insertado con ID: {id}")
#modificar
#p1.actualizar()
#eliminar
#p1.eliminar()from pymongo import MongoClient
from datetime import datetime

URI='mongodb+srv://Maikel:Maikelbq@cluster0.aqorakb.mongodb.net/?appName=Cluster0'
client= MongoClient(URI)

class ConexionDB:
    def __init__(self, uri, db_name="granja"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, name):
        return self.db[name]


class Lote:
    #Bd y tabla a administrar
    collection = client['granja']['lotes']
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

class RegistroSanitario:
    def __init__(self, tipo, medicamento, fecha, dosis, observaciones):
        self.tipo = tipo  # vacuna o tratamiento
        self.medicamento = medicamento
        self.fecha = fecha
        self.dosis = dosis
        self.observaciones = observaciones

    def to_dict(self):
        return self.__dict__

class ProtocoloBioseguridad:
    def __init__(self, tipo, fecha, observaciones):
        self.tipo = tipo
        self.fecha = fecha
        self.observaciones = observaciones

    def to_dict(self):
        return self.__dict__


#servicos
class SistemaGranja:
    def __init__(self, db):
        self.lotes = db.get_collection("lotes")

  
    #Gestion de lotes
    def registrar_lote(self, lote: Lote):
        if self.lotes.find_one({"numero_lote": lote.numero_lote}):
            print("El lote ya existe")
            return
        self.lotes.insert_one(lote.to_dict())
        print("Lote registrado correctamente")

    def mostrar_lotes(self):
        for lote in self.lotes.find():
            print(lote)

    #Sanidad
    def agregar_registro_sanitario(self, numero_lote, registro: RegistroSanitario):
        self.lotes.update_one(
            {"numero_lote": numero_lote},
            {"$set": {"historial_sanitario": registro.to_dict()}}
        )
        print("Registro sanitario agregado")

    def agregar_protocolo(self, numero_lote, protocolo: ProtocoloBioseguridad):
        self.lotes.update_one(
            {"numero_lote": numero_lote},
            {"$set": {"historial_sanitario": protocolo.to_dict()}}
        )
        print("Protocolo agregado")

    def registrar_mortalidad(self, numero_lote, cantidad):
        self.lotes.update_one(
            {"numero_lote": numero_lote},
            {"$inc": {"mortalidad": cantidad}}
        )
        print("Mortalidad actualizada")


#interfaz
def menu():
    print("\n Sistema granja ")
    print("1. Registrar lote")
    print("2. Mostrar lotes")
    print("3. Agregar vacuna/tratamiento")
    print("4. Agregar protocolo")
    print("5. Registrar mortalidad")
    print("0. Salir")

#Main
if __name__ == "__main__":
    URI = 'mongodb+srv://Maikel:Maikelbq@cluster0.aqorakb.mongodb.net/?appName=Cluster0'

    conexion = ConexionDB(URI)
    sistema = SistemaGranja(conexion)

    while True:
        menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            lote = Lote(
                numero_lote=input("Número de lote: "),
                fecha_ingreso=str(datetime.now()),
                edad=int(input("Edad: ")),
                peso_promedio=float(input("Peso promedio: ")),
                etapa_productiva=input("Etapa productiva: ")
            )
            sistema.registrar_lote(lote)

        elif opcion == "2":
            sistema.mostrar_lotes()

        elif opcion == "3":
            registro = RegistroSanitario(
                tipo=input("Tipo (vacuna/tratamiento): "),
                medicamento=input("Medicamento: "),
                fecha=str(datetime.now()),
                dosis=input("Dosis: "),
                observaciones=input("Observaciones: ")
            )
            sistema.agregar_registro_sanitario(input("Número de lote: "), registro)

        elif opcion == "4":
            protocolo = ProtocoloBioseguridad(
                tipo=input("Tipo protocolo: "),
                fecha=str(datetime.now()),
                observaciones=input("Observaciones: ")
            )
            sistema.agregar_protocolo(input("Número de lote: "), protocolo)

        elif opcion == "5":
            sistema.registrar_mortalidad(
                input("Número de lote: "),
                int(input("Cantidad: "))
            )

        elif opcion == "0":
            break

        else:
            print("Opción inválida")

#main
p1=Lote("2", "2026-03-31", 4, 34, "2", "69cc71f9c4894d7629dd4154")
#insertar el producto en la base de datos
#id=p1.insertar() 
#print(f"Producto insertado con ID: {id}")
#modificar
#p1.actualizar()
#eliminar
#p1.eliminar()
