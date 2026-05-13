import random
from datetime import datetime

from datetime import timedelta
from src.utils.helpers import (
    generate_session_id,
    generate_user_id,
    iso_timestamp
)

from src.utils.file_io import load_json
from src.utils.constants import (
    COUNTRIES,
    DEVICES,
    LANGS,
    BASE_STEP_CONVERSION,
    FUNNEL_STAGES,
    RANDOM_SEED
)

random.seed(RANDOM_SEED)


def load_events():
    """
    Load seed events from disk.
    """

    return load_json("data/events.json")


def choose_segment():
    """
    Create realistic segment variation.
    """

    country = random.choices(
        COUNTRIES,
        weights=[0.25, 0.15, 0.25, 0.20, 0.15],
        k=1
    )[0]

    device = random.choices(
        DEVICES,
        weights=[0.45, 0.25, 0.30],
        k=1
    )[0]

    if country == "BR":
        lang = "pt-BR"
    elif country == "DE":
        lang = "de-DE"
    elif country == "IN":
        lang = "en-IN"
    else:
        lang = "en-US"

    return {
        "country": country,
        "device": device,
        "lang": lang
    }


def apply_friction_adjustments(
    step,
    segment,
    conversion_probability
):
    """
    Inject known friction patterns.
    """

    generated_errors = []

    country = segment["country"]
    device = segment["device"]
    lang = segment["lang"]

    # --------------------------------------------------
    # Pattern 1:
    # BR + Android + pt-BR signup friction
    # --------------------------------------------------

    if (
        step == "signup_form"
        and country == "BR"
        and device == "mobile_android"
        and lang == "pt-BR"
    ):
        conversion_probability *= 0.45

        generated_errors.append({
            "field": "phone",
            "code": "invalid_country_code"
        })

    # --------------------------------------------------
    # Pattern 2:
    # NG KYC upload friction
    # --------------------------------------------------

    if (
        step == "kyc_doc_upload"
        and country == "NG"
    ):
        conversion_probability *= 0.50

        generated_errors.append({
            "field": "document",
            "code": "document_format_unsupported"
        })

    # --------------------------------------------------
    # Pattern 3:
    # KYC review latency
    # --------------------------------------------------

    latency_multiplier = 1

    if step == "kyc_review":
        latency_multiplier = random.choice([1, 2, 3, 5])

        if latency_multiplier >= 4:
            conversion_probability *= 0.70

    return {
        "conversion_probability": conversion_probability,
        "generated_errors": generated_errors,
        "latency_multiplier": latency_multiplier
    }

def generate_synthetic_sessions(
    target_sessions=600
):
    """
    Generate synthetic onboarding sessions.
    """

    all_events = []

    base_time = datetime.utcnow()

    for session_index in range(target_sessions):

        segment = choose_segment()

        session_id = generate_session_id()

        user_id = generate_user_id()

        current_offset = random.randint(0, 5000)

        converted = True

        # --------------------------------------------------
        # Walk through funnel stages
        # --------------------------------------------------

        for step in FUNNEL_STAGES:

            # ----------------------------------------------
            # Entry event
            # ----------------------------------------------

            all_events.append({
                "session_id": session_id,
                "user_id_anon": user_id,
                "event": "page_view",
                "step": step,
                "ts": iso_timestamp(
                    base_time,
                    current_offset
                ),
                "country": segment["country"],
                "device": segment["device"],
                "lang": segment["lang"]
            })

            current_offset += random.randint(3, 15)

            # ----------------------------------------------
            # Conversion probability
            # ----------------------------------------------

            base_probability = BASE_STEP_CONVERSION[step]

            friction_result = apply_friction_adjustments(
                step=step,
                segment=segment,
                conversion_probability=base_probability
            )

            adjusted_probability = friction_result[
                "conversion_probability"
            ]

            # ----------------------------------------------
            # Generate errors
            # ----------------------------------------------

            for error in friction_result["generated_errors"]:

                all_events.append({
                    "session_id": session_id,
                    "user_id_anon": user_id,
                    "event": "form_validation_error",
                    "step": step,
                    "field": error["field"],
                    "code": error["code"],
                    "ts": iso_timestamp(
                        base_time,
                        current_offset
                    )
                })

                current_offset += random.randint(2, 8)

            # ----------------------------------------------
            # Simulate KYC latency
            # ----------------------------------------------

            latency_multiplier = friction_result[
                "latency_multiplier"
            ]

            current_offset += (
                random.randint(10, 40)
                * latency_multiplier
            )

            # ----------------------------------------------
            # Determine conversion
            # ----------------------------------------------

            did_convert = (
                random.random()
                <= adjusted_probability
            )

            # ----------------------------------------------
            # Exit condition
            # ----------------------------------------------

            if not did_convert:

                converted = False

                all_events.append({
                    "session_id": session_id,
                    "user_id_anon": user_id,
                    "event": "session_end",
                    "step": step,
                    "ts": iso_timestamp(
                        base_time,
                        current_offset
                    )
                })

                break

            # ----------------------------------------------
            # Successful progression event
            # ----------------------------------------------

            all_events.append({
                "session_id": session_id,
                "user_id_anon": user_id,
                "event": "step_completed",
                "step": step,
                "ts": iso_timestamp(
                    base_time,
                    current_offset
                )
            })

            current_offset += random.randint(5, 20)

        # --------------------------------------------------
        # Successful full funnel completion
        # --------------------------------------------------

        if converted:

            all_events.append({
                "session_id": session_id,
                "user_id_anon": user_id,
                "event": "conversion",
                "step": "first_trade",
                "ts": iso_timestamp(
                    base_time,
                    current_offset
                )
            })

    return all_events

def extend_dataset():

    seed_events = load_events()

    synthetic_events = generate_synthetic_sessions(
        target_sessions=600
    )

    combined_events = (
        seed_events
        + synthetic_events
    )

    combined_events = sorted(
        combined_events,
        key=lambda x: (
            x["session_id"],
            x["ts"]
        )
    )

    return combined_events