from flask import Flask, render_template, redirect

from config import Config
from project.forms import MainPageForm
from randomizer import generate_seed

app = Flask(__name__)
app.config.from_object(Config())


@app.route("/", methods=["get", "post"])
def index():
    form = MainPageForm()
    if form.validate_on_submit():
        seed: str = form.seed.data or generate_seed()
        print("seed:", seed)
        return redirect("/")
    return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
