def generate_numbers(max_num, min_num, total_count):
    """
    Genera una lista de números donde la cantidad de números aumenta progresivamente
    hasta alcanzar exactamente el total_count.

    Args:
        max_num (int): El número máximo en el rango (ej: 99)
        min_num (int): El número mínimo en el rango (ej: 90)
        total_count (int): Cantidad total de números a generar (ej: 100)
    """
    if max_num <= min_num:
        raise ValueError("max_num debe ser mayor que min_num")

    numbers = []
    range_size = max_num - min_num + 1

    # Calcular la distribución de cantidades para cada número
    remaining_count = total_count - range_size  # Restamos uno por cada número base
    position_weights = []

    # Comenzamos con 0 extras para el primer número (solo tendrá 1)
    current_weight = 0
    total_weight = 0

    for i in range(range_size):
        if i == 0:
            current_weight = 0  # El primer número (99) solo aparece una vez
        else:
            # Incrementamos el peso gradualmente
            current_weight = min(i * 2, remaining_count - total_weight)
        position_weights.append(current_weight)
        total_weight += current_weight

        if total_weight >= remaining_count:
            break

    # Ajustar los pesos si es necesario para llegar exactamente al total
    if total_weight < remaining_count:
        diff = remaining_count - total_weight
        last_pos = len(position_weights) - 1
        position_weights[last_pos] += diff

    # Generar los números según los pesos calculados
    for i, N in enumerate(range(max_num, min_num - 1, -1)):
        if i >= len(position_weights):
            break

        extras = position_weights[i]
        # Determinar cuántos decimales generar
        decimals = min(extras, 9)

        # Agregar los números con decimales
        for d in range(decimals, 0, -1):
            number = round(N + d * 0.1, 1)
            numbers.append(number)

        # Agregar el número entero
        numbers.append(float(N))

        # Agregar números enteros adicionales si son necesarios
        for _ in range(max(0, extras - decimals)):
            numbers.append(float(N))

    return numbers


def print_numbers(numbers):
    """
    Imprime los números, mostrando enteros sin decimales
    """
    for number in numbers:
        if number.is_integer():
            print(int(number))
        else:
            print(number)


# Ejemplo de uso
if __name__ == "__main__":
    # Generar números del 99 al 90 con exactamente 100 números
    numbers = generate_numbers(99, 90, 100)
    print("Total de números generados:", len(numbers))
    print("\nNúmeros generados:")
    print_numbers(numbers)

    print("\nCantidad de números por valor:")
    current_num = None
    count = 0
    for num in sorted(numbers, reverse=True):
        base_num = int(num)
        if base_num != current_num:
            if current_num is not None:
                print(f"Número {current_num}: {count} veces")
            current_num = base_num
            count = 1
        else:
            count += 1
    print(f"Número {current_num}: {count} veces")
