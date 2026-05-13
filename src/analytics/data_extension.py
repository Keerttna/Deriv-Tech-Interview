import random
from datetime import datetime

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