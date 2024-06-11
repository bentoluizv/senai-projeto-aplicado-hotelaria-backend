def is_valid_cpf(rawCpf: str) -> bool:
    only_digits_cpf = rawCpf.replace(".", "").replace("-", "")
    last_two_digits = only_digits_cpf[-2:]
    first_six_digits = only_digits_cpf[:-2]

    digits_list = []

    factor = 2
    sum = 0
    for num in first_six_digits[::-1]:
        sum += int(num) * factor
        factor += 1

    remainder = sum % 11

    if remainder < 2:
        digits_list.append(0)
    else:
        digits_list.append(11 - remainder)

    first_seven_digits = first_six_digits + str(digits_list[0])

    factor = 2
    sum = 0
    for num in first_seven_digits[::-1]:
        sum += int(num) * factor
        factor += 1

    remainder = sum % 11

    if remainder < 2:
        digits_list.append(0)
    else:
        digits_list.append(11 - remainder)

    digits = "".join(map(str, digits_list))

    if digits != last_two_digits:
        return False

    return True
