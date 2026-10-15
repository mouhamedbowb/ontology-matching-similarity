"""Helpers to load the OAEI Conference ontologies and their reference alignments."""
from pathlib import Path
import xml.etree.ElementTree as ET

from rdflib import Graph, RDF, OWL, URIRef

DATA = Path("data/raw")

# Names used in the alignment file names -> real ontology file names
ONTOLOGY_FILES = {
    "cmt": "cmt.owl",
    "confOf": "confof.owl",
    "edas": "edas.owl",
    "ekaw": "ekaw.owl",
    "iasted": "iasted.owl",
    "sigkdd": "sigkdd.owl",
    "conference": "Conference.owl",
}

RDF_RESOURCE = "{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource"


def local_name(uri: str) -> str:
    """Part of a URI after the last '#' or '/'."""
    for sep in ("#", "/"):
        if sep in uri:
            uri = uri.rsplit(sep, 1)[-1]
    return uri


def load_entities(name: str) -> dict:
    """Return the named classes and properties of one ontology, as sets of URI strings."""
    g = Graph()
    g.parse(DATA / "ontologies" / ONTOLOGY_FILES[name], format="xml")

    def named(rdf_type):
        return {str(s) for s in g.subjects(RDF.type, rdf_type) if isinstance(s, URIRef)}

    return {
        "classes": named(OWL.Class),
        "object_properties": named(OWL.ObjectProperty),
        "datatype_properties": named(OWL.DatatypeProperty),
    }


def load_reference(path: Path) -> list:
    """Read one reference alignment file: a list of (entity1, entity2, relation)."""
    root = ET.parse(path).getroot()
    cells = []
    for cell in root.iterfind(".//{*}Cell"):
        entity1 = cell.find("{*}entity1").get(RDF_RESOURCE)
        entity2 = cell.find("{*}entity2").get(RDF_RESOURCE)
        relation = cell.find("{*}relation").text
        cells.append((entity1, entity2, relation))
    return cells