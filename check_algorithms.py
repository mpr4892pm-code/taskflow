from algorithms import (
    insertion_sort,
    binary_search,
    linear_search
)


def check(case_name, result, expected):

    if result == expected:
        print(f"PASS: {case_name}")

    else:
        print(
            f"FAIL: {case_name} "
            f"— expected {expected}, got {result}"
        )


# Empty list
data = []

insertion_sort(data, "value")

check(
    "empty insertion sort",
    data,
    []
)


# Single element
data = [
    {"value": 10}
]

insertion_sort(data, "value")

check(
    "single element",
    data,
    [{"value": 10}]
)


# Binary search
data = [
    {"value": 1},
    {"value": 2},
    {"value": 3},
    {"value": 4},
    {"value": 5}
]

check(
    "binary first",
    binary_search(data, 1, "value"),
    0
)

check(
    "binary middle",
    binary_search(data, 3, "value"),
    2
)

check(
    "binary last",
    binary_search(data, 5, "value"),
    4
)

check(
    "binary absent",
    binary_search(data, 10, "value"),
    -1
)