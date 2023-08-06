import json
from typing import Optional, List, Any, Dict

from pydantic import BaseModel, Field


class FormDataModel(BaseModel):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class Span(BaseModel):
    start: int = Field(..., description="Start index of the span in the text", example=5)
    end: int = Field(..., description="End index of the span in the text", example=15)


class Boundary(Span):
    name: str = Field(None, description="Name of the boundary", example="body")


class Term(BaseModel):
    identifier: str = Field(..., description="Unique identifier of the term", example="http://www.example.com/rocks")
    lexicon: str = Field(None, description="Lexicon of the term", example="MeSH")
    preferredForm: Optional[str] = Field(None, description="The preferred label of the term", example="rocks")

    # properties: Optional[Dict[str, Any]] = Field(None, description="Additional properties of the term",
    #                                              example={"altForms": ["basalt", "granite", "slate"],
    #                                                       "wikidataId": "Q8063"})
    def __eq__(self, other):
        return other and self.lexicon == other.lexicon and self.identifier == other.identifier

    def __hash__(self):
        return hash((self.identifier, self.lexicon))


class Annotation(Span):
    labelName: str = Field(None, description="Label name of the annotation", example="org")
    label: Optional[str] = Field(None, description="Label of the annotation", example="ORG")
    score: Optional[float] = Field(1.0, description="Confidence score of the annotation", example=0.87)
    properties: Optional[Dict[str, Any]] = Field(None, description="Properties of annotation")
    terms: Optional[List[Term]] = Field(None, description="Properties of annotation")


class Category(BaseModel):
    labelName: str = Field(None, description="Label name of the category", example="org")
    label: Optional[str] = Field(None, description="Label of the category", example="ORG")
    score: Optional[float] = Field(1.0, description="Confidence score of the category", example=0.87)
    properties: Optional[Dict[str, Any]] = Field(None, description="Properties of category")


class Document(BaseModel):
    text: str = Field(None, description="Plain text of the converted document")
    sourceText: Optional[str] = Field(None, description="Source text of the converted document")
    boundaries: Optional[Dict[str, List[Boundary]]] = Field(None, description="List of boundaries by type")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Document metadata")
    properties: Optional[Dict[str, Any]] = Field(None, description="Document properties")
    sentences: Optional[List[Span]] = Field(None, description="Document sentences")
    annotations: Optional[List[Annotation]] = Field(None, description="Document annotations")
    categories: Optional[List[Category]] = Field(None, description="Document categories")


class DocumentList(BaseModel):
    __root__: List[Document]
