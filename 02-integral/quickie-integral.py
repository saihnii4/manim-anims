# TODO: highlight transformational elements

from manim import *

_template = TexTemplate()
_template.add_to_preamble("""\\usepackage{cancel}""")


follow = lambda m1, m2: m1.match_coord(m2, (0,)).match_coord(m2, (1,))

class QwikIntegral(Scene):
    font_size = 52 # consistency is key

    def construct(self):
        integrand = MathTex("""\\int_{0}^{1} \\frac{\\arcsin\\left(\\frac{2x}{1+x^2}\\right)}{1+x^2}dx""", font_size=self.font_size)

        u_sub = follow(MathTex("""x = \\tan{u}""", font_size=56), integrand)
        imp_diff = MathTex("""dx = \\sec^2{u}~du""")
        applied = MathTex("""\\int_{0}^{\\frac{\\pi}{4}} \\frac{\\arcsin\\left(\\frac{2\\tan u}{1 + \\tan^2u}\\right)}{1+\\tan^2u} \\cdot \\sec^2{u}~du""")
        applied_m1 = MathTex("""\\int_{0}^{\\frac{\\pi}{4}} \\frac{\\arcsin\\left(\\frac{2\\tan u}{\\sec^2{u}}\\right)}{\\sec^2{u}} \\cdot \\sec^2{u}~du""")
        applied_c1 = MathTex("""\\int_{0}^{\\frac{\\pi}{4}} \\frac{\\arcsin\\left(2\\sin{u}\\cos{u}\\right)}{\\bcancel{\\sec^2{u}}} \\cdot \\bcancel{\\sec^2{u}}~du""", tex_template=_template)

        applied_m2 = MathTex("""\\int_{0}^{\\frac{\\pi}{4}}\\arcsin{\\left(2\\sin{u}\\cos{u}\\right)}~du""")
        applied_m3 = MathTex("""\\int_{0}^{\\frac{\\pi}{4}}\\arcsin{\\left(\\sin{2u}\\right)}~du""")
        applied_m4 = MathTex("""\\int_{0}^{\\frac{\\pi}{4}}2u~du""")
        applied_m5 = MathTex("""u^2 \Big|_{0}^{\\frac{\\pi}{4}}""")
        expanded_bounds = MathTex("""\\left(\\frac{\\pi}{4}\\right)^2 - 0^2""")
        answer = MathTex("""\\frac{\\pi^2}{16}""")
    
        self.play(Write(integrand), run_time=1)
    
        _n = 2.1 # _n is used whenever symmetry is needed
        self.play(integrand.animate.shift(LEFT*_n), Write(u_sub), u_sub.animate.shift(RIGHT*_n), run_time=0.5)

        _n = 0.4
        imp_diff = follow(imp_diff, u_sub)
        self.play(Write(imp_diff), imp_diff.animate.shift(DOWN*_n), u_sub.animate.shift(UP*_n), run_time=0.4)

        self.play(Unwrite(imp_diff), Unwrite(u_sub), ReplacementTransform(integrand, applied), run_time=0.5)

        remaining = [applied, applied_m1, applied_c1, applied_m2, applied_m3, applied_m4, applied_m5, expanded_bounds, answer]

        for (curr, next) in zip(remaining, remaining[1:]):
            self.play(ReplacementTransform(curr, next), run_time=0.65)