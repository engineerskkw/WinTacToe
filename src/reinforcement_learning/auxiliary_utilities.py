def linear_map(value, low, high, values):
    original_high = max(values)
    original_low = min(values)
    if original_high == original_low:
        return high
    original_midpoint = (original_high + original_low) / 2
    original_halfrange = original_midpoint - original_low
    value = (value - original_midpoint) / original_halfrange

    midpoint = (high + low) / 2
    halfrange = midpoint - low
    value = midpoint + value * halfrange
    return value