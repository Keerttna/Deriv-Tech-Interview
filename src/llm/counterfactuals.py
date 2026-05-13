from src.llm.llm_logger import (
    log_llm_call
)


def generate_counterfactuals(
    top_hypothesis
):

    output = {

        "hypothesis_id":
            top_hypothesis[
                "hypothesis_id"
            ],

        "alternative_explanations": [

            "Tracking instrumentation issue",

            "Traffic quality difference",

            "Localization mismatch",

            "Device-specific browser issue"
        ],

        "confidence_adjustment":
            "none",

        "reason":
            (
                "Observed friction aligns "
                "consistently with segment-"
                "specific behavioral signals."
            )
    }

    log_llm_call(
        stage="counterfactual_check",
        input_artifacts=[
            "outputs/ranked_hypotheses.json"
        ],
        output_artifact=
            "outputs/counterfactual_check.json"
    )

    return output