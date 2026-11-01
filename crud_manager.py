from mongo_bridge import MongoBridge

def main():
    bridge = MongoBridge()
    if bridge.db is None:
        print("Error: No se pudo conectar a MongoDB.")
        return

    while True:
        print("\n--- GESTION DE VEHICULOS ---")
        print("1. Listar vehiculos (Ver estado activo/inactivo)")
        print("2. Insertar o actualizar vehiculo")
        print("3. Aplicar borrado logico")
        print("4. Restaurar vehiculo")
        print("5. Salir")
        
        opcion = input("\nSelecciona una opcion (1-5): ").strip()

        if opcion == "1":
            cars = bridge.execute_find("cars", sort=[("_id", 1)])
            print("\nID  | Modelo | Descripcion             | Anio | Estado")
            print("-" * 55)
            for c in cars:
                estado = "ACTIVO" if c.get("activo", True) else "INACTIVO"
                print(f"{c['_id']:<3} | {c.get('modelID'):<6} | {c.get('descr'):<23} | {c.get('year'):<4} | {estado}")

        elif opcion == "2":
            try:
                car_id = int(input("ID (_id): "))
                model_id = int(input("ID Modelo (modelID): "))
                descr = input("Descripcion: ").strip()
                year = int(input("Anio: "))
                mpg = float(input("Rendimiento (MPG): "))
                cylinders = int(input("Cilindros: "))
                horsepower = float(input("Potencia (HP): "))
                weight = float(input("Peso (lb): "))
                accel = float(input("Aceleracion (s): "))

                car_doc = {
                    "_id": car_id,
                    "modelID": model_id,
                    "descr": descr,
                    "year": year,
                    "mpg": mpg,
                    "cylinders": cylinders,
                    "horsepower": horsepower,
                    "weight": weight,
                    "accel": accel,
                    "activo": True
                }

                bridge.db.cars.replace_one({"_id": car_id}, car_doc, upsert=True)
                print(f"Vehiculo ID {car_id} guardado correctamente.")
            except Exception as e:
                print(f"Error al guardar: {e}")

        elif opcion == "3":
            try:
                car_id = int(input("ID a desactivar: "))
                if bridge.soft_delete_car(car_id):
                    print(f"Vehiculo ID {car_id} desactivado (borrado logico).")
                else:
                    print(f"No se realizaron cambios en el ID {car_id}.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "4":
            try:
                car_id = int(input("ID a restaurar: "))
                if bridge.restore_car(car_id):
                    print(f"Vehiculo ID {car_id} restaurado a ACTIVO.")
                else:
                    print(f"No se realizaron cambios en el ID {car_id}.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == "5":
            print("Cerrando gestor.")
            break
        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    main()