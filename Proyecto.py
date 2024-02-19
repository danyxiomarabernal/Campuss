import json
import os

# Nombre del archivo JSON donde se almacenarán los datos
archivo_json = "campuslands_data.json"

# Base de datos para almacenar la información de los campers, rutas y trainers
database = {
    "campers": [],
    "rutas_entrenamiento": {
        "NodeJS": {"modulos": ["Fundamentos de programación", "Programación Web", "Backend"], "capacidad_maxima": 33},
        "Java": {"modulos": ["Fundamentos de programación", "Programación formal", "Backend"], "capacidad_maxima": 33},
        "NetCore": {"modulos": ["Fundamentos de programación", "Programación formal", "Backend"], "capacidad_maxima": 33}
    },
    "trainers": []
}

# Función para cargar la base de datos desde el archivo JSON
def cargar_base_datos():
    if os.path.exists(archivo_json):
        with open(archivo_json, "r") as file:
            return json.load(file)
    else:
        return database

# Función para guardar la base de datos en el archivo JSON
def guardar_base_datos():
    with open(archivo_json, "w") as file:
        json.dump(database, file, indent=4)

# Función para registrar un nuevo camper
def registrar_camper():
    try:
        camper = {}
        camper["numero_identificacion"] = input("Ingrese el número de identificación: ")
        camper["nombres"] = input("Ingrese los nombres del camper: ")
        camper["apellidos"] = input("Ingrese los apellidos del camper: ")
        camper["direccion"] = input("Ingrese la dirección del camper: ")
        camper["acudiente"] = input("Ingrese el nombre del acudiente: ")
        camper["telefonos_contacto"] = {
            "celular": input("Ingrese el número de celular del camper: "),
            "fijo": input("Ingrese el número fijo del camper (deje vacío si no tiene): ")
        }
        camper["estado"] = "En proceso de ingreso"
        camper["riesgo"] = input("Ingrese el nivel de riesgo del camper (Bajo, Medio, Alto): ")
        camper["nota_teoria"] = 0
        camper["nota_practica"] = 0
        camper["nota_trabajos"] = 0
        return camper
    except Exception as e:
        print(f"Ocurrió un error al ingresar la información del camper: {e}")

# Función para registrar notas de un camper
def registrar_notas_camper():
    try:
        if database["campers"]:
            print("Seleccione el camper al que desea registrar las notas:")
            for i, camper in enumerate(database["campers"]):
                print(f"{i+1}. {camper['nombres']} {camper['apellidos']}")
            indice_camper = int(input("Ingrese el número de camper: ")) - 1
            camper = database["campers"][indice_camper]
            camper["nota_teoria"] = float(input("Ingrese la nota teórica del camper: "))
            camper["nota_practica"] = float(input("Ingrese la nota práctica del camper: "))
            camper["nota_trabajos"] = float(input("Ingrese la nota de trabajos del camper: "))
            print("Notas registradas correctamente.")
        else:
            print("No hay campers registrados.")
    except IndexError:
        print("El número de camper ingresado no es válido.")
    except Exception as e:
        print(f"Ocurrió un error al registrar las notas del camper: {e}")

# Función para ver la asignación de campers por trainer
def ver_asignacion_campers_por_trainer():
    try:
        if database["trainers"]:
            print("Seleccione el trainer del que desea ver la asignación de campers:")
            for i, trainer in enumerate(database["trainers"]):
                print(f"{i+1}. {trainer['nombre']}")
            indice_trainer = int(input("Ingrese el número de trainer: ")) - 1
            trainer = database["trainers"][indice_trainer]
            especialidad_trainer = trainer["especialidad"]
            campers_asignados = []
            for camper in database["campers"]:
                if especialidad_trainer in camper["especialidad"]:
                    campers_asignados.append(camper)
            if campers_asignados:
                print(f"Campers asignados al trainer {trainer['nombre']}:")
                for camper in campers_asignados:
                    print(f"{camper['nombres']} {camper['apellidos']}")
            else:
                print(f"No hay campers asignados al trainer {trainer['nombre']}.")
        else:
            print("No hay trainers registrados.")
    except IndexError:
        print("El número de trainer ingresado no es válido.")
    except Exception as e:
        print(f"Ocurrió un error al ver la asignación de campers por trainer: {e}")

