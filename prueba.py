# === IMPORTADOS ===
import os       # Para interactuar con el sistema operativo (verificar o borrar archivos)
import json     # Para convertir datos a formato JSON (estructura de texto )
import unicodedata  # Para normalizar caracteres (por ejemplo, eliminar tildes)

# === VARIABLES GLOBALES ===
# Nombre del archivo donde se guarda el historial de residuos
HISTORIAL_FILE = "historial_reciclaje.txt"

# Diccionario que contiene el impacto ecológico estimado segun el tipo de residuo (agua, energía, CO₂)
IMPACTO_RESIDUOS = {
    "plástico": {"agua": 3, "energia": 0.5, "co2": 0.2},
    "lata": {"agua": 5, "energia": 1.0, "co2": 0.5},
    "cartón": {"agua": 2, "energia": 0.3, "co2": 0.1},
    "papel": {"agua": 4, "energia": 0.4, "co2": 0.2},
    "vidrio": {"agua": 1, "energia": 0.8, "co2": 0.3},
    "tetrapak": {"agua": 3, "energia": 0.6, "co2": 0.25},
    "textil": {"agua": 6, "energia": 1.5, "co2": 0.4},
    "electrónico": {"agua": 10, "energia": 5.0, "co2": 2.0},
    "no reciclable (pañales, papel sucio, pilas, etc)": {"agua": 0, "energia": 0, "co2": 0}
}

# === FUNCIONES DEL PROGRAMA ===

# Elimina tildes del texto para normalizar y evitar errores al comparar strings
# Ejemplo: "plástico" -> "plastico"
def quitar_tildes(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

# Clasifica el tamaño del residuo según su altura en cm (aproxiamados por el usuario)
# Devuelve el nombre del tamaño y un factor multiplicador para calcular el impacto
# Ejemplo: altura = 35 cm -> ("grande", 1.5)
def clasificar_tamaño(cm):
    if cm < 15:
        return "pequeño", 0.8
    elif 15 <= cm <= 30:
        return "mediano", 1.0
    else:
        return "grande", 1.5

# Registra un nuevo residuo ingresado por el usuario
# Pide tipo de residuo, descripción y medidas, calcula el impacto ecológico
# Guarda los datos en el archivo historial_reciclaje.txt
def registrar_residuo():
    print("\n¿Qué tipo de residuo desea registrar?")
    opciones = list(IMPACTO_RESIDUOS.keys())
    for idx, material in enumerate(opciones, 1):
        print(f"{idx}. {material.capitalize()}")

    seleccion = input("Ingrese el número correspondiente: ").strip()
    if not seleccion.isdigit() or int(seleccion) not in range(1, len(opciones) + 1):
        print("❌ Selección inválida.")
        return

    tipo_seleccionado = opciones[int(seleccion) - 1]
    tipo_normalizado = quitar_tildes(tipo_seleccionado.lower())

    if "no reciclable" in tipo_normalizado:
        print("\n⚠️ Este residuo NO se puede reciclar.")
        print("❌ Ejemplos: pañales, papel higiénico, papel sucio, colillas, pilas usadas, residuos orgánicos contaminados.")
        continuar = input("¿Deseás registrarlo igualmente para llevar control? (si/no): ").strip().lower()
        if continuar != "si":
            print("❌ Registro cancelado.")
            return

    descripcion = input("Ingrese una descripción del residuo : ").strip()

    # Si es una botella de plástico, se pregunta si conoce su capacidad en litros
    if "botella" in tipo_normalizado and "plastico" in tipo_normalizado:
        respuesta = input("¿Sabés la capacidad de la botella en litros? (si/no): ").strip().lower()
        if respuesta == "si":
            litros = float(input("Ingrese la capacidad de la botella en litros (ej: 2): "))
            if litros >= 2:
                tamaño, factor = "grande", 1.5
            elif litros >= 1:
                tamaño, factor = "mediano", 1.0
            else:
                tamaño, factor = "pequeño", 0.8
        else:
            alto = float(input("Ingrese el alto del residuo en cm: "))
            ancho = float(input("Ingrese el ancho del residuo en cm: "))
            tamaño, factor = clasificar_tamaño(alto)
    else:
        alto = float(input("Ingrese el alto del residuo en cm: "))
        ancho = float(input("Ingrese el ancho del residuo en cm: "))
        tamaño, factor = clasificar_tamaño(alto)

    impacto = IMPACTO_RESIDUOS[tipo_seleccionado]
    impacto_escalado = {k: round(v * factor, 2) for k, v in impacto.items()}

    # Guarda los datos como una línea JSON en el archivo
    with open(HISTORIAL_FILE, "a") as f:
        f.write(json.dumps({
            "tipo": tipo_seleccionado,
            "descripcion": descripcion,
            "tamaño": tamaño,
            "factor_tamaño": factor,
            "impacto": impacto_escalado
        }) + "\n")

    print("\n✅ Residuo registrado correctamente.")
    print(f"Tipo: {tipo_seleccionado} - {descripcion}")
    print(f"Tamaño estimado: {tamaño} (factor {factor})")
    print(f"Impacto estimado: {impacto_escalado['agua']}L de agua, "
          f"{impacto_escalado['energia']}kWh de energía, {impacto_escalado['co2']}kg de CO₂.")

# Lee el archivo historial y muestra la suma total de agua, energía y CO2 ahorrados
def ver_impacto_acumulado():
    total = {"agua": 0, "energia": 0, "co2": 0}
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r") as f:
            for line in f:
                data = json.loads(line)
                for k in total:
                    total[k] += data["impacto"].get(k, 0)
    print("\n🌍 Impacto acumulado:")
    print(f"💧 Agua ahorrada: {round(total['agua'], 2)}L")
    print(f"⚡ Energía ahorrada: {round(total['energia'], 2)}kWh")
    print(f"🌱 CO₂ reducido: {round(total['co2'], 2)}kg")

# Elimina el archivo de historial si existe
def limpiar_historial():
    if os.path.exists(HISTORIAL_FILE):
        os.remove(HISTORIAL_FILE)
        print("🗑 Historial limpiado correctamente.")
    else:
        print("No hay historial para limpiar.")

# Menú principal del programa que ofrece al usuario distintas opciones para interactuar con la app
def menu():
    while True:
        print("\n=== ♻️ ReciclApp - Menú Principal ===")
        print("1. Registrar nuevo residuo")
        print("2. Ver impacto acumulado")
        print("3. Limpiar historial")
        print("4. Salir")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            registrar_residuo()
        elif opcion == "2":
            ver_impacto_acumulado()
        elif opcion == "3":
            limpiar_historial()
        elif opcion == "4":
            print("👋 ¡Gracias por usar ReciclApp! 🌱")
            break
        else:
            print("⚠️ Opción inválida. Intente nuevamente.")

# Llamada inicial para ejecutar el programa
menu()
#Los emojis fuerona añadidos para mejorar el menu ya que es lo unico que ve el usuario