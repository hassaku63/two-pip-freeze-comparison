import argparse
import io
import csv

from typing import TypedDict

NA_TEXT = '-'

def main():
    parser = argparse.ArgumentParser(prog='compare two pip freeze output')
    parser.add_argument('file1', type=argparse.FileType('r'))
    parser.add_argument('file2', type=argparse.FileType('r'))
    parser.add_argument('--output-format', type=str, default='csv', choices=['csv', 'markdown'], dest='output_format')
    parser.add_argument('--sort', action='store_true', default=False, dest='sort', help='sort alpha')
    args = parser.parse_args()
    do_sort: bool = args.sort
    output_format = args.output_format
    filename1: str = args.file1.name
    filename2: str = args.file2.name

    freeze1: list[str] = [s.strip() for s in args.file1.readlines()]
    freeze2: list[str] = [s.strip() for s in args.file2.readlines()]

    freeze1: dict = dict(elm.split('==') for elm in freeze1)
    freeze2: dict = dict(elm.split('==') for elm in freeze2)

    deps_list = set()
    deps_list.update(freeze1.keys())
    deps_list.update(freeze2.keys())
    deps_list: list = sorted(deps_list) if do_sort else list(deps_list)

    result: list[dict] = []
    for dep in deps_list:
        result.append({
            'package': dep,
            filename1: freeze1.get(dep, NA_TEXT),
            filename2: freeze2.get(dep, NA_TEXT),
        })


    sio = io.StringIO()
    if output_format == 'csv':
        writer = csv.DictWriter(sio, fieldnames=result[0].keys())
        writer.writeheader()
        writer.writerows(result)
    elif output_format == 'markdown':
        unpacked = [
            (d['package'], d[filename1], d[filename2])
            for d in result
        ]
        pkgs, fnames1, fnames2 = zip(*unpacked)
        maxlen_pkgs = max([len(x) for x in pkgs])
        maxlen_v1 = max([len(x) for x in fnames1] + [len(filename1)])
        maxlen_v2 = max([len(x) for x in fnames2] + [len(filename2)])
        width_pkg = adjust_length_to_unit(maxlen_pkgs)
        width_v1 = adjust_length_to_unit(maxlen_v1)
        width_v2 = adjust_length_to_unit(maxlen_v2)

        # header
        sio.write('|{}|{}|{}|\n'.format(
            ''.ljust(width_pkg),
            filename1.ljust(width_v1),
            filename2.ljust(width_v2),
        ))
        sio.write('|{}|{}|{}|\n'.format(
            '-' * width_pkg,
            '-' * width_v1,
            '-' * width_v2,
        ))
        # rows
        for r in result:
            sio.write('|{pkg}|{v1}|{v2}|\n'.format(
                pkg=r['package'].ljust(width_pkg),
                v1=r[filename1].rjust(width_v1),
                v2=r[filename2].rjust(width_v2),
            ))
    else:
        raise Exception('unexpected output format')

    print(sio.getvalue())


def adjust_length_to_unit(length: int, unit: int=3):
    i = 0
    while True:
        if length < i:
            return i
        i += unit


if __name__ == '__main__':
    main()