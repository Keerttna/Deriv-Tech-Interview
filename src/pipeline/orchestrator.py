from src.analytics.data_extension import (
    extend_dataset
)

from src.analytics.session_reconstruction import (
    reconstruct_sessions
)

from src.utils.file_io import save_json


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

    print("\n=== PHASE 2 COMPLETE ===\n")