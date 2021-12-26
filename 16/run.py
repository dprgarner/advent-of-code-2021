"""
10:30-11:45
Leading zero bug-fix after submitting: 2 mins
"""


def read_hex():
    return "".join("{:04b}".format(int(x, base=16)) for x in input())


OPERATOR = {
    0: "SUM",
    1: "PRODUCT",
    2: "MINIMUM",
    3: "MAXIMUM",
    5: "GREATER_THAN",
    6: "LESS_THAN",
    7: "EQUAL_TO",
}


def parse_packet(binary_string):
    version = int(binary_string[:3], base=2)
    binary_string = binary_string[3:]
    print("Packet version:", version)

    operator_type = int(binary_string[0:3], base=2)
    binary_string = binary_string[3:]
    if operator_type == 4:
        value_bits = []
        while binary_string[0] == "1":
            value_bits.append(binary_string[1:5])
            binary_string = binary_string[5:]
        value_bits.append(binary_string[1:5])
        binary_string = binary_string[5:]
        value = int("".join(value_bits), base=2)
        print("Literal value:", value)
        return (("LITERAL", value), binary_string, version)

    else:
        print("This is an operator")
        length_type = binary_string[0]
        binary_string = binary_string[1:]
        if length_type == "0":
            length = int(binary_string[:15], base=2)
            binary_string = binary_string[15:]
            print("The next ", length, " bits are the subpackets")
            subpackets = []
            remaining = binary_string[:length]
            binary_string = binary_string[length:]
            while remaining:
                subpacket, remaining, v = parse_packet(remaining)
                version += v
                subpackets.append(subpacket)
            print("subpackets", subpackets)
            return (OPERATOR[operator_type], subpackets), binary_string, version
        else:
            subpackets_count = int(binary_string[:11], base=2)
            binary_string = binary_string[11:]
            print("There are ", subpackets_count, " subpackets")
            subpackets = []
            while subpackets_count:
                subpacket, binary_string, v = parse_packet(binary_string)
                version += v
                subpackets.append(subpacket)
                subpackets_count -= 1
            print("subpackets", subpackets)
            return (OPERATOR[operator_type], subpackets), binary_string, version


def product(values):
    result = 1
    for value in values:
        result *= value
    return result


def evaluate(expression):
    operator, values = expression
    if operator == "LITERAL":
        return values
    if operator == "SUM":
        return sum(evaluate(x) for x in values)
    if operator == "PRODUCT":
        return product(evaluate(x) for x in values)
    if operator == "MINIMUM":
        return min(evaluate(x) for x in values)
    if operator == "MAXIMUM":
        return max(evaluate(x) for x in values)
    if operator == "GREATER_THAN":
        return int(evaluate(values[0]) > evaluate(values[1]))
    if operator == "LESS_THAN":
        return int(evaluate(values[0]) < evaluate(values[1]))
    if operator == "EQUAL_TO":
        return int(evaluate(values[0]) == evaluate(values[1]))

    raise Exception("Undefined operator")


def main():
    binary_string = read_hex()
    print(binary_string)
    expression, _, version = parse_packet(binary_string)
    print("total versions:", version)
    print("expression", expression)
    result = evaluate(expression)
    print("result:", result)


if __name__ == "__main__":
    main()
