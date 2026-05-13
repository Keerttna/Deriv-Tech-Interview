import json

from src.utils.constants import (
    FUNNEL_STAGES
)


def load_funnel():

    with open(
        "outputs/funnel.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def test_stage_order(funnel):

    print(
        "\n[TEST] Funnel stage order..."
    )

    actual_order = [
        x["step"]
        for x in funnel
    ]

    assert (
        actual_order
        == FUNNEL_STAGES
    ), (
        f"Stage order mismatch.\n"
        f"Expected: {FUNNEL_STAGES}\n"
        f"Actual: {actual_order}"
    )

    print("PASS")


def test_monotonic_entries(funnel):

    print(
        "\n[TEST] Funnel entries decrease..."
    )

    entries = [
        x["entries"]["count"]
        for x in funnel
    ]

    for i in range(
        len(entries) - 1
    ):

        assert (
            entries[i + 1]
            <= entries[i]
        ), (
            f"Entries increased between "
            f"{FUNNEL_STAGES[i]} and "
            f"{FUNNEL_STAGES[i+1]}"
        )

    print("PASS")


def test_rates_sum_to_one(funnel):

    print(
        "\n[TEST] Conversion + dropoff = 1..."
    )

    for step in funnel:

        total = round(
            step["conversion_rate"]
            + step["dropoff_rate"],
            4
        )

        assert (
            total == 1.0
        ), (
            f"Rates invalid for "
            f"{step['step']} "
            f"(total={total})"
        )

    print("PASS")


def test_duration_metrics_exist(funnel):

    print(
        "\n[TEST] Duration metrics exist..."
    )

    for step in funnel:

        median = step[
            "median_time_spent_seconds"
        ]

        p90 = step[
            "p90_time_spent_seconds"
        ]

        assert median >= 0
        assert p90 >= 0

    print("PASS")


def test_kyc_latency_emerges(funnel):

    print(
        "\n[TEST] KYC review latency exists..."
    )

    kyc_review = next(
        x for x in funnel
        if x["step"] == "kyc_review"
    )

    assert (
        kyc_review[
            "p90_time_spent_seconds"
        ] > 60
    ), (
        "Expected elevated KYC "
        "review latency not found"
    )

    print("PASS")


def test_signup_dropoff_high(funnel):

    print(
        "\n[TEST] Signup dropoff elevated..."
    )

    signup = next(
        x for x in funnel
        if x["step"] == "signup_form"
    )

    assert (
        signup["dropoff_rate"]
        > 0.25
    ), (
        "Signup dropoff rate "
        "unexpectedly low"
    )

    print("PASS")


def run_all_tests():

    funnel = load_funnel()

    test_stage_order(funnel)

    test_monotonic_entries(funnel)

    test_rates_sum_to_one(funnel)

    test_duration_metrics_exist(
        funnel
    )

    test_kyc_latency_emerges(
        funnel
    )

    test_signup_dropoff_high(
        funnel
    )

    print(
        "\nALL FUNNEL TESTS PASSED"
    )


if __name__ == "__main__":

    run_all_tests()