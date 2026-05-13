import random

from src.utils.constants import (
    RANDOM_SEED
)

random.seed(RANDOM_SEED)

def build_trace(
    session
):
    """
    Build compact anonymized
    session trace representation.
    """

    return {

        "session_id":
            session["session_id"],

        "segment": {

            "country":
                session["country"],

            "device":
                session["device"],

            "lang":
                session["lang"]
        },

        "ordered_steps":
            session[
                "steps_reached"
            ],

        "validation_errors":
            session[
                "validation_errors"
            ],

        "durations":
            session[
                "durations"
            ],

        "final_step":
            session[
                "final_step"
            ],

        "converted_to_first_trade":
            session[
                "converted_to_first_trade"
            ]
    }

def has_known_friction(
    session
):
    """
    Detect sessions with
    meaningful friction patterns.
    """

    errors = session.get(
        "validation_errors",
        []
    )

    error_codes = [
        e["code"]
        for e in errors
    ]

    known_patterns = [
        "invalid_country_code",
        "document_format_unsupported"
    ]

    return any(
        code in known_patterns
        for code in error_codes
    )

def is_successful_conversion(
    session
):

    return session.get(
        "converted_to_first_trade",
        False
    )

def sample_representative_traces(
    sessions,
    sample_size=50
):
    """
    Deterministically sample
    representative onboarding traces.
    """

    # --------------------------------------------------
    # Separate trace categories
    # --------------------------------------------------

    friction_sessions = [
        s for s in sessions
        if has_known_friction(s)
    ]

    successful_sessions = [
        s for s in sessions
        if is_successful_conversion(s)
    ]

    failed_sessions = [
        s for s in sessions
        if not is_successful_conversion(s)
    ]

    # --------------------------------------------------
    # Deterministic shuffling
    # --------------------------------------------------

    random.shuffle(
        friction_sessions
    )

    random.shuffle(
        successful_sessions
    )

    random.shuffle(
        failed_sessions
    )

    # --------------------------------------------------
    # Balanced representative allocation
    # --------------------------------------------------

    selected = []

    # High-friction examples
    selected.extend(
        friction_sessions[:20]
    )

    # Successful journeys
    selected.extend(
        successful_sessions[:15]
    )

    # Failed journeys
    selected.extend(
        failed_sessions[:15]
    )

    # --------------------------------------------------
    # Deduplicate by session_id
    # --------------------------------------------------

    unique = {}

    for session in selected:

        unique[
            session["session_id"]
        ] = session

    sampled = list(
        unique.values()
    )

    # --------------------------------------------------
    # Enforce sample size
    # --------------------------------------------------

    sampled = sampled[
        :sample_size
    ]

    # --------------------------------------------------
    # Convert to compact traces
    # --------------------------------------------------

    traces = [
        build_trace(s)
        for s in sampled
    ]

    return traces

def summarize_trace_diversity(
    traces
):
    """
    Compute diversity summary
    for verification.
    """

    countries = set()
    devices = set()
    langs = set()

    for trace in traces:

        segment = trace["segment"]

        countries.add(
            segment["country"]
        )

        devices.add(
            segment["device"]
        )

        langs.add(
            segment["lang"]
        )

    return {

        "countries":
            sorted(
                list(countries)
            ),

        "devices":
            sorted(
                list(devices)
            ),

        "languages":
            sorted(
                list(langs)
            )
    }