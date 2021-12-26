#!/bin/bash -e

mkdir $1
touch $1/small.txt
touch $1/large.txt
cat > "$1"/run.py << EOF
"""
"""


def read_ints():
    try:
        while True:
            ints.append(int(input()))
    except EOFError:
        pass
    return ints


def main_a():
    ints = read_ints()


def main_b():
    pass

if __name__ == "__main__":
    main_a()
    # main_b()
EOF
