import io
from typing import Union, List, Type

import pytest
from pydantic import BaseModel, Field
from starlette.datastructures import UploadFile

from pymultirole_plugins.schema import Document

from pymultirole_plugins.converter import ConverterBase, ConverterParameters


def test_converter():
    with pytest.raises(TypeError) as err:
        parser = ConverterBase()
        assert parser is None
    assert "Can't instantiate abstract class ConverterBase with abstract methods convert" in str(err.value)


def test_default_options():
    options = ConverterParameters()
    assert options is not None


class DummyParameters(ConverterParameters):
    foo: str = Field("foo", description="Foo")
    bar: int = Field(0, description="Bar")


class DummyConverter(ConverterBase):
    """Dummy converter.
    """

    def convert(self, source: Union[io.IOBase, UploadFile], parameters: ConverterParameters) \
            -> List[Document]:
        """Parse the input source file and return a list of documents.

        :param source: A file object containing the data.
        :param parameters: options of the converter.
        :returns: List of converted documents.
        """
        parameters: DummyParameters = parameters
        file = source.file._file if isinstance(source, UploadFile) else source
        if isinstance(file, io.TextIOBase):
            wrapper = file
        else:
            wrapper = io.TextIOWrapper(file)
        doc = Document(text=wrapper.read(), metadata=parameters.dict())
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DummyParameters


def test_dummy():
    converter = DummyConverter()
    options = DummyParameters()
    docs = converter.convert(io.StringIO("dummy"), options)
    assert len(docs) == 1
    assert docs[0].text == "dummy"
    assert docs[0].metadata == options.dict()
