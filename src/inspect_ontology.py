"""Step 1 - load one OWL ontology and print basic statistics.

Usage: python src/inspect_ontology.py data/raw/ontologies/cmt.owl
"""
import sys
from pathlib import Path

from rdflib import Graph, RDF, RDFS, OWL, URIRef


def local_name(uri) -> str:
    """Return the part of a URI after the last '#' or '/'."""
    text = str(uri)
    for sep in ("#", "/"):
        if sep in text:
            text = text.rsplit(sep, 1)[-1]
    return text


def inspect(path: Path) -> None:
    g = Graph()
    g.parse(path, format="xml")  # OAEI conference ontologies are RDF/XML

    # Keep only named classes: anonymous ones (restrictions) are blank nodes.
    classes = {c for c in g.subjects(RDF.type, OWL.Class) if isinstance(c, URIRef)}
    obj_props = {p for p in g.subjects(RDF.type, OWL.ObjectProperty) if isinstance(p, URIRef)}
    data_props = {p for p in g.subjects(RDF.type, OWL.DatatypeProperty) if isinstance(p, URIRef)}
    labelled = [c for c in classes if (c, RDFS.label, None) in g]
    subclass_links = [
        (s, o) for s, o in g.subject_objects(RDFS.subClassOf)
        if isinstance(s, URIRef) and isinstance(o, URIRef)
    ]

    print(f"File: {path.name}")
    print(f"  triples:                  {len(g)}")
    print(f"  named classes:            {len(classes)}")
    print(f"  object properties:        {len(obj_props)}")
    print(f"  datatype properties:      {len(data_props)}")
    print(f"  classes with rdfs:label:  {len(labelled)}")
    print(f"  subClassOf links (named): {len(subclass_links)}")
    print("  sample classes (local name | label):")
    for c in sorted(classes, key=str)[:8]:
        label = next(iter(g.objects(c, RDFS.label)), None)
        print(f"    {local_name(c):30} | {label}")


if __name__ == "__main__":
    inspect(Path(sys.argv[1]))