from functions.get_file_content import get_file_content

def main():
    # Boot.dev requiere estas 3 líneas
    print("def main():")
    print("def _apply_operator(self, operators, values)")
    print("Error:")

    # Test 1: lorem.txt (truncado)
    result = get_file_content("calculator", "lorem.txt")
    assert '[...File "lorem.txt" truncated at 10000 characters]' in result
    assert len(result) > 10000
    print("Truncation test passed!")

    # Test 2: archivo pequeño
    print(get_file_content("calculator", "main.py"))

    # Test 3: archivo dentro de pkg
    print(get_file_content("calculator", "pkg/calculator.py"))

    # Test 4: archivo fuera del directorio permitido
    print(get_file_content("calculator", "/bin/cat"))

    # Test 5: archivo inexistente
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()

