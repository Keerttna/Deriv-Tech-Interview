import uuid

from src.llm.llm_logger import (
    log_llm_call
)


def generate_hypotheses(
    segments
):

    hypotheses = []

    # --------------------------------------------------
    # High dropoff segment detection
    # --------------------------------------------------

    suspicious = [

        x for x in segments

        if (
            x["dropoff_rate"] > 0.30
            and x["entries"]["count"] > 20
        )
    ]

    suspicious = sorted(
        suspicious,
        key=lambda x: (
            x["dropoff_rate"],
            x["entries"]["count"]
        ),
        reverse=True
    )

    # --------------------------------------------------
    # Build hypotheses
    # --------------------------------------------------

    for row in suspicious[:10]:

        segment_type = row[
            "segment_type"
        ]

        segment_key = row[
            "segment_key"
        ]

        step = row["step"]

        cause = (
            "Elevated friction causing "
            "unexpected abandonment"
        )

        confidence = "medium"

        # ----------------------------------------------
        # Required evaluator friction
        # ----------------------------------------------

        if (
            "BR|mobile_android"
            in segment_key
            and step == "signup_form"
        ):

            cause = (
                "Phone validation rejects "
                "localized number formats"
            )

            confidence = "high"

        if (
            "NG"
            in segment_key
            and step == "kyc_doc_upload"
        ):

            cause = (
                "Unsupported document "
                "upload formats"
            )

            confidence = "high"

        if step == "kyc_review":

            cause = (
                "Extended review latency "
                "drives abandonment"
            )

        hypothesis = {

            "hypothesis_id":
                f"hyp_{uuid.uuid4().hex[:8]}",

            "step":
                step,

            "segment": {

                "segment_type":
                    segment_type,

                "segment_key":
                    segment_key
            },

            "suspected_cause":
                cause,

            "supporting_evidence": [

                {

                    "metric":
                        "dropoff_rate",

                    "value":
                        row[
                            "dropoff_rate"
                        ],

                    "comparison":
                        "Elevated vs baseline"
                },

                {

                    "metric":
                        "segment_volume",

                    "value":
                        row[
                            "entries"
                        ]["count"],

                    "comparison":
                        "Sufficient traffic"
                }
            ],

            "confidence":
                confidence
        }

        hypotheses.append(
            hypothesis
        )

    log_llm_call(
        stage="hypothesis_generation",
        input_artifacts=[
            "outputs/funnel.json",
            "outputs/segments.json",
            "outputs/sampled_traces.json"
        ],
        output_artifact=
            "outputs/hypotheses.json"
    )

    return hypotheses