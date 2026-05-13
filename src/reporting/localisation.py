def generate_localisation_insights(
    ranked_hypotheses
):

    insights = []

    for hypothesis in ranked_hypotheses:

        segment_key = (
            hypothesis["segment"]
            ["segment_key"]
        )

        if (
            "pt-BR"
            in segment_key
        ):

            insights.append({

                "language":
                    "pt-BR",

                "step":
                    hypothesis["step"],

                "issue":
                    (
                        "Localized onboarding "
                        "friction detected"
                    ),

                "evidence":
                    (
                        "Elevated segment "
                        "dropoff and validation "
                        "errors"
                    ),

                "confidence":
                    "high"
            })

    return insights