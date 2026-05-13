import numpy as np

from src.utils.constants import (
    FUNNEL_STAGES
)

def safe_divide(
    numerator,
    denominator
):
    """
    Prevent division-by-zero errors.
    """

    if denominator == 0:
        return 0.0

    return round(
        numerator / denominator,
        4
    )

def extract_step_durations(
    sessions,
    step
):
    """
    Collect all durations for a given step.
    """

    durations = []

    for session in sessions:

        session_durations = session.get(
            "durations",
            {}
        )

        if step in session_durations:

            durations.append(
                session_durations[step]
            )

    return durations

def compute_funnel_metrics(
    sessions
):
    """
    Deterministically compute funnel metrics.
    """

    funnel_results = []

    total_sessions = len(sessions)

    for index, step in enumerate(
        FUNNEL_STAGES
    ):

        # --------------------------------------------------
        # Determine next step
        # --------------------------------------------------

        next_step = None

        if index < len(FUNNEL_STAGES) - 1:
            next_step = FUNNEL_STAGES[
                index + 1
            ]

        # --------------------------------------------------
        # Entries
        # --------------------------------------------------

        entries = sum(
            1
            for session in sessions
            if step in session[
                "steps_reached"
            ]
        )

        # --------------------------------------------------
        # Completions
        # --------------------------------------------------

        if next_step:

            completions = sum(
                1
                for session in sessions
                if (
                    step
                    in session[
                        "steps_reached"
                    ]
                    and next_step
                    in session[
                        "steps_reached"
                    ]
                )
            )

        else:
            # Final stage
            completions = sum(
                1
                for session in sessions
                if session[
                    "converted_to_first_trade"
                ]
            )

        # --------------------------------------------------
        # Dropoffs
        # --------------------------------------------------

        dropoffs = entries - completions

        # --------------------------------------------------
        # Rates
        # --------------------------------------------------

        conversion_rate = safe_divide(
            completions,
            entries
        )

        dropoff_rate = safe_divide(
            dropoffs,
            entries
        )

        # --------------------------------------------------
        # Duration Metrics
        # --------------------------------------------------

        durations = extract_step_durations(
            sessions,
            step
        )

        if durations:

            median_duration = round(
                float(
                    np.median(durations)
                ),
                2
            )

            p90_duration = round(
                float(
                    np.percentile(
                        durations,
                        90
                    )
                ),
                2
            )

        else:

            median_duration = 0.0
            p90_duration = 0.0

        # --------------------------------------------------
        # Build metric object
        # --------------------------------------------------

        funnel_results.append({

            "step": step,

            "entries": {
                "count": entries,
                "denominator": total_sessions
            },

            "completions": {
                "count": completions,
                "denominator": entries
            },

            "dropoffs": {
                "count": dropoffs,
                "denominator": entries
            },

            "conversion_rate": conversion_rate,

            "dropoff_rate": dropoff_rate,

            "median_time_spent_seconds":
                median_duration,

            "p90_time_spent_seconds":
                p90_duration
        })

    return funnel_results