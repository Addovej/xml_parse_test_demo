from multiprocessing import Pool
from pathlib import Path
from random import randint
from typing import Tuple
from uuid import uuid1
from xml.etree import ElementTree as et
from zipfile import ZipFile

from tqdm import tqdm

from utils import timing, ValidationException

GeneratedXML = Tuple[str, str]


class XmlGenerator:

    def __init__(self, path: Path, xml_count: int, zip_count: int) -> None:
        self.path: Path = path
        self.xml_count: int = xml_count
        self.zip_count: int = zip_count

        self.path.mkdir(parents=True, exist_ok=True)

    def __call__(self) -> None:
        self.generate_zips()

    def validate(self) -> None:
        if self.xml_count <= 0:
            raise ValidationException(
                'xml-count arg must be greater 0',
                'xml_count_failed'
            )
        if self.zip_count <= 0:
            raise ValidationException(
                'zip-count arg must be greater 0',
                'zip_count_failed'
            )

    def _generate_xml(self) -> GeneratedXML:
        root: et.Element = et.Element('root')
        _id = self.rand_id()
        et.SubElement(
            root, 'var', {'name': 'id', 'value': _id}
        )
        et.SubElement(
            root, 'var', {'name': 'level', 'value': str(self.rand_level())}
        )
        objects: et.Element = et.SubElement(root, 'objects')

        for _ in range(randint(1, 11)):
            et.SubElement(
                objects, 'object', {'name': self.rand_object_name()}
            )

        return f'{_id}.xml', et.tostring(root).decode()

    @staticmethod
    def rand_id() -> str:
        return str(uuid1())

    @staticmethod
    def rand_level() -> int:
        return randint(1, 101)

    @staticmethod
    def rand_object_name() -> str:
        return uuid1().hex

    def generate_zip(self, *args) -> None:
        try:
            with ZipFile(self.path / f'{uuid1()}.zip', 'w') as archive:
                for _ in range(self.xml_count):
                    filename, xml = self._generate_xml()
                    archive.writestr(filename, xml)
        except IOError as e:
            print(e)

    @timing
    def generate_zips(self) -> None:
        with Pool() as pool:
            with tqdm(total=self.zip_count) as pbar:
                for _ in pool.imap(self.generate_zip, range(self.zip_count)):
                    pbar.update()
