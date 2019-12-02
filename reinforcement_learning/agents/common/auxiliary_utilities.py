# BEGIN--------------------PROJECT-ROOT-PATH-APPENDING-------------------------#
import sys, os
REL_PROJECT_ROOT_PATH = "./../../../"
ABS_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
ABS_PROJECT_ROOT_PATH = os.path.normpath(os.path.join(ABS_FILE_DIR, REL_PROJECT_ROOT_PATH))
sys.path.append(ABS_PROJECT_ROOT_PATH)
# -------------------------PROJECT-ROOT-PATH-APPENDING----------------------END#


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