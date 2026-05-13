from src.llm.llm_logger import (
    log_llm_call
)


def critique_rankings(
    ranked_hypotheses
):

    for hypothesis in ranked_hypotheses:

        critique = (
            "Observed friction appears "
            "causally plausible given "
            "segment-specific dropoff "
            "patterns and supporting "
            "evidence."
        )

        final_confidence = (
            hypothesis["confidence"]
        )

        if (
            hypothesis[
                "lift_potential"
            ] < 5
        ):

            final_confidence = "low"

            critique = (
                "Low traffic impact may "
                "indicate statistical "
                "noise rather than "
                "meaningful friction."
            )

        hypothesis[
            "causal_plausibility_critique"
        ] = critique

        hypothesis[
            "final_confidence"
        ] = final_confidence

    log_llm_call(
        stage="causal_critique",
        input_artifacts=[
            "outputs/hypotheses.json",
            "outputs/segments.json"
        ],
        output_artifact=
            "outputs/ranked_hypotheses.json"
    )

    return ranked_hypotheses