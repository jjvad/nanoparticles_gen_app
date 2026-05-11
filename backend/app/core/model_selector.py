FEATURES = ["NPs", "coresize", "surfcharge"]


def select_model_path(properties: dict) -> str:
    provided = sorted(properties.keys())

    n = len(provided)

    # все признаки
    if n == 3:
        return "/models/cvae_3"

    # два признака
    elif n == 2:
        missing = list(set(FEATURES) - set(provided))[0]
        return f"/models/cvae_2/{missing}"

    # один признак
    elif n == 1:
        feature = provided[0]
        return f"/models/cvae_1/{feature}"

    raise ValueError("Invalid number of properties")