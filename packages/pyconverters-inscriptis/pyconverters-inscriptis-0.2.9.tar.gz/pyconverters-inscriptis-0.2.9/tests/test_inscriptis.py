from pathlib import Path

from pyconverters_inscriptis.inscriptis import InscriptisConverter, InscriptisParameters


def test_inscriptis():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/test.html')
    result = Path(testdir, 'data/test.txt')
    with source.open("r") as fin:
        converter = InscriptisConverter()
        options = InscriptisParameters(encoding="utf-8")
        docs = converter.convert(fin, options)
        assert len(docs) == 1
        with result.open("r") as fin2:
            text = fin2.read()
            assert docs[0].text == text
            assert docs[0].sourceText.startswith("<html>")


def test_table_in_table():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/table-in-table.html')
    result = Path(testdir, 'data/table-in-table.txt')
    with source.open("r") as fin:
        converter = InscriptisConverter()
        options = InscriptisParameters(encoding="utf-8")
        docs = converter.convert(fin, options)
        assert len(docs) == 1
        with result.open("r") as fin2:
            text = fin2.read()
            assert docs[0].text == text
            assert docs[0].sourceText.startswith("<h1>")


def test_table_pre():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/table-pre.html')
    result = Path(testdir, 'data/table-pre.txt')
    with source.open("r") as fin:
        converter = InscriptisConverter()
        options = InscriptisParameters(encoding="utf-8")
        docs = converter.convert(fin, options)
        assert len(docs) == 1
        with result.open("r") as fin2:
            text = fin2.read()
            assert docs[0].text == text
            assert docs[0].sourceText.startswith("<h1>")
