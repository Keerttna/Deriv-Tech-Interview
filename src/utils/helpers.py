import random
import uuid
from datetime import datetime, timedelta

from src.utils.constants import RANDOM_SEED

random.seed(RANDOM_SEED)


def generate_session_id():
    return f"ss_{uuid.uuid4().hex[:8]}"


def generate_user_id():
    return f"u_{uuid.uuid4().hex[:8]}"


def iso_timestamp(base_time, offset_seconds):
    """
    Create ISO timestamp with offset.
    """

    ts = base_time + timedelta(seconds=offset_seconds)

    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def weighted_choice(values, weights):
    """
    Deterministic weighted random selection.
    """

    return random.choices(values, weights=weights, k=1)[0]