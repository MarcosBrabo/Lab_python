import os
import json

HISTORIAL_FILE = "historial_reciclaje.txt"

IMPACTO_RESIDUOS = {
    "botella de plástico": {"agua": 3, "energia": 0.5, "co2": 0.2},
    "lata": {"agua": 5, "energia": 1.0, "co2": 0.5},
    "cartón": {"agua": 2, "energia": 0.3, "co2": 0.1}
}

def registrar_residuo():
    tipo = input("Ingrese el tipo de residuo (ej: botella de plástico, lata, cartón): ").lower()
    alto = float(input("Ingrese el alto del residuo en cm: "))
    ancho = float(input("Ingrese el ancho del residuo en cm: "))
    volumen = alto * ancho

    reciclable = tipo in IMPACTO_RESIDUOS
    impacto = IMPACTO_RESIDUOS.get(tipo, {"agua": 0, "energia": 0, "co2": 0})
    impacto_escalado = {k: v * volumen / 1000 for k, v in impacto.items()}

    with open(HISTORIAL_FILE, "a") as f:
        f.write(json.dumps({"tipo": tipo, "volumen": volumen, "impacto": impacto_escalado}) + "\n")

    print("\nResultado:")
    if reciclable:
        print(f"✅ El residuo '{tipo}' es reciclable.")
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
    print(f"💧 Agua ahorrada: {total['agua']}L")
    print(f"⚡ Energía ahorrada: {total['energia']}kWh")
    print(f"🌱 CO₂ reducido: {total['co2']}kg")

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
            print("¡Gracias por usar RecyclingApp!")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

menu()