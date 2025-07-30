import os
import json

HISTORIAL_FILE = "historial_reciclaje.txt"

IMPACTO_RESIDUOS = {
    "botella de plástico": {"agua": 3, "energia": 0.5, "co2": 0.2},
    "lata": {"agua": 5, "energia": 1.0, "co2": 0.5},
    "cartón": {"agua": 2, "energia": 0.3, "co2": 0.1}
}

def clasificar_tamaño(cm):
    if cm < 15:
        return "pequeño", 0.8
    elif 15 <= cm <= 30:
        return "mediano", 1.0
    else:
        return "grande", 1.5

def registrar_residuo():
    tipo = input("Ingrese el tipo de residuo (botella de plastico, lata, cartón): ").strip().lower()

    if tipo == "botella de plástico":
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

    reciclable = tipo in IMPACTO_RESIDUOS
    impacto = IMPACTO_RESIDUOS.get(tipo, {"agua": 0, "energia": 0, "co2": 0})
    impacto_escalado = {k: round(v * factor, 2) for k, v in impacto.items()}

    with open(HISTORIAL_FILE, "a") as f:
        f.write(json.dumps({
            "tipo": tipo,
            "tamaño": tamaño,
            "factor_tamaño": factor,
            "impacto": impacto_escalado
        }) + "\n")

    print("\nResultado:")
    if reciclable:
        print(f"✅ El residuo '{tipo}' es reciclable.")
        print(f"Tamaño estimado: {tamaño} (factor {factor})")
        print(f"Impacto estimado: {impacto_escalado['agua']}L de agua, "
              f"{impacto_escalado['energia']}kWh de energía, {impacto_escalado['co2']}kg de CO₂.")
    else:
        print(f"❌ El residuo '{tipo}' no está en la lista de reciclables.")

def ver_impacto_acumulado():
    total = {"agua": 0, "energia": 0, "co2": 0}
    if os.path.exists(HISTORIAL_FILE):
        with open(HISTORIAL_FILE, "r") as f:
            for line in f:
                data = json.loads(line)
                for k in total:
                    total[k] += data["impacto"].get(k, 0)
    print("\nImpacto acumulado:")
    print(f"💧 Agua ahorrada: {round(total['agua'], 2)}L")
    print(f"⚡ Energía ahorrada: {round(total['energia'], 2)}kWh")
    print(f"🌱 CO₂ reducido: {round(total['co2'], 2)}kg")

def limpiar_historial():
    if os.path.exists(HISTORIAL_FILE):
        os.remove(HISTORIAL_FILE)
        print("🗑 Historial limpiado correctamente.")
    else:
        print("No hay historial para limpiar.")

def menu():
    while True:
        print("\n=== Reciclo o Tiro ===")
        print("1. Registrar residuo")
        print("2. Ver impacto acumulado")
        print("3. Limpiar historial")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_residuo()
        elif opcion == "2":
            ver_impacto_acumulado()
        elif opcion == "3":
            limpiar_historial()
        elif opcion == "4":
            print("¡Gracias por usar ReciclApp! 🌿")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

menu()
