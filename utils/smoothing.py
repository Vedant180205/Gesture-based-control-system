# utils/smoothing.py

class SmoothFilter:
    def __init__(self, alpha=0.5):
        self.alpha = alpha
        self.prev_x = None
        self.prev_y = None

    def apply(self, x, y):
        if self.prev_x is None:
            self.prev_x = x
            self.prev_y = y
            return x, y

        dx = x - self.prev_x
        dy = y - self.prev_y

        # DEAD ZONE (key fix)
        if abs(dx) < 5 and abs(dy) < 5:
            return self.prev_x, self.prev_y

        distance = abs(dx) + abs(dy)

        if distance > 50:
            alpha = 0.8
        else:
            alpha = self.alpha

        smooth_x = int(alpha * x + (1 - alpha) * self.prev_x)
        smooth_y = int(alpha * y + (1 - alpha) * self.prev_y)

        self.prev_x = smooth_x
        self.prev_y = smooth_y

        return smooth_x, smooth_y