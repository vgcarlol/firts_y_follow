# Cada clave es un no terminal y su valor es una lista de producciones.
# Cada producción es una lista de símbolos. Se usa "ε" para la cadena vacía.
grammar = {
    "E": [["T", "E'"]],
    "E'": [["+", "T", "E'"], ["ε"]],
    "T": [["F", "T'"]],
    "T'": [["*", "F", "T'"], ["ε"]],
    "F": [["(", "E", ")"], ["id"]]
}

def compute_first(grammar):
    first = {non_terminal: set() for non_terminal in grammar.keys()}
    changed = True

    # Se itera hasta que no haya más cambios en los conjuntos FIRST
    while changed:
        changed = False
        for non_terminal, productions in grammar.items():
            for production in productions:
                # Caso especial: la producción es directamente ε
                if production == ["ε"]:
                    if "ε" not in first[non_terminal]:
                        first[non_terminal].add("ε")
                        changed = True
                    continue

                # Se procesa cada símbolo de la producción
                for symbol in production:
                    # Si es terminal (no aparece como clave en la gramática)
                    if symbol not in grammar:
                        if symbol not in first[non_terminal]:
                            first[non_terminal].add(symbol)
                            changed = True
                        # Un terminal no produce ε, se interrumpe la iteración en la producción
                        break
                    else:
                        # Si es no terminal, se agrega el FIRST de ese símbolo (excepto ε)
                        before = len(first[non_terminal])
                        first[non_terminal].update(first[symbol] - {"ε"})
                        if len(first[non_terminal]) > before:
                            changed = True
                        # Si el no terminal no produce ε, se interrumpe el recorrido de la producción
                        if "ε" not in first[symbol]:
                            break
                else:
                    # Si todos los símbolos de la producción pueden derivar ε, se añade ε
                    if "ε" not in first[non_terminal]:
                        first[non_terminal].add("ε")
                        changed = True

    return first

def compute_first_of_string(symbols, grammar, first):
    if not symbols:
        return {"ε"}
    
    result = set()
    for symbol in symbols:
        if symbol not in grammar:  # Es terminal
            result.add(symbol)
            return result
        else:
            result.update(first[symbol] - {"ε"})
            if "ε" not in first[symbol]:
                return result
    result.add("ε")
    return result

def compute_follow(grammar, first, start_symbol):
    follow = {non_terminal: set() for non_terminal in grammar.keys()}
    follow[start_symbol].add("$")  # Fin de cadena para el símbolo inicial
    changed = True

    # Se itera hasta que no haya cambios en los conjuntos FOLLOW
    while changed:
        changed = False
        for lhs, productions in grammar.items():
            for production in productions:
                for i, symbol in enumerate(production):
                    # Solo se procesa si el símbolo es un no terminal
                    if symbol in grammar:
                        # Se obtiene FIRST del resto de la producción (símbolos a la derecha)
                        rest = production[i+1:]
                        first_rest = compute_first_of_string(rest, grammar, first)
                        before = len(follow[symbol])
                        # Se añade FIRST(rest) sin ε al FOLLOW del símbolo
                        follow[symbol].update(first_rest - {"ε"})
                        # Si el resto puede derivar ε o no hay símbolos a la derecha,
                        # se añade el FOLLOW del lado izquierdo (lhs)
                        if "ε" in first_rest or not rest:
                            follow[symbol].update(follow[lhs])
                        if len(follow[symbol]) > before:
                            changed = True
    return follow

if __name__ == "__main__":
    # Definimos el símbolo inicial de la gramática
    start_symbol = "E"

    # Calculamos los conjuntos FIRST y FOLLOW
    first_sets = compute_first(grammar)
    follow_sets = compute_follow(grammar, first_sets, start_symbol)

    # Mostramos los resultados
    print("Conjuntos FIRST:")
    for non_terminal, symbols in first_sets.items():
        print(f"  {non_terminal}: {symbols}")

    print("\nConjuntos FOLLOW:")
    for non_terminal, symbols in follow_sets.items():
        print(f"  {non_terminal}: {symbols}")
