import numpy as np

from src.utils.constants import (
    FUNNEL_STAGES
)


def safe_divide(
    numerator,
    denominator
):

    if denominator == 0:
        return 0.0

    return round(
        numerator / denominator,
        4
    )


def compute_duration_metrics(
    sessions,
    step
):

    durations = []

    for session in sessions:

        step_durations = session.get(
            "durations",
            {}
        )

        if step in step_durations:

            durations.append(
                step_durations[step]
            )

    if not durations:

        return {
            "median": 0.0,
            "p90": 0.0
        }

    return {
        "median": round(
            float(
                np.median(durations)
            ),
            2
        ),
        "p90": round(
            float(
                np.percentile(
                    durations,
                    90
                )
            ),
            2
        )
    }


def build_segment_groups(
    sessions
):

    grouped = {}

    # --------------------------------------------------
    # Single-dimension segments
    # --------------------------------------------------

    for dimension in [
        "country",
        "device",
        "lang"
    ]:

        for session in sessions:

            key = (
                dimension,
                str(
                    session[dimension]
                )
            )

            grouped.setdefault(
                key,
                []
            ).append(session)

    # --------------------------------------------------
    # Pairwise segments
    # --------------------------------------------------

    pair_dimensions = [
        ("country", "device"),
        ("device", "lang"),
        ("country", "lang")
    ]

    for dim1, dim2 in pair_dimensions:

        for session in sessions:

            segment_key = (
                f"{session[dim1]}"
                f"|{session[dim2]}"
            )

            key = (
                f"{dim1}_{dim2}",
                segment_key
            )

            grouped.setdefault(
                key,
                []
            ).append(session)

    return grouped


def compute_segment_metrics(
    sessions
):

    grouped_segments = (
        build_segment_groups(
            sessions
        )
    )

    results = []

    # --------------------------------------------------
    # Process each segment
    # --------------------------------------------------

    for (
        segment_type,
        segment_key
    ), segment_sessions in (
        grouped_segments.items()
    ):

        segment_size = len(
            segment_sessions
        )

        # ----------------------------------------------
        # Compute metrics for each funnel stage
        # ----------------------------------------------

        for index, step in enumerate(
            FUNNEL_STAGES
        ):

            next_step = None

            if index < (
                len(FUNNEL_STAGES) - 1
            ):
                next_step = (
                    FUNNEL_STAGES[
                        index + 1
                    ]
                )

            # ------------------------------------------
            # Entries
            # ------------------------------------------

            entries = sum(
                1
                for session
                in segment_sessions
                if step in session[
                    "steps_reached"
                ]
            )

            # ------------------------------------------
            # Completions
            # ------------------------------------------

            if next_step:

                completions = sum(
                    1
                    for session
                    in segment_sessions
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

                completions = sum(
                    1
                    for session
                    in segment_sessions
                    if session[
                        "converted_to_first_trade"
                    ]
                )

            # ------------------------------------------
            # Dropoffs
            # ------------------------------------------

            dropoffs = (
                entries
                - completions
            )

            # ------------------------------------------
            # Rates
            # ------------------------------------------

            conversion_rate = (
                safe_divide(
                    completions,
                    entries
                )
            )

            dropoff_rate = (
                safe_divide(
                    dropoffs,
                    entries
                )
            )

            # ------------------------------------------
            # Duration metrics
            # ------------------------------------------

            duration_metrics = (
                compute_duration_metrics(
                    segment_sessions,
                    step
                )
            )

            # ------------------------------------------
            # Build result
            # ------------------------------------------

            results.append({

                "segment_type":
                    segment_type,

                "segment_key":
                    segment_key,

                "segment_size":
                    segment_size,

                "step":
                    step,

                "entries": {
                    "count": entries,
                    "denominator":
                        segment_size
                },

                "completions": {
                    "count":
                        completions,
                    "denominator":
                        entries
                },

                "dropoffs": {
                    "count":
                        dropoffs,
                    "denominator":
                        entries
                },

                "conversion_rate":
                    conversion_rate,

                "dropoff_rate":
                    dropoff_rate,

                "median_time_spent_seconds":
                    duration_metrics[
                        "median"
                    ],

                "p90_time_spent_seconds":
                    duration_metrics[
                        "p90"
                    ]
            })

    return results