import json


def load_json(path):

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def test_hypotheses():

    hypotheses = load_json(
        "outputs/hypotheses.json"
    )

    assert len(hypotheses) >= 6

    print("PASS hypotheses")


def test_rankings():

    ranked = load_json(
        "outputs/ranked_hypotheses.json"
    )

    lifts = [
        x["lift_potential"]
        for x in ranked
    ]

    assert lifts == sorted(
        lifts,
        reverse=True
    )

    print("PASS rankings")


def test_experiments():

    experiments = load_json(
        "outputs/experiments.json"
    )

    for exp in experiments:

        assert (
            exp[
                "sample_size_per_arm"
            ] > 0
        )

        assert (
            exp[
                "guardrail_metric"
            ]
        )

    print("PASS experiments")


def run_all():

    test_hypotheses()

    test_rankings()

    test_experiments()

    print(
        "\nALL PHASE 5 TESTS PASSED"
    )


if __name__ == "__main__":

    run_all()