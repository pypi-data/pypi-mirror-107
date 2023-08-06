from typing import Type

import pytest
from pydantic import BaseModel, Field
from starlette.responses import Response

from pymultirole_plugins.schema import Document

from pymultirole_plugins.formatter import FormatterBase, FormatterParameters


def test_formatter():
    with pytest.raises(TypeError) as err:
        parser = FormatterBase()
        assert parser is None
    assert "Can't instantiate abstract class FormatterBase with abstract methods format" in str(err.value)


def test_default_options():
    options = FormatterParameters()
    assert options is not None


class DummyParameters(FormatterParameters):
    foo: str = Field("foo", description="Foo")
    bar: int = Field(0, description="Foo")


class DummyFormatter(FormatterBase):
    """Dummy formatter.
    """

    def format(self, document: Document, options: FormatterParameters) \
            -> Response:
        """Parse the input document and return a formatted response.

        :param document: An annotated document.
        :param options: options of the parser.
        :returns: Response.
        """
        return Response(content=document.json(), media_type="application/json")

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DummyParameters


def test_dummy():
    formatter = DummyFormatter()
    options = DummyParameters()
    resp: Response = formatter.format(Document(text="This is a test document", metadata=options.dict()), options)
    assert resp.status_code == 200
    assert resp.media_type == "application/json"
