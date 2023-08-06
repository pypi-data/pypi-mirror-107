import io
from typing import Type, List, Union

from fastapi import UploadFile
from inscriptis import get_text
from inscriptis.model.config import ParserConfig
from pydantic import BaseModel, Field
from pymultirole_plugins.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.schema import Document


class InscriptisParameters(ConverterParameters):
    encoding: str = Field("utf-8", description="Encoding of the HTML file")
    display_images: bool = Field(False, description="whether to include image tiles/alt texts.")
    deduplicate_captions: bool = Field(False, description=" whether to deduplicate captions such as image\
                titles (many newspaper include images and video previews with\
                identical titles).")
    display_links: bool = Field(False, description="whether to display link targets\
                           (e.g. `[Python](https://www.python.org)`).")
    display_anchors: bool = Field(False, description="whether to display anchors (e.g. `[here](#here)`).")


class InscriptisConverter(ConverterBase):
    """[Inscriptis](https://inscriptis.readthedocs.io/en/latest/) HTML pretty converter .
    """

    def convert(self, source: Union[io.IOBase, UploadFile], parameters: ConverterParameters) \
            -> List[Document]:
        """Parse the input source file and return a list of documents.

        :param source: A file object containing the data.
        :param parameters: options of the converter.
        :returns: List of converted documents.
        """
        parameters: InscriptisParameters = parameters

        config = ParserConfig(display_images=parameters.display_images,
                         deduplicate_captions=parameters.deduplicate_captions, display_links=parameters.display_links,
                         display_anchors=parameters.display_anchors)
        file = source.file._file if isinstance(source, UploadFile) else source
        fileName = source.filename if isinstance(source, UploadFile) else source.name
        if isinstance(file, io.TextIOBase):
            wrapper = file
        else:
            wrapper = io.TextIOWrapper(file, encoding=parameters.encoding)

        html = wrapper.read()
        text = get_text(html, config=config)
        doc = Document(text=text, sourceText=html, properties={"fileName": fileName, "encoding": parameters.encoding})
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return InscriptisParameters
