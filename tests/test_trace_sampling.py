import json

from src.analytics.trace_sampling import (
    summarize_trace_diversity
)


def load_traces():

    with open(
        "outputs/sampled_traces.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def test_trace_count(
    traces
):

    print(
        "\n[TEST] Trace count..."
    )

    assert (
        len(traces) <= 50
    )

    assert (
        len(traces) > 0
    )

    print("PASS")


def test_required_fields(
    traces
):

    print(
        "\n[TEST] Required fields..."
    )

    required = {

        "session_id",
        "segment",
        "ordered_steps",
        "validation_errors",
        "durations",
        "final_step",
        "converted_to_first_trade"
    }

    for trace in traces:

        assert required.issubset(
            trace.keys()
        )

    print("PASS")


def test_friction_present(
    traces
):

    print(
        "\n[TEST] Friction traces exist..."
    )

    found = False

    for trace in traces:

        errors = trace[
            "validation_errors"
        ]

        codes = [
            e["code"]
            for e in errors
        ]

        if (
            "invalid_country_code"
            in codes
        ):
            found = True

    assert found, (
        "Expected signup friction "
        "trace not found"
    )

    print("PASS")


def test_successful_and_failed(
    traces
):

    print(
        "\n[TEST] Success/failure diversity..."
    )

    converted = any(
        t[
            "converted_to_first_trade"
        ]
        for t in traces
    )

    failed = any(
        not t[
            "converted_to_first_trade"
        ]
        for t in traces
    )

    assert converted
    assert failed

    print("PASS")


def test_segment_diversity(
    traces
):

    print(
        "\n[TEST] Segment diversity..."
    )

    summary = (
        summarize_trace_diversity(
            traces
        )
    )

    assert (
        len(summary["countries"])
        >= 3
    )

    assert (
        len(summary["devices"])
        >= 2
    )

    assert (
        len(summary["languages"])
        >= 2
    )

    print("PASS")


def run_all_tests():

    traces = load_traces()

    test_trace_count(
        traces
    )

    test_required_fields(
        traces
    )

    test_friction_present(
        traces
    )

    test_successful_and_failed(
        traces
    )

    test_segment_diversity(
        traces
    )

    print(
        "\nALL TRACE TESTS PASSED"
    )


if __name__ == "__main__":

    run_all_tests()