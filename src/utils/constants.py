FUNNEL_STAGES = [
    "landing",
    "signup_form",
    "email_verify",
    "kyc_doc_upload",
    "kyc_review",
    "first_deposit",
    "first_trade"
]

COUNTRIES = [
    "BR",
    "NG",
    "US",
    "IN",
    "DE"
]

DEVICES = [
    "mobile_android",
    "mobile_ios",
    "desktop"
]

LANGS = [
    "pt-BR",
    "en-US",
    "en-IN",
    "de-DE"
]

BASE_STEP_CONVERSION = {
    "landing": 0.85,
    "signup_form": 0.70,
    "email_verify": 0.80,
    "kyc_doc_upload": 0.65,
    "kyc_review": 0.75,
    "first_deposit": 0.60,
    "first_trade": 0.55
}

TARGET_SESSIONS = 600

TARGET_EVENTS = 5000

RANDOM_SEED = 42