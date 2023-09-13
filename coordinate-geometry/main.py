from manim import *


class UnitCircle(Scene):
    def construct(self):
        # construct a coordinate system with the unit circle
        plane = NumberPlane()
        axes = Axes(
            x_length=None,
            y_length=None,
            axis_config={
                # "include_ticks": False,
                "include_tip": False,
                "unit_size": plane.get_x_unit_size(),
            },
        ).add_coordinates()
        circle = Circle(color=BLUE)
        circle.set_stroke(width=2)
        circle.set_fill(color=BLUE, opacity=0.2)

        _eq = MathTex("(x + (0.0))^2 + (y + (0.0))^2 = 1")
        _eq.to_corner(UR)
        bg_rect = BackgroundRectangle(_eq, color=BLACK, fill_opacity=1, buff=0.2)
        eq = VGroup(bg_rect, _eq)

        center = Dot(circle.get_center_of_mass())
        center_label = Text("(0.0, 0.0)", font_size=24, color=ORANGE).next_to(
            center, DR
        )
        circle_g = VGroup(center, circle)

        self.play(Create(plane), run_time=2)
        self.play(Create(axes), run_time=2)
        self.wait(1)
        self.play(Write(eq), run_time=1)
        self.wait(1)
        axes.add(circle_g)
        self.play(Create(circle_g), run_time=3)
        self.wait(2)
        self.play(Write(center_label), run_time=3)
        self.wait(0.5)
        center_label.add_updater(
            lambda m: m.become(
                Text(
                    f"({circle_g[0].get_center()[0]:.1f}, {circle_g[0].get_center()[1]:.1f})",
                    font_size=24,
                    color=ORANGE,
                ).next_to(circle_g[0], DR)
            )
        )

        def _eq_updater(m: VGroup):
            bg = m.submobjects[0]
            eq = m.submobjects[1]

            eq.become(
                MathTex(
                    f"(x + ({-circle_g[0].get_center()[0]:.1f}))^2 + (y + ({-circle_g[0].get_center()[1]:.1f}))^2 = 1"
                ).to_corner(UR)
            )

            bg.become(BackgroundRectangle(eq, color=BLACK, fill_opacity=1, buff=0.2))

        eq.add_updater(_eq_updater)

        self.play(circle_g.animate.move_to(axes.coords_to_point(2, 2)))
        self.wait(1)

        self.play(circle_g.animate.move_to(axes.coords_to_point(-1, 3)))
        self.wait(1)

        self.play(circle_g.animate.move_to(axes.coords_to_point(-2, -2)))
        self.wait(1)

        self.play(circle_g.animate.move_to(axes.coords_to_point(2, -3)))
        self.wait(1)

        self.play(circle_g.animate.move_to(axes.coords_to_point(0, 0)))
        self.wait(1)

        graph = axes.plot(lambda x: x, color=BLUE)
        self.play(Write(graph), run_time=3)
        self.wait(2)
        p1 = Point(
            axes.coords_to_point(-1 / np.sqrt(2), -1 / np.sqrt(2)),
            color=WHITE,
            stroke_width=6,
        )
        p2 = Point(
            axes.coords_to_point(1 / np.sqrt(2), 1 / np.sqrt(2)),
            color=WHITE,
            stroke_width=6,
        )
        self.play(FadeIn(p1, p2), run_time=2)
        self.wait(2)

        self.play(FadeOut(p1, p2))
        self.play(circle_g.animate.move_to(axes.coords_to_point(1, 1)))
        p1 = Point(
            axes.coords_to_point(1 + 1 / np.sqrt(2), 1 + 1 / np.sqrt(2)),
            color=WHITE,
            stroke_width=6,
        )
        p2 = Point(
            axes.coords_to_point(1 - 1 / np.sqrt(2), 1 - 1 / np.sqrt(2)),
            color=WHITE,
            stroke_width=6,
        )
        self.play(FadeIn(p1, p2))
        self.wait(2)
    
        self.play(FadeOut(p1, p2))
        p1 = Point(axes.coords_to_point(0, 0), color=WHITE, stroke_width=6)
        self.play(FadeIn(p1))
        self.play(
            circle_g.animate.move_to(
                axes.coords_to_point(1 / np.sqrt(2), -1 / np.sqrt(2))
            )
        )
        self.wait(2)
        self.remove(p1, p2, _eq, graph, circle_g, _eq, bg_rect, plane)