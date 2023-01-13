from manim import *
import numpy as np

class Limit(Scene):
    f_x = lambda x: (x**2*np.sin(1/x))/((1+x)**(1/x) - np.e)

    def construct(self):
        limit = MathTex("""\\lim_{x \\to 0} \\frac{x^2\\sin{\\frac{1}{x}} + x}{\\sqrt[x]{1+x} - e}""")
        quotient_rule = MathTex("""\\frac{\\left(\\lim_{x \\to 0} x \\left(x\\sin{\\frac{1}{x}} + 1\\right)\\right)}{\\lim_{x \\to 0} \\sqrt[x]{1+x} - e}""")
        self.play(Write(limit))

        self.play(ReplacementTransform(limit, quotient_rule))