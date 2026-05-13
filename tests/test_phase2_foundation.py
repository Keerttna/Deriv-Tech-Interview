from pprint import pprint

from src.analytics.data_extension import (
    choose_segment,
    apply_friction_adjustments
)


def run_test():

    print("\n=== SEGMENT GENERATION TEST ===\n")

    for _ in range(5):
        pprint(choose_segment())

    print("\n=== BR FRICTION TEST ===\n")

    segment = {
        "country": "BR",
        "device": "mobile_android",
        "lang": "pt-BR"
    }

    result = apply_friction_adjustments(
        step="signup_form",
        segment=segment,
        conversion_probability=0.70
    )

    pprint(result)

    print("\n=== NG KYC TEST ===\n")

    segment = {
        "country": "NG",
        "device": "desktop",
        "lang": "en-US"
    }

    result = apply_friction_adjustments(
        step="kyc_doc_upload",
        segment=segment,
        conversion_probability=0.65
    )

    pprint(result)

    print("\n=== KYC REVIEW LATENCY TEST ===\n")

    segment = {
        "country": "US",
        "device": "desktop",
        "lang": "en-US"
    }

    for _ in range(5):

        result = apply_friction_adjustments(
            step="kyc_review",
            segment=segment,
            conversion_probability=0.75
        )

        pprint(result)


if __name__ == "__main__":
    run_test()