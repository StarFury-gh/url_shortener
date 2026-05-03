from core.utils import constants


async def generate_new_slug(length: int = 8, prev_slug: str | None = None):
    if prev_slug is None:
        return constants.ALLOWED_SYMBOLS[0] * length

    if prev_slug is not None and len(prev_slug) != length:
        raise ValueError(f"Different lengths given: {length=} {len(prev_slug)=}")

    result = prev_slug

    for i in range(length - 1, -1, -1):
        if result[i] != constants.ALLOWED_SYMBOLS[-1]:
            new_idx = constants.ALLOWED_SYMBOLS.index(result[i]) + 1
            result = result[:i] + constants.ALLOWED_SYMBOLS[new_idx] + result[i + 1 :]
            break

        else:
            result = result[:i] + constants.ALLOWED_SYMBOLS[0] + result[i + 1 :]
            continue

    return result
