import json
from pathlib import Path

from starlette.responses import Response

from pyformatters_xml_rf.xml_rf import RFXmlFormatter, RFXmlParameters
from pymultirole_plugins.schema import Document
import lxml.etree as ET


def test_xml_rf():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/response_1621334812115.json')
    with source.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs[0])
        formatter = RFXmlFormatter()
        options = RFXmlParameters()
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert resp.media_type == "application/xml"
        root = ET.fromstring(resp.body)
        baseNs = root.nsmap.get(None, None)
        all_descs = list(root.iterdescendants(f"{{{baseNs}}}DESCRIPTEUR"))
        all_forms = list(root.iterdescendants(f"{{{baseNs}}}FORME"))
        assert len(all_descs) > 0
        assert len(all_forms) > 0


def test_xml_rf_without_forms():
    testdir = Path(__file__).parent
    source = Path(testdir, 'data/response_1621334812115.json')
    with source.open("r") as fin:
        docs = json.load(fin)
        doc = Document(**docs[0])
        formatter = RFXmlFormatter()
        options = RFXmlParameters(with_forms=False)
        resp: Response = formatter.format(doc, options)
        assert resp.status_code == 200
        assert resp.media_type == "application/xml"
        root = ET.fromstring(resp.body)
        baseNs = root.nsmap.get(None, None)
        all_descs = list(root.iterdescendants(f"{{{baseNs}}}DESCRIPTEUR"))
        all_forms = list(root.iterdescendants(f"{{{baseNs}}}FORME"))
        assert len(all_descs) > 0
        assert len(all_forms) == 0
