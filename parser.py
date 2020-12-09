from csv import writer as csv_writer
from multiprocessing import Pool
from pathlib import Path
from typing import List, Optional, Tuple
from xml.etree import ElementTree as et
from zipfile import ZipFile

from tqdm import tqdm

from utils import timing, ValidationException

VarsData = Tuple[str, str]
ObjectsData = List[Tuple[str, str]]

ParsedData = Tuple[List[VarsData], ObjectsData]
XmlParsedData = Tuple[VarsData, ObjectsData]


class XmlParser:

    def __init__(self, path: Path) -> None:
        self.path: Path = path

    @timing
    def __call__(self) -> None:
        _vars, _objects = self.parse_zips()
        self.save_vars_csv(_vars)
        self.save_objects_csv(_objects)

    @timing
    def parse_zips(self) -> ParsedData:
        _vars: list = []
        _objects: list = []

        files = list(self.path.glob('*.zip'))
        with Pool() as pool:
            with tqdm(total=len(files)) as pbar:
                for _v, _o in pool.imap(self.parse_zip, files):
                    _vars.extend(_v)
                    _objects.extend(_o)
                    pbar.update()

        return _vars, _objects

    @timing
    def save_vars_csv(self, data: List[VarsData]) -> None:
        print('Save vars.csv')
        self._save_csv(
            filename=self.path / 'vars.csv',
            header=('id', 'level'),
            rows=data
        )

    @timing
    def save_objects_csv(self, data: ObjectsData) -> None:
        print('Save vars.csv')
        self._save_csv(
            filename=self.path / 'objects.csv',
            header=('id', 'object_name'),
            rows=data
        )

    def validate(self) -> None:
        if not self.path.is_dir():
            raise ValidationException(
                f'Path: {self.path} is not directory',
                'path_failed'
            )

    def parse_zip(self, path: Path) -> ParsedData:
        _vars: list = []
        _objects: list = []

        with ZipFile(path, 'r') as archive:
            files = archive.namelist()
            for file in files:
                with archive.open(file, 'r') as xml_file:
                    parsed = self._parse_xml(xml_file)
                    if parsed:
                        _vars.append(parsed[0])
                        _objects.extend(parsed[1])

        return _vars, _objects

    @staticmethod
    def _parse_xml(xml) -> Optional[XmlParsedData]:
        try:
            tree = et.parse(xml)
        except Exception as e:
            # Log here
            return
        else:
            _id = tree.find('.var[@name="id"]').attrib['value']
            _vars = (_id, tree.find('.var[@name="level"]').attrib['value'])
            _objects = [
                (_id, el.attrib['name']) for el in tree.findall('.objects/object')
            ]

            return _vars, _objects

    @staticmethod
    def _save_csv(filename: Path, header: tuple, rows: list) -> None:
        with open(filename, 'w') as csv_file:
            writer = csv_writer(csv_file)
            writer.writerow(header)
            for row in tqdm(rows):
                writer.writerow(row)
