def hashing_search(fstring: str, sstring: str) -> bool:
    def factors_generation(string: str) -> list:
        factors = [1]

        for i in range(1, len(string)):
            factor = factors[i - 1] * 2
            factors.append(factor)
        return factors

    def hash_generation(string, degree: list) -> list:
        hashs = [ord(string[0])]

        for i in range(1, len(fstring)):
            symb_hash = hashs[i - 1] + degree[i] * ord(string[i])
            hashs.append(symb_hash)
        return hashs

    if len(fstring) == len(sstring) and len(fstring) > 0:
        factors = factors_generation(sstring)
        fhashs = hash_generation(fstring, factors)
        shashs = hash_generation(sstring, factors)
        if fhashs[-1] == shashs[-1]:
            return True
        else:
            return False
    else:
        return False
