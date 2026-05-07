# numer albumu: s30556
# Data: 07.05.2026


# Krótki opis programu:
# Program generuje losową sekwencję DNA, zapisuje ją w formacie FASTA
# oraz wykonuje podstawowe analizy bioinformatyczne.

import random


def generate_sequence(length: int) -> str:
    """Zwraca losową sekwencję DNA o zadanej długości."""
    nucleotides = ["A", "C", "G", "T"]
    sequence = ""

    for _ in range(length):
        sequence += random.choice(nucleotides)

    return sequence


def calculate_stats(sequence: str) -> dict:
    """Zwraca słownik ze statystykami sekwencji."""
    seq_length = len(sequence)

    a = sequence.count("A")
    c = sequence.count("C")
    g = sequence.count("G")
    t = sequence.count("T")

    return {
        "A": round(a / seq_length * 100, 2),
        "C": round(c / seq_length * 100, 2),
        "G": round(g / seq_length * 100, 2),
        "T": round(t / seq_length * 100, 2),
        "GC": round((g + c) / seq_length * 100, 2)
    }


def insert_name(sequence: str, name: str) -> str:
    """Wstawia imię użytkownika w losową pozycję sekwencji, zapisując je małymi literami."""
    position = random.randint(0, len(sequence))
    name = name.lower()

    return sequence[:position] + name + sequence[position:]


def format_fasta(seq_id: str, description: str, sequence: str, line_width: int = 80) -> str:
    """Zwraca sformatowany rekord FASTA jako string."""
    if description:
        fasta_text = ">" + seq_id + " " + description + "\n"
    else:
        fasta_text = ">" + seq_id + "\n"

    for i in range(0, len(sequence), line_width):
        fasta_text += sequence[i:i + line_width] + "\n"

    return fasta_text


def validate_positive_int(prompt: str, min_val: int = 1, max_val: int = 100_000) -> int:
    """Pobiera od użytkownika liczbę całkowitą z zakresu."""
    while True:
        text = input(prompt)

        try:
            number = int(text)

            if min_val <= number <= max_val:
                return number
            else:
                print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")

        except ValueError:
            print(f"Błąd: wartość musi być liczbą całkowitą z zakresu [{min_val}, {max_val}].")


def validate_fasta_id() -> str:
    """Pobiera od użytkownika poprawne ID sekwencji."""
    while True:
        seq_id = input("Podaj ID sekwencji: ").strip()

        if seq_id == "":
            print("Błąd: ID nie może być puste.")
        elif any(char.isspace() for char in seq_id):
            print("Błąd: ID nie może zawierać białych znaków.")
        else:
            return seq_id


def get_distribution() -> dict:
    """Pozwala użytkownikowi podać własny rozkład nukleotydów."""
    answer = input("Czy chcesz podać własny rozkład nukleotydów? (t/n): ").strip().lower()

    if answer != "t":
        return {"A": 25, "C": 25, "G": 25, "T": 25}

    while True:
        print("Podaj procentowy udział nukleotydów. Suma musi wynosić 100.")

        a = validate_positive_int("A [%]: ", 0, 100)
        c = validate_positive_int("C [%]: ", 0, 100)
        g = validate_positive_int("G [%]: ", 0, 100)
        t = validate_positive_int("T [%]: ", 0, 100)

        if a + c + g + t == 100:
            return {"A": a, "C": c, "G": g, "T": t}

        print("Błąd: suma procentów musi wynosić dokładnie 100.")


def generate_sequence_with_distribution(length: int, distribution: dict) -> str:
    """Generuje sekwencję DNA według procentowego rozkładu nukleotydów."""
    nucleotides = ["A", "C", "G", "T"]
    weights = [
        distribution["A"],
        distribution["C"],
        distribution["G"],
        distribution["T"]
    ]

    return "".join(random.choices(nucleotides, weights=weights, k=length))


def find_motif(sequence: str, motif: str) -> list:
    """Wyszukuje wszystkie pozycje motywu w sekwencji. Indeksowanie od 1."""
    positions = []

    if motif == "":
        return positions

    start = 0
    motif = motif.upper()

    while True:
        found = sequence.find(motif, start)

        if found == -1:
            break

        positions.append(found + 1)
        start = found + 1

    return positions


def complement_sequence(sequence: str) -> str:
    """Zwraca sekwencję komplementarną DNA."""
    result = ""

    for char in sequence:
        if char == "A":
            result += "T"
        elif char == "T":
            result += "A"
        elif char == "C":
            result += "G"
        elif char == "G":
            result += "C"

    return result


def reverse_complement_sequence(sequence: str) -> str:
    """Zwraca sekwencję odwrotnie komplementarną DNA."""
    return complement_sequence(sequence)[::-1]


def transcribe_to_mrna(sequence: str) -> str:
    """Zamienia sekwencję DNA na mRNA przez zamianę T na U."""
    return sequence.replace("T", "U")


def print_stats(stats: dict, length: int) -> None:
    """Wypisuje statystyki sekwencji."""
    print(f"Statystyki sekwencji (n={length}):")
    print(f"A: {stats['A']:.2f}%")
    print(f"C: {stats['C']:.2f}%")
    print(f"G: {stats['G']:.2f}%")
    print(f"T: {stats['T']:.2f}%")
    print(f"GC-content: {stats['GC']:.2f}%")


def main():
    """Główna część programu."""
    length = validate_positive_int("Podaj długość sekwencji: ")
    seq_id = validate_fasta_id()
    description = input("Podaj opis sekwencji: ").strip()
    name = input("Podaj imię: ").strip()

    distribution = get_distribution()
    sequence = generate_sequence_with_distribution(length, distribution)

    sequence_with_name = insert_name(sequence, name)
    stats = calculate_stats(sequence)

    complement = complement_sequence(sequence)
    reverse_complement = reverse_complement_sequence(sequence)
    mrna = transcribe_to_mrna(sequence)

    fasta_content = ""
    fasta_content += format_fasta(seq_id, description, sequence_with_name)
    fasta_content += "\n"
    fasta_content += format_fasta(seq_id + "_complement", "Sekwencja komplementarna", complement)
    fasta_content += "\n"
    fasta_content += format_fasta(seq_id + "_reverse_complement", "Sekwencja odwrotnie komplementarna", reverse_complement)
    fasta_content += "\n"
    fasta_content += format_fasta(seq_id + "_mRNA", "Sekwencja mRNA", mrna)

    filename = seq_id + ".fasta"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(fasta_content)

    print()
    print("Sekwencja zapisana do pliku:", filename)
    print_stats(stats, length)

    motif = input("Podaj motyw do wyszukania, np. ATG albo zostaw puste: ").strip().upper()
    motif_positions = find_motif(sequence, motif)

    if motif == "":
        print("Nie podano motywu.")
    elif len(motif_positions) == 0:
        print("Motyw nie został znaleziony.")
    else:
        print("Motyw", motif, "znaleziono na pozycjach:", motif_positions)

    print()
    print("Sekwencja komplementarna:")
    print(complement)

    print()
    print("Sekwencja odwrotnie komplementarna:")
    print(reverse_complement)

    print()
    print("Sekwencja mRNA:")
    print(mrna)


if __name__ == "__main__":
    main()