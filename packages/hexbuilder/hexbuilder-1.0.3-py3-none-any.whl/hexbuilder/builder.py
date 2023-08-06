import os
import re
import sys
import argparse


alpha = '0123456789abcdef'
single_comment = re.compile(r'\/\/.*?\n')
multi_comment = re.compile(r'\/\*(.|\n)*?\*\/')


def main():
    parser = argparse.ArgumentParser(
        description='Converts a text file to its representing hex code.'
    )

    parser.add_argument('input', type=str, help='the input file')
    parser.add_argument('-o', '--output', type=str, help='the output file')

    args = parser.parse_args()

    in_file = args.input
    out_file = args.output

    if out_file is None:
        out_file = os.path.splitext(in_file)[0] + '.hex'

    with open(in_file, 'r') as f:
        content = f.read()

    if not content.endswith('\n'):
        content += '\n'

    content = single_comment.sub('\n', content)
    content = multi_comment.sub(
        lambda x: '\n' * x.group().count('\n'),
        content
    )

    stripped = ''
    for index, i in enumerate(content.split('\n')):

        for char in i.lower():

            if char.isspace():
                continue

            if char not in alpha:
                print(
                    f'[Error] Invalid character {char} at line {index}',
                    file=sys.stderr
                )

                return

            stripped += char

    if len(stripped) & 1:
        print(f'[Error] Hex representation has odd length {len(stripped)}')

    output = [
        (alpha.find(stripped[i]) << 4) | alpha.find(stripped[i + 1])
        for i in range(0, len(stripped), 2)
    ]

    with open(out_file, 'wb+') as f:
        f.write(bytes(output))

    print(f'Produced {len(output)} bytes')