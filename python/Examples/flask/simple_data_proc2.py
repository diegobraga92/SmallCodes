'''
Enunciado

Implemente uma função que recebe uma lista de números e retorna os intervalos contínuos.

Exemplo
[1, 2, 3, 5, 6, 8]
→ ["1-3", "5-6", "8"]

Requisitos

Lista pode estar vazia

Lista pode não estar ordenada

Retornar strings
'''


from typing import List


def continuous_ranges(numbers: List[int]) -> List[str]:
    if not numbers:
        return []

    numbers = sorted(set(numbers))
    result = []

    start = prev = numbers[0]

    for num in numbers[1:]:
        if num == prev + 1:
            prev = num
            continue

        result.append(
            f"{start}-{prev}" if start != prev else f"{start}"
        )
        start = prev = num

    result.append(
        f"{start}-{prev}" if start != prev else f"{start}"
    )

    return result


if __name__ == "__main__":
    print(continuous_ranges([1, 2, 3, 5, 6, 8]))
