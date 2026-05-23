"""Shared helpers for parametrized route tests."""

from typing import Any


def assert_list_field_values(items: list[dict], field: str, values: list[Any]) -> None:
    for item in items:
        assert item[field] in values


def assert_nested_field_values(
    items: list[dict], field: str, subfield: str, values: list[Any]
) -> None:
    for item in items:
        assert item[subfield] in values


def apply_response_checks(
    json_data: dict | list, checks: list[dict] | None, *, is_list: bool = False
) -> None:
    if not checks:
        return

    for check in checks:
        field = check["field"]

        if "subfields" in check:
            if is_list:
                raise ValueError("subfield checks require a dict response")
            nested_items = json_data[field]
            for item in nested_items:
                for subfield_check in check["subfields"]:
                    assert item[subfield_check["subfield"]] in subfield_check["values"]
            continue

        values = check["values"]
        if is_list:
            assert_list_field_values(json_data, field, values)
        else:
            assert json_data[field] in values
