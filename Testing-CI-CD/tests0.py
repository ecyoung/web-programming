from prime import is_prime

def test_prime(n, expected):
    if is_prime != expected:
        print(f"ERROR on is_prime({n}), {expected}")