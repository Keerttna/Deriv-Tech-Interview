import json
from pathlib import Path


REQUIRED_FILES = [

    "outputs/funnel.json",

    "outputs/segments.json",

    "outputs/sampled_traces.json",

    "outputs/hypotheses.json",

    "outputs/ranked_hypotheses.json",

    "outputs/experiments.json",

    "outputs/friction_report.md",

    "outputs/sample_size_model.md",

    "outputs/llm_calls.jsonl"
]


def validate_exists():

    for file in REQUIRED_FILES:

        assert Path(file).exists(), (
            f"Missing artifact: {file}"
        )

    print("PASS artifact existence")


def validate_json():

    json_files = [

        f for f in REQUIRED_FILES
        if f.endswith(".json")
    ]

    for file in json_files:

        with open(
            file,
            "r",
            encoding="utf-8"
        ) as f:

            json.load(f)

    print("PASS JSON validity")


def validate_experiments():

    with open(
        "outputs/experiments.json",
        "r",
        encoding="utf-8"
    ) as f:

        experiments = json.load(f)

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

    print(
        "PASS experiment validation"
    )


def run_validation():

    validate_exists()

    validate_json()

    validate_experiments()

    print(
        "\nALL VALIDATIONS PASSED"
    )


if __name__ == "__main__":

    run_validation()