def linear_search(fstring: str, sstring: str) -> bool:
    if len(fstring) == len(sstring):
        fstring = list(fstring)
        sstring = list(sstring)

        for i in range(len(fstring)):
            if fstring[i] != sstring[i]:
                return False

        return True

    else:
        return False
