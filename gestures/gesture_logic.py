import math


def distance(p1, p2):
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def is_finger_extended(hand, tip_id, pip_id):
    """Tip farther from wrist than PIP knuckle → finger is extended."""
    wrist = hand[0][1:]
    tip   = hand[tip_id][1:]
    pip   = hand[pip_id][1:]
    return distance(tip, wrist) > distance(pip, wrist)


def detect_gesture(hand):
    """
    OPEN        — all 4 fingers (index/middle/ring/pinky) extended
    TWO_FINGERS — index + middle extended (ring/pinky state ignored)
                  BUT not OPEN (not all 4 extended)
    FIST        — 0 fingers extended
    None        — anything else (transitional)
    """
    finger_pairs = [(8, 6), (12, 10), (16, 14), (20, 18)]
    extended = [is_finger_extended(hand, t, p) for t, p in finger_pairs]

    index_ext, middle_ext, ring_ext, pinky_ext = extended
    count = sum(extended)

    # OPEN: all 4 clearly spread
    if count >= 4:
        return "OPEN"

    # FIST: all 4 curled
    if count == 0:
        return "FIST"

    # TWO_FINGERS: index + middle up (ring/pinky can be anything, but we're not OPEN)
    if index_ext and middle_ext:
        return "TWO_FINGERS"

    return None