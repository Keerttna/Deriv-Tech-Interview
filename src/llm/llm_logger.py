import hashlib
import json
from datetime import datetime


def log_llm_call(
    stage,
    input_artifacts,
    output_artifact,
    hypothesis_id=None,
    provider="mock_llm",
    model="deterministic-gpt-sim"
):

    payload = {

        "stage":
            stage,

        "hypothesis_id":
            hypothesis_id,

        "timestamp":
            datetime.utcnow().isoformat(),

        "provider":
            provider,

        "model":
            model,

        "prompt_hash":
            hashlib.md5(
                (
                    stage
                    + output_artifact
                ).encode()
            ).hexdigest(),

        "input_artifacts":
            input_artifacts,

        "output_artifact":
            output_artifact
    }

    with open(
        "outputs/llm_calls.jsonl",
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(payload)
            + "\n"
        )