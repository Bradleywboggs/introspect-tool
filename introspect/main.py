import argparse
import json
from typing import List, Iterable, TextIO, Tuple

from introspect.introspection import Introspection, IntrospectionsSet


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, default="./introspect.txt")
    args = parser.parse_args()
    return vars(args)


def get_introspections_json(file_handle: TextIO) -> Iterable[str]:
    return (line for line in file_handle.readlines())


def get_introspections(introspection_json: List[str]) -> Iterable[Introspection]:
    try:
        return (Introspection(**json.loads(i)) for i in introspection_json)
    except TypeError:
        raise TypeError("File data is not valid json")


def get_keyed_introspections(
    introspections: Iterable[Introspection],
) -> Tuple[IntrospectionsSet, IntrospectionsSet]:
    primary = {}
    comparison = {}
    for i in introspections:
        if i.id not in primary:
            primary = {**primary, i.id: i}
        else:
            comparison = {**comparison, i.id: i}
    return primary, comparison


def analyse_introspections(primary: IntrospectionsSet, comparison: IntrospectionsSet) -> None:
    for identifier, introspection in primary.items():
        comparison_value = comparison.get(identifier)
        if comparison_value:
            introspection.compare(comparison_value)


def main():
    args = get_args()
    with open(args.get("file"), "r") as f:
        raw_introspection_data = get_introspections_json(f)
        introspections = get_introspections(raw_introspection_data)
        primary, comparison = get_keyed_introspections(introspections)
        analyse_introspections(primary, comparison)


if __name__ == "__main__":
    main()
