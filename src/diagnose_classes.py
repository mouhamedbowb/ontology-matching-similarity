"""Step 1b - find out why the number of classes differs from the OAEI table.

Usage: python src/diagnose_classes.py data/raw/ontologies/cmt.owl
"""
import sys
from pathlib import Path

from rdflib import Graph, RDF, RDFS, OWL, URIRef, BNode, XSD

IGNORED_NAMESPACES = (str(XSD), str(RDF), str(RDFS), str(OWL))


def main(path: Path) -> None:
    g = Graph()
    g.parse(path, format="xml")

    declared = set(g.subjects(RDF.type, OWL.Class))
    named = {c for c in declared if isinstance(c, URIRef)}
    anonymous = {c for c in declared if isinstance(c, BNode)}
    rdfs_classes = {c for c in g.subjects(RDF.type, RDFS.Class) if isinstance(c, URIRef)}

    # URIs used like classes but never declared as owl:Class
    used = set()
    for pred in (RDFS.subClassOf, OWL.equivalentClass, OWL.disjointWith):
        for s, o in g.subject_objects(pred):
            used.update(x for x in (s, o) if isinstance(x, URIRef))
    for pred in (RDFS.domain, RDFS.range):
        used.update(o for o in g.objects(None, pred) if isinstance(o, URIRef))
    undeclared = {
        u for u in used
        if u not in named and not str(u).startswith(IGNORED_NAMESPACES)
    }

    print(f"File: {path.name}")
    print(f"  owl:Class, named (URI):          {len(named)}")
    print(f"  owl:Class, anonymous (blank):    {len(anonymous)}")
    print(f"  rdfs:Class, named:               {len(rdfs_classes)}")
    print(f"  used as class but undeclared:    {len(undeclared)}")
    for u in sorted(undeclared, key=str)[:10]:
        print(f"    {u}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))

