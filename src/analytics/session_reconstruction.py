from collections import defaultdict
from datetime import datetime


def reconstruct_sessions(events):

    grouped = defaultdict(list)

    # --------------------------------------------------
    # Group by session
    # --------------------------------------------------

    for event in events:

        grouped[
            event["session_id"]
        ].append(event)

    reconstructed = []

    # --------------------------------------------------
    # Build compact session objects
    # --------------------------------------------------

    for session_id, session_events in grouped.items():

        session_events = sorted(
            session_events,
            key=lambda x: x["ts"]
        )

        first_event = session_events[0]

        steps_reached = []

        errors = []

        durations = {}

        converted = False

        previous_ts = None
        previous_step = None

        # ----------------------------------------------
        # Iterate through ordered events
        # ----------------------------------------------

        for event in session_events:

            step = event.get("step")

            ts = datetime.strptime(
                event["ts"],
                "%Y-%m-%dT%H:%M:%SZ"
            )

            # ------------------------------------------
            # Track steps
            # ------------------------------------------

            if (
                step
                and step not in steps_reached
            ):
                steps_reached.append(step)

            # ------------------------------------------
            # Track validation errors
            # ------------------------------------------

            if (
                event["event"]
                == "form_validation_error"
            ):

                errors.append({
                    "step": step,
                    "field": event.get("field"),
                    "code": event.get("code")
                })

            # ------------------------------------------
            # Step duration calculation
            # ------------------------------------------

            if previous_ts and previous_step:

                delta = (
                    ts - previous_ts
                ).total_seconds()

                durations[
                    previous_step
                ] = round(delta, 2)

            previous_ts = ts
            previous_step = step

            # ------------------------------------------
            # Conversion detection
            # ------------------------------------------

            if (
                event["event"]
                == "conversion"
            ):
                converted = True

        reconstructed.append({
            "session_id": session_id,
            "user_id_anon": first_event.get(
                "user_id_anon"
            ),
            "country": first_event.get(
                "country"
            ),
            "device": first_event.get(
                "device"
            ),
            "lang": first_event.get(
                "lang"
            ),
            "steps_reached": steps_reached,
            "validation_errors": errors,
            "durations": durations,
            "final_step": (
                steps_reached[-1]
                if steps_reached
                else None
            ),
            "converted_to_first_trade": converted
        })

    return reconstructed