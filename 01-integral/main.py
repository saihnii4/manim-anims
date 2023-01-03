from manim import *
import numpy as np

_template = TexTemplate()
_template.add_to_preamble("""\\usepackage{cancel}""")


follow = lambda m1, m2: m1.match_coord(m2, (0,)).match_coord(m2, (1,))
align = lambda m1, m2: m1.shift(np.array(((m1.width - m2.width) / 2, 0, 0)))


def square(m):
    _sq = (
        MathTex("\\blacksquare", font_size=96, color=WHITE)
        .move_to(m, 3 * RIGHT)
        .shift(RIGHT)
    )
    return _sq.shift(np.array((0, (_sq.height - m.height) / 2, 0)))


class Integral(Scene):
    def construct(self):
        def _zip_steps(*steps: Mobject, hide_orig: bool = True):
            for a, b in zip(steps, steps[1:]):
                b = align(follow(b, a), a)

                yield (
                    FadeIn(b),
                    b.animate.shift(2 * DOWN),
                )

        _graph = Axes(x_range=[0, 1], y_range=[0, 0.4]).set(height=5, width=5)
        graph = _graph.plot(lambda x: np.log(x + 1) / (1 + x**2), x_range=[0, 1])
        area = _graph.get_area(graph, x_range=(0, 1))

        integrand_graph = VGroup(_graph, graph, area)
        self.play(Create(_graph), Write(graph), Create(area))
        self.pause()

        self.play(integrand_graph.animate.shift(np.array((0, -1, 0))))

        init = MathTex(
            """\\int_{0}^{1} \\frac{\\ln \\left(1+x\\right)}{1+x^2} dx""",
            font_size=64,
        ).shift(3 * UP)
        self.play(Create(init))
        self.play(
            init.animate.move_to((init.get_x() - 3, 10, 0)),
            integrand_graph.animate.shift(np.array((0, -config.frame_height, 0))),
        )

        u_sub = MathTex("""x = \\tan u""", font_size=64)
        self.pause()
        self.play(
            Write(u_sub), u_sub.animate.move_to((init.get_x() + 5, 10.5, 0)), run_time=1
        )

        implicit_diff = follow(MathTex("""dx = \\sec^2 u~du""", font_size=64), u_sub)
        self.play(Write(implicit_diff), implicit_diff.animate.shift(0.75 * DOWN))

        line_1 = follow(
            MathTex(
                """= \\int_{0}^{\\frac{\\pi}{4}} \\frac{\\ln \\left(1 + \\tan u\\right)}{1+\\left(\\tan u\\right)^2} \\sec^2 u~du"""
            ),
            init,
        )

        self.play(
            FadeIn(
                line_1,
            ),
            line_1.animate.shift(2 * DOWN),
        )

        self.pause()

        line_2 = follow(
            MathTex(
                """= \\int_{0}^{\\frac{\\pi}{4}} \\frac{\\ln \\left(1 + \\tan u\\right)}{\\sec^2 u} \\sec^2 u~du"""
            ),
            line_1,
        )

        self.play(ReplacementTransform(line_1, line_2))
        self.pause()

        line_2_cancellations = follow(
            MathTex(
                """= \\int_{0}^{\\frac{\\pi}{4}} \\frac{\\ln \\left(1 + \\tan u\\right)}{\\bcancel{\\sec^2 u}} \\bcancel{\\sec^2 u}~du""",
                tex_template=_template,
            ),
            line_2,
        )

        self.play(ReplacementTransform(line_2, line_2_cancellations), runtime=1.25)

        line_3 = MathTex(
            """= \\int_{0}^{\\frac{\\pi}{4}} \\ln \\left(1 + \\tan u\\right)~du"""
        )

        line_4 = MathTex(
            """= \\int_{0}^{\\frac{\\pi}{4}} \\ln \\left(\\frac{\\sin u + \\cos u}{\\cos u} \\right)~du"""
        )

        line_5 = MathTex(
            """= \\int_{0}^{\\frac{\\pi}{4}} \\ln\\left(\\sin u + \\cos u\\right) - \\ln \\cos u~du"""
        )

        line_6 = MathTex(
            """= \\int_{0}^{\\frac{\\pi}{4}} \\ln\\left(\\sqrt{2}\\cos\\left(u - \\frac{\\pi}{4}\\right)\\right) - \\ln\\cos u~du"""
        )

        line_7 = MathTex(
            """= \\int_{0}^{\\frac{\\pi}{4}} \\frac{1}{2} \\ln\\left(2\\right) + \\ln\\left(\\cos\\left(u - \\frac{\\pi}{4}\\right)\\right) - \\ln\\cos u~du"""
        )

        line_8 = (
            MathTex(
                """= \\frac{\\pi \\ln{2}}{8} + \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos \\left(u - \\frac{\\pi}{4}\\right)~du - \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos u~du"""
            )
            .match_coord(line_7, (0,))
            .match_coord(line_7, (1,))
        )

        line_8.shift(
            np.array(
                (
                    (line_8.width - line_7.width) / 2,
                    0,
                    0,
                )
            )
        )

        animations = _zip_steps(
            line_2_cancellations, line_3, line_4, line_5, line_6, line_7, line_8
        )
        for anim in animations:
            self.play(*filter(bool, anim))
            self.pause()

        line_9 = follow(
            MathTex(
                """= \\frac{\\pi \\ln{2}}{8} + \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos \\left(\\left(\\frac{\\pi}{4} - u\\right) - \\frac{\\pi}{4}\\right)~du - \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos u~du"""
            ),
            line_8,
        )

        align(line_9, line_8)

        self.play(ReplacementTransform(line_8, line_9), runtime=1.25)
        self.pause()

        line_9_cancel = follow(
            MathTex(
                """= \\frac{\\pi \\ln{2}}{8} + \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos \\left(\\left(\\bcancel{\\frac{\\pi}{4}} - u\\right) \\bcancel{- \\frac{\\pi}{4}}\\right)~du - \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos u~du""",
                tex_template=_template,
            ),
            line_9,
        )

        line_9_visual_cancel = follow(
            MathTex(
                """= \\frac{\\pi \\ln{2}}{8} + \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos \\left(-u\\right)~du - \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos u~du"""
            ),
            line_9_cancel,
        )
        line_9_cancel = align(line_9, line_9_cancel)
        self.play(TransformMatchingTex(line_9, line_9_cancel))
        self.pause()
        align(line_9_visual_cancel, line_9_cancel)
        self.play(TransformMatchingShapes(line_9_cancel, line_9_visual_cancel))
        self.pause()

        odd_func = follow(
            MathTex(
                """= \\frac{\\pi \\ln{2}}{8} + \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos \\left(u\\right)~du - \\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos u~du"""
            ),
            line_9_visual_cancel,
        )
        align(odd_func, line_9_visual_cancel)
        self.play(TransformMatchingShapes(line_9_visual_cancel, odd_func))
        self.pause()

        integrand_cancel = follow(
            MathTex(
                """= \\frac{\\pi \\ln{2}}{8} + \\bcancel{\\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos \\left(u\\right)~du} - \\bcancel{\\int_{0}^{\\frac{\\pi}{4}} \\ln\\cos u~du}""",
                tex_template=_template,
            ),
            line_9_visual_cancel,
        )

        align(integrand_cancel, odd_func)
        self.play(TransformMatchingShapes(odd_func, integrand_cancel))
        self.pause()

        integrand_visual_cancel = follow(
            MathTex(
                """= \\frac{\\pi \\ln{2}}{8}""",
            ),
            integrand_cancel,
        )

        align(integrand_visual_cancel, integrand_cancel)
        self.play(TransformMatchingShapes(integrand_cancel, integrand_visual_cancel))
        self.pause()

        final_result = follow(
            MathTex("""= \\frac{\\pi \\ln{2}}{8}""", font_size=96), integrand_cancel
        ).set_coord(-6, (1,))
        self.play(Transform(integrand_visual_cancel, final_result), run_time=2)
        self.pause()

        self.play(DrawBorderThenFill(square(final_result)))
