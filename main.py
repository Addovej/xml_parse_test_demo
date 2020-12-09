from argparse import ArgumentParser, Namespace
from pathlib import Path

from generator import XmlGenerator
from parser import XmlParser
from utils import ValidationException


def parse_args() -> Namespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument(
        '--mode', type=str, nargs='?',
        choices=('generate', 'parse', 'clear'),
        default='parse'
    )
    parser.add_argument('--path', type=str, nargs='?', default='data')
    parser.add_argument('--xml-count', type=int, nargs='?', default=100)
    parser.add_argument('--zip-count', type=int, nargs='?', default=50)

    return parser.parse_args()


def main(mode: str, path: Path, xml_count: int, zip_count: int) -> None:
    if mode and mode == 'generate':
        generator = XmlGenerator(path, xml_count, zip_count)
        try:
            generator.validate()
        except ValidationException as e:
            print(f'Error: {e}')
        else:
            print('Generate zips')
            generator()
    else:
        parser = XmlParser(path)
        try:
            parser.validate()
        except ValidationException as e:
            print(f'Error: {e}')
        else:
            print('Parse zip')
            parser()


if __name__ == '__main__':
    args: Namespace = parse_args()
    main(args.mode, Path(args.path), args.xml_count, args.zip_count)
