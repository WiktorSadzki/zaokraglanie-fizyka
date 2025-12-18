import math

def get_decimal(number):
    n = str(number)
    if '.' not in n:
        return 0
    else:
        return len(n.split('.')[1])

def round_significant_digits(number, significant_digits):
    if number == 0:
        return 0
    factor = 10**(-int(math.floor(math.log10(abs(number))))+significant_digits-1)
    return math.ceil(number * factor ) / factor

def calculate_uncertainty(u0, u1):
    return abs(u1 - u0) / u0 * 100

def round_uncertainty(number):
    b0 = round_significant_digits(number, 2)
    b1 = round_significant_digits(number, 1)

    if calculate_uncertainty(b0, b1) <= 10:
        return b1
    return b0

def round_significant_places(x, places):
    s = str(x)

    if '.' in s:
        integer, frac = s.split('.')
    else:
        integer, frac = s, ''

    sign = ''
    if integer.startswith('-'):
        sign = '-'
        integer = integer[1:]

    digits = integer + frac
    if not digits:
        return x

    point = len(integer)
    digits += '0' * (places + 1)

    kept = digits[:places]
    dropped = digits[places]

    last_kept = int(kept[-1])

    if dropped > '5' or (dropped == '5' and last_kept % 2 != 0):
        kept = str(int(kept) + 1).zfill(len(kept))

    if places < point:
        result = kept + '0' * (point - places)
    else:
        result = kept[:point] + '.' + kept[point:]

    return float(sign + result)

def significant_digits(number, x):
    s = str(x)
    n = str(number)

    if(round(x) != x):
        s = s.replace('.', '')
        if '.' in n:
            n = n.split('.')[0]
        return len(s) + len(n)-1

    diff = abs(len(n) - len(s))
    x = int(x)
    s = str(x).rstrip('0')

    return len(s) + diff-1

def analize_file(input_filename, output_filename):
    results = []

    with open(input_filename, 'r') as f:
        for line in f:
            parts = line.split()
            parts[0] = parts[0].replace(',', '.')
            parts[1] = parts[1].replace(',', '.')
            if len(parts) < 2:
                continue

            m_raw = float(parts[0])
            u_raw = float(parts[1])

            u_final = round_uncertainty(u_raw)

            sig = significant_digits(m_raw, u_final)
            x_final = round_significant_places(m_raw, sig)

            prec = max(get_decimal(u_final), get_decimal(x_final))

            results.append(
                f"{x_final:.{prec}f}".replace('.', ',') + ' ' +
                f"{u_final:.{prec}f}".replace('.', ',')
            )
    with open(output_filename, 'w') as f:
        for line in results:
            f.write(line + '\n')
            print(line)

def main():
    analize_file("measurements.txt", "results.txt")

if __name__ == '__main__':
    main()