from flask import Flask, render_template, redirect, Response

from config import Config
from project.forms import MainPageForm, RubiksCubeForm
from randomizer import generate_seed
from rubiks_cube_utils import get_cube, encode, to_web_view, decode

app = Flask(__name__)
app.config.from_object(Config())


@app.route("/", methods=["get", "post"])
def index() -> Response | str:
    form = MainPageForm()
    if form.validate_on_submit():
        size: int = int(form.size.data)
        seed: str = form.seed.data or generate_seed()

        log = lambda x: app.logger.debug("\n" + "\n".join("\t" + i for i in str(x).split("\n")))
        log("seed: " + str(seed))
        return redirect(f"/cube/{encode(get_cube(size, seed, log=log))}/")
    return render_template("index.html", form=form)


@app.route("/cube/<string:sides>/", methods=["get", "post"])
def cube(sides: str) -> Response | str:
    form = RubiksCubeForm()
    if form.validate_on_submit():
        ...
    return render_template("cube.html", form=form, cube=to_web_view(decode(sides)))


if __name__ == '__main__':
    app.run(debug=True)