# Función para asignar un camper a una ruta de entrenamiento
def asignar_camper_a_ruta(camper, ruta):
    try:
        if len(database["rutas_entrenamiento"][ruta]["campers"]) < database["rutas_entrenamiento"][ruta]["capacidad_maxima"]:
            database["rutas_entrenamiento"][ruta]["campers"].append(camper)
            print(f"Camper asignado a la ruta {ruta} correctamente.")
        else:
            print(f"No hay cupo disponible en la ruta {ruta}.")
    except KeyError:
        print("La ruta ingresada no es válida.")

# Función para generar reportes
def generar_reportes():
    try:
        print("\nReportes:")
        print("1. Listar campers que se encuentran en estado de inscrito.")
        print("2. Listar campers que han aprobado el examen inicial.")
        print("3. Listar entrenadores que se encuentran trabajando con CampusLands.")
        print("4. Listar campers que cuentan con bajo rendimiento.")
        print("5. Listar campers y trainers asociados a una ruta de entrenamiento.")
        print("6. Mostrar cuantos campers perdieron y aprobaron cada uno de los módulos teniendo en cuenta la ruta de entrenamiento y el entrenador encargado.")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            campers_inscritos = [camper for camper in database["campers"] if camper["estado"] == "Inscrito"]
            if campers_inscritos:
                print("\nCampers en estado de inscrito:")
                for camper in campers_inscritos:
                    print(f"{camper['nombres']} {camper['apellidos']}")
            else:
                print("No hay campers en estado de inscrito.")
        elif opcion == "2":
            campers_aprobados = [camper for camper in database["campers"] if camper["estado"] == "Aprobado"]
            if campers_aprobados:
                print("\nCampers que han aprobado el examen inicial:")
                for camper in campers_aprobados:
                    print(f"{camper['nombres']} {camper['apellidos']}")
            else:
                print("No hay campers que hayan aprobado el examen inicial.")
        elif opcion == "3":
            if database["trainers"]:
                print("\nEntrenadores trabajando con CampusLands:")
                for trainer in database["trainers"]:
                    print(f"{trainer['nombre']}")
            else:
                print("No hay entrenadores trabajando con CampusLands.")
        elif opcion == "4":
            campers_bajo_rendimiento = [camper for camper in database["campers"] if camper["estado"] == "Bajo rendimiento"]
            if campers_bajo_rendimiento:
                print("\nCampers con bajo rendimiento:")
                for camper in campers_bajo_rendimiento:
                    print(f"{camper['nombres']} {camper['apellidos']}")
            else:
                print("No hay campers con bajo rendimiento.")
        elif opcion == "5":
            print("\nCampers y trainers asociados a una ruta de entrenamiento:")
            for ruta, detalles in database["rutas_entrenamiento"].items():
                print(f"\n{ruta}:")
                if detalles["campers"]:
                    print("Campers:")
                    for camper in detalles["campers"]:
                        print(f"- {camper['nombres']} {camper['apellidos']}")
                else:
                    print("No hay campers asignados a esta ruta.")
                if detalles["trainer"]:
                    print("Trainer:")
                    print(f"- {detalles['trainer']['nombre']}")
                else:
                    print("No hay trainer asignado a esta ruta.")
        elif opcion == "6":
            print("\nCuantos campers perdieron y aprobaron cada uno de los módulos:")
            for ruta, detalles in database["rutas_entrenamiento"].items():
                print(f"\n{ruta}:")
                for modulo in detalles["modulos"]:
                    campers_aprobados = [camper for camper in detalles["campers"] if camper["nota_final"][modulo] >= 60]
                    campers_perdidos = [camper for camper in detalles["campers"] if camper["nota_final"][modulo] < 60]
                    print(f"\n{modulo}:")
                    print(f"- Aprobados: {len(campers_aprobados)}")
                    print(f"- Perdidos: {len(campers_perdidos)}")
        else:
            print("Opción no válida.")
    except Exception as e:
        print(f"Ocurrió un error al generar reportes: {e}")

# Función para matricular en ruta de entrenamiento
def matricular_en_ruta():
    try:
        if database["campers"]:
            print("Seleccione el camper que desea matricular en una ruta de entrenamiento:")
            for i, camper in enumerate(database["campers"]):
                print(f"{i+1}. {camper['nombres']} {camper['apellidos']}")
            indice_camper = int(input("Ingrese el número de camper: ")) - 1
            camper = database["campers"][indice_camper]
            print("Rutas de entrenamiento disponibles:")
            for ruta, detalles in database["rutas_entrenamiento"].items():
                print(f"{ruta}: {detalles['modulos']}")
            ruta_seleccionada = input("Ingrese el nombre de la ruta de entrenamiento: ")
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_finalizacion = input("Ingrese la fecha de finalización (YYYY-MM-DD): ")
            salon_entrenamiento = input("Ingrese el salón de entrenamiento: ")
            camper["ruta_entrenamiento"] = ruta_seleccionada
            camper["fecha_inicio"] = fecha_inicio
            camper["fecha_finalizacion"] = fecha_finalizacion
            camper["salon_entrenamiento"] = salon_entrenamiento
            print("Camper matriculado correctamente.")
        else:
            print("No hay campers registrados.")
    except Exception as e:
        print(f"Ocurrió un error al matricular en ruta: {e}")

