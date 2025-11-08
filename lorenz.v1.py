import arcade
import numpy as np
from scipy.integrate import solve_ivp

# Window settings
WIDTH, HEIGHT = 800, 600
TITLE = "Lorenz Attractor - Fading Trail"

# Lorenz system parameters
sigma, rho, beta = 10, 28, 8/5

def lorenz(t, state):
    x, y, z = state
    return [sigma*(y-x), x*(rho-z)-y, x*y-beta*z]

# Solve Lorenz system
t_span = (0, 100)
t_slots = np.linspace(*t_span, 10000)
sol = solve_ivp(lorenz, t_span, [1,1,1], t_eval=t_slots)

# Scale to window
x_vals = (sol.y[0] - sol.y[0].min()) / (sol.y[0].max() - sol.y[0].min()) * WIDTH
z_vals = (sol.y[2] - sol.y[2].min()) / (sol.y[2].max() - sol.y[2].min()) * HEIGHT
points = list(zip(x_vals, z_vals))

class LorenzFadingTrail(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.index = 1
        self.trail_length = 800  # number of segments to show

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "The Lorenz Attractor in 2D", 
            WIDTH//2,
            HEIGHT - 30, 
            color=(255, 255, 255, 180),
            font_size=18,
            font_name="Garamond",                   # or any system font you like
            anchor_x="center",                   # horizontal centering
            )

        start = max(0, self.index - self.trail_length)

        # Draw fading trail
        for i in range(start, self.index):
            x1, y1 = points[i]
            x2, y2 = points[i+1]

            # Fade factor: older segments are dimmer
            t = (i - start) / self.trail_length  # 0 = tail, 1 = head
                     # tail dim, head bright

            arcade.draw_line(x1, y1, x2, y2, (int(0*t), int(204*t), int(204*t)), 1.5)

        # Draw the current point as a white ball
        x, y = points[self.index]
        arcade.draw_circle_filled(x, y, 3, arcade.color.BLIZZARD_BLUE)

    def on_update(self, delta_time):
        self.index += 1
        if self.index >= len(points)-1:
            self.index = 1  # loop back to start

if __name__ == "__main__":
    LorenzFadingTrail()
    arcade.run()
