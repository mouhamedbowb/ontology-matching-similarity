"""Step 2 - check that every entity cited in the reference alignments exists in our ontologies.

Usage: python src/check_coverage.py
"""
from data_loading import DATA, load_entities, load_reference


def kind(uri: str, entities: dict) -> str:
    if uri in entities["classes"]:
        return "class"
    if uri in entities["object_properties"] or uri in entities["datatype_properties"]:
        return "property"
    return "unknown"


def main() -> None:
    cache = {}
    totals = {"cells": 0, "class-class": 0, "property-property": 0, "mixed": 0, "unknown": 0}
    unknown_examples = []

    for path in sorted((DATA / "reference-alignment").glob("*.rdf")):
        name1, name2 = path.stem.split("-")
        for name in (name1, name2):
            if name not in cache:
                cache[name] = load_entities(name)

        cells = load_reference(path)
        counts = {"class-class": 0, "property-property": 0, "mixed": 0, "unknown": 0}
        for e1, e2, _relation in cells:
            k1, k2 = kind(e1, cache[name1]), kind(e2, cache[name2])
            if "unknown" in (k1, k2):
                counts["unknown"] += 1
                if len(unknown_examples) < 5:
                    unknown_examples.append((path.name, e1, e2))
            elif k1 == k2 == "class":
                counts["class-class"] += 1
            elif k1 == k2 == "property":
                counts["property-property"] += 1
            else:
                counts["mixed"] += 1

        print(f"{path.name:26} cells={len(cells):3}  "
              f"class-class={counts['class-class']:3}  "
              f"property-property={counts['property-property']:3}  "
              f"mixed={counts['mixed']:2}  unknown={counts['unknown']:2}")
        totals["cells"] += len(cells)
        for key, value in counts.items():
            totals[key] += value

    print("\nTOTAL:", totals)
    if unknown_examples:
        print("\nExamples of entities not found in the ontologies:")
        for example in unknown_examples:
            print("  ", example)


if __name__ == "__main__":
    main()