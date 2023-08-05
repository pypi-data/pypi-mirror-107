import os

from db_tools import MetaExporter


def test_meta_exporter(db_url):
    file_name = "db_structure.xlsx"
    meta_exporter = MetaExporter(db_url)
    meta_exporter.export(file_name)
    assert os.path.exists(file_name)
    os.remove(file_name)


def test_parse_database():
    db_url = "mysql://localhost:3306/db_test"
    meta_exporter = MetaExporter(db_url)
    assert meta_exporter._database == "db_test"

    db_url = "mysql://localhost:3306/db_test?charset=utf-8"
    meta_exporter = MetaExporter(db_url)
    assert meta_exporter._database == "db_test"
