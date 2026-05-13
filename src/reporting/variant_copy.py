def generate_variant_copy(
    top_experiment
):

    return f"""
# Experiment Variant Copy

## Target Segment

{top_experiment['target_segment']}

## Control

Current onboarding form experience.

## Treatment

Localized validation messaging and
improved formatting guidance.

## Rationale

Reduce friction and improve successful
form completion.

## HTML Snippet

```html
<label>
Phone Number
</label>

<input
  type="tel"
  placeholder="+55 11 91234-5678"
/>

<p class="helper-text">
Use your local country code format.
</p>

"""
