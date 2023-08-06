from typing import Type

import pytest
from pydantic import BaseModel, Field

from pymultirole_plugins.annotator import AnnotatorBase, AnnotatorParameters
from pymultirole_plugins.schema import Document, Category


def test_annotator():
    with pytest.raises(TypeError) as err:
        parser = AnnotatorBase()
        assert parser is None
    assert "Can't instantiate abstract class AnnotatorBase with abstract methods annotate" in str(err.value)


def test_default_options():
    options = AnnotatorParameters()
    assert options is not None


class DummyParameters(AnnotatorParameters):
    foo: str = Field("foo", description="Foo")
    bar: float = Field(0.123456789, description="Bar")


class Dummyannotator(AnnotatorBase):
    """Dummy annotator.
    """

    def annotate(self, document: Document, parameters: AnnotatorParameters) \
            -> Document:
        parameters: DummyParameters = parameters
        document.categories = [Category(labelName=parameters.foo, score=parameters.bar)]
        return document

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return DummyParameters


def test_dummy():
    annotator = Dummyannotator()
    options = DummyParameters()
    doc: Document = annotator.annotate(Document(text="This is a test document", metadata=options.dict()), options)
    assert len(doc.categories) == 1
    assert doc.categories[0].labelName == options.foo
    assert doc.categories[0].score == options.bar
