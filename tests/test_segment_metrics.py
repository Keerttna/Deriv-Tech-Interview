import json


def load_segments():

    with open(
        "outputs/segments.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def test_segments_exist(
    segments
):

    print(
        "\n[TEST] Segments generated..."
    )

    assert len(segments) > 0

    print("PASS")


def test_required_segment_types(
    segments
):

    print(
        "\n[TEST] Required segment types..."
    )

    segment_types = set(
        x["segment_type"]
        for x in segments
    )

    required = {
        "country",
        "device",
        "lang",
        "country_device",
        "device_lang",
        "country_lang"
    }

    missing = (
        required
        - segment_types
    )

    assert not missing, (
        f"Missing segment types: "
        f"{missing}"
    )

    print("PASS")


def test_rates_valid(
    segments
):

    print(
        "\n[TEST] Segment rates valid..."
    )

    for row in segments:

        total = round(
            row["conversion_rate"]
            + row["dropoff_rate"],
            4
        )

        if row["entries"]["count"] > 0:

            assert total == 1.0, (
                f"Invalid rates for "
                f"{row['segment_key']}"
            )

    print("PASS")


def test_br_signup_friction(
    segments
):

    print(
        "\n[TEST] BR Android signup friction..."
    )

    matches = [

        x for x in segments

        if (
            x["segment_type"]
            == "country_device"
            and x["segment_key"]
            == "BR|mobile_android"
            and x["step"]
            == "signup_form"
        )
    ]

    assert len(matches) > 0

    segment = matches[0]

    assert (
        segment["dropoff_rate"]
        > 0.30
    ), (
        "Expected elevated BR "
        "signup friction not found"
    )

    print("PASS")


def test_kyc_latency(
    segments
):

    print(
        "\n[TEST] KYC latency exists..."
    )

    kyc_rows = [

        x for x in segments

        if x["step"]
        == "kyc_review"
    ]

    high_latency = any(
        x[
            "p90_time_spent_seconds"
        ] > 60
        for x in kyc_rows
    )

    assert high_latency, (
        "Expected KYC latency "
        "not found"
    )

    print("PASS")


def run_all_tests():

    segments = load_segments()

    test_segments_exist(
        segments
    )

    test_required_segment_types(
        segments
    )

    test_rates_valid(
        segments
    )

    test_br_signup_friction(
        segments
    )

    test_kyc_latency(
        segments
    )

    print(
        "\nALL SEGMENT TESTS PASSED"
    )


if __name__ == "__main__":

    run_all_tests()