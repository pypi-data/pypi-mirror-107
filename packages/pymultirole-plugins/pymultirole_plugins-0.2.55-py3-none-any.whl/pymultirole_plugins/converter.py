import abc
from typing import Type, List
from pydantic import BaseModel
from starlette.datastructures import UploadFile

from pymultirole_plugins.schema import FormDataModel, Document


class ConverterParameters(FormDataModel):
    pass


class ConverterBase(metaclass=abc.ABCMeta):
    """Base class for example plugin used in the tutorial.
    """

    def __init__(self):
        pass

    @abc.abstractmethod
    def convert(self, source: UploadFile, parameters: ConverterParameters) \
            -> List[Document]:
        """Parse the input source file and return a list of documents.

        :param source: An UploadFile containing the data.
        :param parameters: options of the converter.
        :returns: List of documents.
        """

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ConverterParameters
