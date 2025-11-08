import arcade
import numpy as np
from scipy.integrate import solve_ivp

#arbitrary
WIDTH, HEIGHT = 800, 600
TITLE = "Lorenz Attractor"

# Lorenz  parameters
sigma, rho, beta = 10, 28, 8/5

def lorenz(t, state):
    x, y, z = state #coordinates
    return [sigma*(y-x), x*(rho-z)-y, x*y-beta*z] #dx, dy and dz as per the differential equations

# Solving Lorenz system using integrals
t_span = (0, 100) #arbitrary
t_slots = np.linspace(*t_span, 10000) #divides into a list of 10,000 points between 0 and 100 (inclusive)
sol = solve_ivp(lorenz, t_span, [1,1,1], t_eval=t_slots) #solves the equation per above interval/point 

#Scaling the curve (maximum and minimum to the window
x_vals = (sol.y[0] - sol.y[0].min()) / (sol.y[0].max() - sol.y[0].min()) * WIDTH 
z_vals = (sol.y[2] - sol.y[2].min()) / (sol.y[2].max() - sol.y[2].min()) * HEIGHT
points = list(zip(x_vals, z_vals)) #extracts as list of tuples corresponding (x,z), i.e., [(x1, z1), (x2, z), (x3, z3),...,(x10,000, z10,000)]

class LorenzTrail(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE) #creating window/background 
        arcade.set_background_color(arcade.color.BLACK)
        self.index = 1 #counting in list points
        self.trail_length = 800  # number of segments (line connecting 2 points (xn, zn) and (xn+1, zn+1))to show as it fades

    def on_draw(self):
        self.clear()

        #title as shwn within page
        arcade.draw_text(
            "Lorenz Attractor in X-Z", 
            WIDTH//2,
            HEIGHT - 30, 
            color=(255, 255, 255),
            font_size=14,
            font_name="Garamond",
            anchor_x="center" # horizontal centring
            )

        #if the index is less than the trail length, all segments are drawn. If it exceeds, then only 800 (trail length) are drawn. 
        if self.index<self.trail_length:
            start=0
        else:
            start=self.index-self.trail_length #drawing of the trail (not the latest point, rather, the oldest point) starts at this point. 

        #NOT NECESSARY TO THE CONCEPT
        #Draw fading trail
        for i in range(start, self.index): #traverses each point to be drawn in the trail, from starting point (the last-to-be-faded point to the self.index point (latest point)
            x1, y1 = points[i] 
            x2, y2 = points[i+1]

            #Fade factor
            t=(i-start)/self.trail_length #tail dim, head bright

            #drawing every individual line segment. 
            arcade.draw_line(x1, y1, x2, y2, (int(0*t), int(204*t), int(204*t)), 1.5) #NOTE ON COLOUR: each of (r, g, b) is being faded depending on t, which depends on i. 

        #drawing the moving point as a ball/circle. 
        x, y = points[self.index]
        arcade.draw_circle_filled(x, y, 3, arcade.color.WHITE)

    def on_update(self, delta_time):
        self.index += 1
        if self.index >= len(points)-1:
            self.index = 1  #loops to the beginning. 

LorenzTrail()
arcade.run()







