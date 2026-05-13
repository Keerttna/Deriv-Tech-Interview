from statsmodels.stats.power import (
    NormalIndPower
)

from statsmodels.stats.proportion import (
    proportion_effectsize
)


def compute_sample_size(
    baseline_rate,
    minimum_detectable_effect,
    power=0.8,
    alpha=0.05
):

    treatment_rate = (
        baseline_rate
        + minimum_detectable_effect
    )

    effect_size = (
        proportion_effectsize(
            baseline_rate,
            treatment_rate
        )
    )

    analysis = (
        NormalIndPower()
    )

    sample_size = analysis.solve_power(
        effect_size=effect_size,
        power=power,
        alpha=alpha,
        ratio=1.0,
        alternative="two-sided"
    )

    return int(
        round(sample_size)
    )