# Función para ejecutar el menú de opciones para el rol de Camper
def menu_camper():
    while True:
        print("\n\t\t\t----- MENU CAMPER -----")
        print("\n1. Registrar nuevo camper")
        print("0. Volver al menú principal")
        opcion_camper = input("Seleccione una opción: ")
        if opcion_camper == "1":
            nuevo_camper = registrar_camper()
            database["campers"].append(nuevo_camper)
            print("¡Camper registrado exitosamente!")
        elif opcion_camper == "0":
            return
        else:
            print("Opción no válida.")

# Función para ejecutar el menú de opciones para el rol de Trainer
def menu_trainer():
    while True:
        print("\n\t\t\t----- MENU TRAINER -----")
        print("\n1. Registrar notas de un camper")
        print("2. Ver asignación de campers")
        print("3. Mostrar lista de campers registrados")
        print("0. Volver al menú principal")
        opcion_trainer = input("Seleccione una opción: ")
        if opcion_trainer == "1":
            registrar_notas_camper()
        elif opcion_trainer == "2":
            ver_asignacion_campers_por_trainer()
        elif opcion_trainer == "0":
            return
        elif opcion_trainer == "3":
            print("Lista de campers registrados:")
            for camper in database["campers"]:
                print(f"Nombres: {camper['nombres']}, Apellidos: {camper['apellidos']}, Estado: {camper['estado']}")
        else:
            print("Opción no válida.")

# Función para ejecutar el menú de opciones para el rol de Coordinador
def menu_coordinador():
    while True:
        print("\n\t\t\t----- MENU COORDINADOR -----")
        print("\n1. Registrar notas de un camper")
        print("2. Asignar camper a ruta de entrenamiento")
        print("3. Generar reportes")
        print("4. Matricular en ruta de entrenamiento")
        print("0. Volver al menú principal")
        opcion_coordinador = input("Seleccione una opción: ")
        if opcion_coordinador == "1":
            registrar_notas_camper()
        elif opcion_coordinador == "2":
            if database["campers"]:
                print("Seleccione el camper al que desea asignar a una ruta de entrenamiento:")
                for i, camper in enumerate(database["campers"]):
                    print(f"{i+1}. {camper['nombres']} {camper['apellidos']}")
                indice_camper = int(input("Ingrese el número de camper: ")) - 1
                camper = database["campers"][indice_camper]
                print("Rutas de entrenamiento disponibles:")
                for ruta, detalles in database["rutas_entrenamiento"].items():
                    print(f"{ruta}: {detalles['modulos']}")
                ruta_seleccionada = input("Ingrese el nombre de la ruta de entrenamiento: ")
                asignar_camper_a_ruta(camper, ruta_seleccionada)
            else:
                print("No hay campers registrados.")
        elif opcion_coordinador == "3":
            generar_reportes()
        elif opcion_coordinador == "4":
            matricular_en_ruta()
        elif opcion_coordinador == "0":
            return
        else:
            print("Opción no válida.")

# Función para mostrar el menú principal
def menu_principal():
    while True:
        print("\n\t\t\t¡Bienvenido a CampusLands!")
        print("\n\t\t\t----- MENU PRINCIPAL -----")
        print("\n1. Camper")
        print("2. Trainer")
        print("3. Coordinador")
        print("0. Salir")
        rol = input("\nSeleccione su rol (1-Camper, 2-Trainer, 3-Coordinador, 0-Salir): ")
        if rol == "0":
            guardar_base_datos()
            print("¡Hasta luego!")
            break
        elif rol == "1":
            menu_camper()
        elif rol == "2":
            menu_trainer()
        elif rol == "3":
            menu_coordinador()
        else:
            print("Rol no válido. Por favor, seleccione una opción válida.")

# Función para ejecutar el programa
def ejecutar_programa():
    global database
    database = cargar_base_datos()
    menu_principal()

# Ejecutar el programa
ejecutar_programa()
