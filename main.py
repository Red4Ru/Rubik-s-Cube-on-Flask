import typing

from flask import Flask, render_template, redirect, Response

from config import Config
from project.forms import MainPageForm, RubiksCubeForm
from randomizer import generate_seed
from rubiks_cube.axis import Axis
from rubiks_cube.rubiks_cube import RubiksCube
from rubiks_cube_utils import get_cube, encode, decode

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
        log("seed: " + str(seed))
        return redirect(f"/cube/{encode(get_cube(size, seed, log=log))}/")
    return render_template("index.html", form=form)


@app.route("/cube/<string:sides>/", methods=["get", "post"])
def cube(sides: str) -> Response | str:
    cube: RubiksCube = decode(sides)
    form: RubiksCubeForm = RubiksCubeForm(cube.get_size())
    if form.validate_on_submit():
        sequence: str = form.sequence.data
        rotate_description: str = form.rotate.data
        if rotate_description != "-":
            from_down: bool = rotate_description.startswith("from down")
            left: bool = bool(rotate_description.count("left"))
            cube.rotate_cube(Axis.Z if left else Axis.X, 1 if (from_down ^ left) else -1)
        cube.apply_sequence(sequence)
        return redirect(f"/cube/{encode(cube)}/")
    html_cube: str = render_template("cube_scene.html", sides=cube.get_sides())
    return render_template("cube.html", form=form, cube=html_cube)


if __name__ == '__main__':
    app.run(debug=True)
