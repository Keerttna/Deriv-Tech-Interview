def compute_lift_potential(
    segment_dropoff_rate,
    baseline_dropoff_rate,
    impacted_volume
):

    return round(

        impacted_volume
        * max(
            0,
            (
                segment_dropoff_rate
                - baseline_dropoff_rate
            )
        ),

        4
    )


def rank_hypotheses(
    hypotheses,
    segments
):

    ranked = []

    # --------------------------------------------------
    # Compare segment vs baseline
    # --------------------------------------------------

    for hypothesis in hypotheses:

        step = hypothesis["step"]

        segment_key = (
            hypothesis["segment"]
            ["segment_key"]
        )

        matching = [

            x for x in segments

            if (
                x["segment_key"]
                == segment_key
                and x["step"] == step
            )
        ]

        if not matching:
            continue

        row = matching[0]

        segment_dropoff = row[
            "dropoff_rate"
        ]

        impacted_volume = row[
            "entries"
        ]["count"]

        # ----------------------------------------------
        # Baseline = all other segments
        # ----------------------------------------------

        peer_rows = [

            x for x in segments

            if (
                x["step"] == step
                and x["segment_key"]
                != segment_key
            )
        ]

        if peer_rows:

            baseline_dropoff = (
                sum(
                    x["dropoff_rate"]
                    for x in peer_rows
                )
                / len(peer_rows)
            )

        else:
            baseline_dropoff = 0

        lift = compute_lift_potential(
            segment_dropoff,
            baseline_dropoff,
            impacted_volume
        )

        enriched = dict(
            hypothesis
        )

        enriched[
            "lift_potential"
        ] = lift

        enriched[
            "baseline_dropoff_rate"
        ] = round(
            baseline_dropoff,
            4
        )

        ranked.append(
            enriched
        )

    # --------------------------------------------------
    # Deterministic ranking
    # --------------------------------------------------

    ranked = sorted(
        ranked,
        key=lambda x: (
            x["lift_potential"]
        ),
        reverse=True
    )

    for idx, row in enumerate(
        ranked,
        start=1
    ):

        row["rank"] = idx

    return ranked