import typing

from flask import Flask, render_template, redirect, Response, flash, request

from config import Config
from project.forms import MainPageForm, RubiksCubeForm
from randomizer import generate_seed
from rubiks_cube.axis import Axis
from rubiks_cube.rubiks_cube import RubiksCube
from rubiks_cube_utils import get_cube, encode, decode, check_cube_is_solved, rotate_choices

app = Flask(__name__)
app.config.from_object(Config())


@app.route("/", methods=["get", "post"])
def index() -> Response | str:
    form: MainPageForm = MainPageForm()
    if form.validate_on_submit():
        size: int = int(form.size.data)
        seed: str = form.seed.data or generate_seed()

        log: typing.Callable[[str], None] = lambda x: app.logger.debug(
            "\n" + "\n".join("\t" + i for i in str(x).split("\n"))
        )
        log(f"Seed: {seed}")
        flash(f"Seed: {seed}")
        return redirect(f"/cube/{encode(get_cube(size, seed, log=log))}/")
    return render_template("index.html", form=form)


@app.route("/cube/<string:sides>/", methods=["get", "post"])
def cube(sides: str) -> Response | str:
    if RubiksCubeForm().to_menu.name in request.form:
        return redirect("/")

    cube: RubiksCube = decode(sides)
    form: RubiksCubeForm = RubiksCubeForm(cube.get_size())
    if form.validate_on_submit():
        sequence: str = form.sequence.data
        cube.apply_sequence(sequence)

        rotate_description: str = form.rotate.data
        rotate_choice_index: int = rotate_choices.index(rotate_description) - 1
        if rotate_choice_index != -1:
            cube.rotate_cube((Axis.X, Axis.Y, Axis.Z)[rotate_choice_index // 3], (1, -1, 2)[rotate_choice_index % 3])

        return redirect(f"/cube/{encode(cube)}/")
    return render_template("cube.html", form=form, cube=cube)


@app.template_filter("is_solved")
def check_cube_filter(cube: RubiksCube):
    return check_cube_is_solved(cube)


if __name__ == '__main__':
    app.run(debug=True)
