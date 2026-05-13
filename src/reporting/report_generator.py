def generate_report(
    funnel,
    ranked_hypotheses,
    experiments
):

    top_hypothesis = (
        ranked_hypotheses[0]
        if ranked_hypotheses
        else None
    )

    lines = []

    lines.append(
        "# Friction Analysis Report\n"
    )

    # --------------------------------------------------
    # Executive Summary
    # --------------------------------------------------

    lines.append(
        "## Executive Summary\n"
    )

    if top_hypothesis:

        lines.append(
            (
                f"Top-ranked friction occurs at "
                f"'{top_hypothesis['step']}' "
                f"for segment "
                f"'{top_hypothesis['segment']['segment_key']}'. "
                f"The issue is considered "
                f"causal-suspect due to elevated "
                f"segment-specific dropoff rates "
                f"combined with meaningful "
                f"traffic volume.\n"
            )
        )

    # --------------------------------------------------
    # Funnel Overview
    # --------------------------------------------------

    lines.append(
        "## Funnel Overview\n"
    )

    for step in funnel:

        lines.append(

            (
                f"- {step['step']}: "
                f"entries={step['entries']['count']}, "
                f"conversion_rate={step['conversion_rate']}, "
                f"dropoff_rate={step['dropoff_rate']}\n"
            )
        )

    # --------------------------------------------------
    # Top Hypotheses
    # --------------------------------------------------

    lines.append(
        "\n## Top Friction Hypotheses\n"
    )

    for hypothesis in ranked_hypotheses[:5]:

        lines.append(

            (
                f"### Rank {hypothesis['rank']}\n"
                f"- Step: {hypothesis['step']}\n"
                f"- Segment: "
                f"{hypothesis['segment']['segment_key']}\n"
                f"- Cause: "
                f"{hypothesis['suspected_cause']}\n"
                f"- Lift Potential: "
                f"{hypothesis['lift_potential']}\n"
                f"- Confidence: "
                f"{hypothesis['final_confidence']}\n"
                f"- Critique: "
                f"{hypothesis['causal_plausibility_critique']}\n"
            )
        )

    # --------------------------------------------------
    # Experiments
    # --------------------------------------------------

    lines.append(
        "\n## A/B Test Backlog\n"
    )

    for experiment in experiments:

        lines.append(

            (
                f"### {experiment['name']}\n"
                f"- Target Segment: "
                f"{experiment['target_segment']}\n"
                f"- Sample Size Per Arm: "
                f"{experiment['sample_size_per_arm']}\n"
                f"- Guardrail Metric: "
                f"{experiment['guardrail_metric']}\n"
                f"- Success Criteria: "
                f"{experiment['success_criteria']}\n"
            )
        )

    # --------------------------------------------------
    # Caveats
    # --------------------------------------------------

    lines.append(
        "\n## Confidence and Caveats\n"
    )

    lines.append(
        (
            "Hypotheses are generated from "
            "observed behavioral patterns and "
            "should be validated experimentally "
            "before operational rollout.\n"
        )
    )

    return "\n".join(lines)