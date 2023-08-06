from collections import defaultdict, Counter
from typing import Type

import lxml.etree as ET
from Ranger import RangeBucketMap, Range
from pydantic import BaseModel, Field
from pymultirole_plugins.formatter import FormatterBase, FormatterParameters
from pymultirole_plugins.schema import Document, Boundary, Annotation
from starlette.responses import Response


class RFXmlParameters(FormatterParameters):
    boundaries: str = Field("SECTIONS", description="Name of boundaries to consider")
    with_forms: bool = Field(True, description="Add list of all matching forms")


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
                baseNs = root.nsmap.get(None, None)
                # Ignore all namespaces
                for el in root.iter():
                    if baseNs and el.tag.startswith(f"{{{baseNs}}}"):
                        _, _, el.tag = el.tag.rpartition('}')

                boundaries = {}
                buckets = RangeBucketMap()
                terms = defaultdict(lambda: defaultdict(list))
                for b in document.boundaries.get(parameters.boundaries, []):
                    boundary = Boundary(**b) if isinstance(b, dict) else b
                    r = root.xpath(boundary.name)
                    if len(r) == 1:
                        node = r[0]
                        boundaries[node] = boundary.name
                        buckets[Range.closedOpen(boundary.start, boundary.end)] = node
                for a in document.annotations:
                    annotation = Annotation(**a) if isinstance(a, dict) else a
                    form = document.text[annotation.start:annotation.end]
                    if buckets.contains(annotation.start) and buckets.contains(annotation.end):
                        zones = buckets[Range.closedOpen(annotation.start, annotation.end)]
                        for zone in zones:
                            for term in annotation.terms:
                                terms[zone][term.identifier].append(form)
                for node, name in boundaries.items():
                    if node in terms and terms[node]:
                        descripteurs = ET.Element("DESCRIPTEURS")
                        for ident, forms in terms[node].items():
                            c = Counter(forms)
                            freq = sum(c.values())
                            descripteur = ET.Element("DESCRIPTEUR", Id=ident, Freq=str(freq))
                            if parameters.with_forms:
                                desc_forms = ET.Element("FORMES")
                                for form, ffreq in c.items():
                                    desc_form = ET.Element("FORME", Freq=str(ffreq))
                                    desc_form.text = form
                                    desc_forms.append(desc_form)
                                descripteur.insert(0, desc_forms)
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
