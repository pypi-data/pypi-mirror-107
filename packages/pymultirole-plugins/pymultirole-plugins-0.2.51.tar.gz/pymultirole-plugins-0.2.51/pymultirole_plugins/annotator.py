import abc
from typing import Type

from pydantic import BaseModel

from pymultirole_plugins.schema import Document


class AnnotatorParameters(BaseModel):
    pass


class AnnotatorBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def annotate(self, document: Document, options: AnnotatorParameters) \
            -> Document:
        """Annotate the input document and return a modified document.

        :param document: An annotated document.
        :param options: options of the parser.
        :returns: Document.
        """

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return AnnotatorParameters
