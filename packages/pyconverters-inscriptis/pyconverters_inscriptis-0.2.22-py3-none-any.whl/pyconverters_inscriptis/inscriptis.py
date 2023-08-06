import io
from typing import Type, List, Union

from bs4 import BeautifulSoup
from inscriptis import get_text
from inscriptis.model.config import ParserConfig
from pydantic import BaseModel, Field
from pymultirole_plugins.converter import ConverterParameters, ConverterBase
from pymultirole_plugins.schema import Document
from starlette.datastructures import UploadFile


class InscriptisParameters(ConverterParameters):
    display_images: bool = Field(False, description="whether to include image tiles/alt texts.")
    deduplicate_captions: bool = Field(False, description="whether to deduplicate captions such as image\
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
                              deduplicate_captions=parameters.deduplicate_captions,
                              display_links=parameters.display_links,
                              display_anchors=parameters.display_anchors)
        # Guess encoding if necessary
        soup = BeautifulSoup(source.file, 'html.parser')
        html = str(soup)
        text = get_text(html, config=config)
        doc = Document(text=text, sourceText=html,
                       properties={"fileName": source.filename, "encoding": soup.original_encoding})
        return [doc]

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return InscriptisParameters
