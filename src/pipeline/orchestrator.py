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