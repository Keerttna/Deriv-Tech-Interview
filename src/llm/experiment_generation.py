import uuid

from src.analytics.sample_size import (
    compute_sample_size
)

from src.llm.llm_logger import (
    log_llm_call
)


def generate_experiments(
    ranked_hypotheses
):

    experiments = []

    top = ranked_hypotheses[:4]

    for hypothesis in top:

        baseline = round(
            1
            - hypothesis[
                "supporting_evidence"
            ][0]["value"],
            4
        )

        mde = 0.05

        sample_size = (
            compute_sample_size(
                baseline_rate=baseline,
                minimum_detectable_effect=
                    mde
            )
        )

        experiment = {

            "experiment_id":
                f"exp_{uuid.uuid4().hex[:8]}",

            "name":
                (
                    f"Reduce friction at "
                    f"{hypothesis['step']}"
                ),

            "hypothesis":
                hypothesis[
                    "suspected_cause"
                ],

            "intervention":
                (
                    "Improve onboarding UX "
                    "and validation handling"
                ),

            "primary_metric":
                (
                    "step_conversion_rate"
                ),

            "guardrail_metric":
                (
                    "error_rate"
                ),

            "target_segment":
                hypothesis[
                    "segment"
                ]["segment_key"],

            "minimum_detectable_effect":
                mde,

            "baseline_conversion_rate":
                baseline,

            "sample_size_per_arm":
                sample_size,

            "runtime_estimate":
                "2-3 weeks",

            "success_criteria":
                (
                    "Statistically significant "
                    "improvement in conversion "
                    "without increased error rate"
                )
        }

        experiments.append(
            experiment
        )

    log_llm_call(
        stage="experiment_generation",
        input_artifacts=[
            "outputs/ranked_hypotheses.json"
        ],
        output_artifact=
            "outputs/experiments.json"
    )

    return experiments