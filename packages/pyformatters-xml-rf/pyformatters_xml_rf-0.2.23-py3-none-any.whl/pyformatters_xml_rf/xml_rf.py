from collections import defaultdict, namedtuple, Counter
from typing import Type
from pydantic import BaseModel, Field
from pymultirole_plugins.formatter import FormatterBase, FormatterParameters
from pymultirole_plugins.schema import Document, Boundary, Annotation
from starlette.responses import Response
import lxml.etree as ET
from Ranger import RangeBucketMap, Range


class RFXmlParameters(FormatterParameters):
    boundaries: str = Field("SECTIONS", description="Name of boundaries to consider")


class RFXmlFormatter(FormatterBase):
    """Groupe RF XML formatter.
    """

    def format(self, document: Document, parameters: FormatterParameters) \
            -> Response:
        """Parse the input document and return a formatted response.

        :param document: An annotated document.
        :param parameters: options of the parser.
        :returns: Response.
        """
        parameters: RFXmlParameters = parameters
        try:
            data = document.sourceText
            encoding = document.properties.get('encoding', "UTF-8") if document.properties else "UTF-8"
            if document.sourceText and document.boundaries and document.annotations:
                root = ET.fromstring(bytes(document.sourceText, encoding='utf-8'))
                # root = tree.getroot()

                # Ignore all namespaces
                for el in root.iter():
                    _, _, el.tag = el.tag.rpartition('}')

                boundaries = {}
                buckets = RangeBucketMap()
                terms = defaultdict(list)
                Term = namedtuple("Term", ["identifier", "prefLabel"])

                for b in document.boundaries.get(parameters.boundaries, []):
                    boundary = Boundary(**b) if isinstance(b, dict) else b
                    r = root.xpath(boundary.name)
                    if len(r) == 1:
                        node = r[0]
                        boundaries[node] = boundary.name
                        buckets[Range.closedOpen(boundary.start, boundary.end)] = node
                for a in document.annotations:
                    annotation = Annotation(**a) if isinstance(a, dict) else a
                    if buckets.contains(annotation.start) and buckets.contains(annotation.end):
                        zones = buckets[Range.closedOpen(annotation.start, annotation.end)]
                        for zone in zones:
                            for term in annotation.terms:
                                terms[zone].append(Term(identifier=term.identifier,
                                                        prefLabel=term.preferredForm))
                for node, name in boundaries.items():
                    c = Counter(terms[node])
                    c = sorted(c.items(), key=lambda pair: pair[1], reverse=True)
                    descripteurs = ET.Element("DESCRIPTEURS")
                    for term, freq in c:
                        descripteur = ET.Element("DESCRIPTEUR", Id=term.identifier, Pref=term.prefLabel, Freq=str(freq))
                        descripteurs.append(descripteur)
                    node.insert(0, descripteurs)

                data = ET.tostring(root, encoding=encoding, pretty_print=True)
            resp = Response(content=data, media_type="application/xml")
            resp.charset = encoding
            return resp
        except BaseException as err:
            raise err

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return RFXmlParameters
