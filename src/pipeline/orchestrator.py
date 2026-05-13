from src.analytics.data_extension import (
    extend_dataset
)

from src.analytics.session_reconstruction import (
    reconstruct_sessions
)

from src.utils.file_io import save_json

from src.analytics.funnel_metrics import (
    compute_funnel_metrics
)

from src.analytics.segment_metrics import (
    compute_segment_metrics
)

from src.analytics.trace_sampling import (
    sample_representative_traces
)

from src.llm.hypothesis_generation import (
    generate_hypotheses
)

from src.analytics.lift_ranking import (
    rank_hypotheses
)

from src.llm.critique import (
    critique_rankings
)

from src.llm.experiment_generation import (
    generate_experiments
)

from src.reporting.report_generator import (
    generate_report
)

from src.llm.counterfactuals import (
    generate_counterfactuals
)

from src.reporting.localisation import (
    generate_localisation_insights
)

from src.reporting.variant_copy import (
    generate_variant_copy
)

from src.reporting.sequential_plan import (
    generate_sequential_plan
)


def run_pipeline():

    print("\n=== PIPELINE STARTED ===\n")

    # --------------------------------------------------
    # Extend dataset
    # --------------------------------------------------

    print("Generating synthetic dataset...")

    events = extend_dataset()

    save_json(
        events,
        "outputs/events_extended.json"
    )

    print(
        f"Generated {len(events)} events"
    )

    # --------------------------------------------------
    # Reconstruct sessions
    # --------------------------------------------------

    print(
        "\nReconstructing sessions..."
    )

    sessions = reconstruct_sessions(events)

    save_json(
        sessions,
        "outputs/reconstructed_sessions.json"
    )

    print(
        f"Reconstructed {len(sessions)} sessions"
    )

        # --------------------------------------------------
    # Funnel aggregation
    # --------------------------------------------------

    print(
        "\nComputing funnel metrics..."
    )

    funnel_metrics = (
        compute_funnel_metrics(
            sessions
        )
    )

    save_json(
        funnel_metrics,
        "outputs/funnel.json"
    )

    print(
        "Generated funnel.json"
    )

        # --------------------------------------------------
    # Segment aggregation
    # --------------------------------------------------

    print(
        "\nComputing segment metrics..."
    )

    segment_metrics = (
        compute_segment_metrics(
            sessions
        )
    )

    save_json(
        segment_metrics,
        "outputs/segments.json"
    )

    print(
        "Generated segments.json"
    )

        # --------------------------------------------------
    # Trace sampling
    # --------------------------------------------------

    print(
        "\nSampling representative traces..."
    )

    sampled_traces = (
        sample_representative_traces(
            sessions
        )
    )

    save_json(
        sampled_traces,
        "outputs/sampled_traces.json"
    )

    print(
        f"Generated "
        f"{len(sampled_traces)} "
        f"sampled traces"
    )

        # --------------------------------------------------
    # Hypothesis generation
    # --------------------------------------------------

    print(
        "\nGenerating hypotheses..."
    )

    hypotheses = (
        generate_hypotheses(
            segment_metrics
        )
    )

    save_json(
        hypotheses,
        "outputs/hypotheses.json"
    )

    # --------------------------------------------------
    # Lift ranking
    # --------------------------------------------------

    print(
        "\nRanking hypotheses..."
    )

    ranked = rank_hypotheses(
        hypotheses,
        segment_metrics
    )

    ranked = critique_rankings(
        ranked
    )

    save_json(
        ranked,
        "outputs/ranked_hypotheses.json"
    )

    # --------------------------------------------------
    # Experiment generation
    # --------------------------------------------------

    print(
        "\nGenerating experiments..."
    )

    experiments = (
        generate_experiments(
            ranked
        )
    )

    save_json(
        experiments,
        "outputs/experiments.json"
    )

        # --------------------------------------------------
    # Final report
    # --------------------------------------------------

    print(
        "\nGenerating final report..."
    )

    report = generate_report(
        funnel_metrics,
        ranked,
        experiments
    )

    with open(
        "outputs/friction_report.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(report)

    # --------------------------------------------------
    # Counterfactual check
    # --------------------------------------------------

    counterfactual = (
        generate_counterfactuals(
            ranked[0]
        )
    )

    save_json(
        counterfactual,
        "outputs/counterfactual_check.json"
    )

    # --------------------------------------------------
    # Localization insights
    # --------------------------------------------------

    localization = (
        generate_localisation_insights(
            ranked
        )
    )

    save_json(
        localization,
        "outputs/localisation_insights.json"
    )

    # --------------------------------------------------
    # Variant copy
    # --------------------------------------------------

    variant_copy = (
        generate_variant_copy(
            experiments[0]
        )
    )

    with open(
        "outputs/experiment_variant_copy.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(variant_copy)

    # --------------------------------------------------
    # Sequential plan
    # --------------------------------------------------

    sequential_plan = (
        generate_sequential_plan(
            experiments
        )
    )

    with open(
        "outputs/sequential_test_plan.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(sequential_plan)