def generate_sequential_plan(
    experiments
):

    lines = []

    lines.append(
        "# Sequential Experiment Plan\n"
    )

    for idx, exp in enumerate(
        experiments,
        start=1
    ):

        lines.append(

            (
                f"## Experiment {idx}\n"
                f"- Name: {exp['name']}\n"
                f"- Dependency Rationale: "
                f"Run independently to avoid "
                f"interaction effects.\n"
                f"- Cooldown Period: 3 days\n"
                f"- Decision Gate: "
                f"Proceed only if guardrails "
                f"remain stable.\n"
            )
        )

    return "\n".join(lines)