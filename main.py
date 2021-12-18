from flask import Flask, render_template, session
from random import choice, shuffle
from flask_session import Session
import app_config
from os import remove, listdir

app = Flask(__name__, template_folder='./templates', static_folder='./static')
app.config.from_object(app_config)
Session(app)

imposters = app_config.IMPOSTER_MAX
good = app_config.GOOD_MAX
base_tasks = list(range(1, app_config.NUM_OF_TASKS + 1))
base_data = {}


@app.route("/", methods=['GET'])
def index():
    global imposters, good, base_tasks

    if "role" in session:
        return render_template('index.html', role=session["role"], tasks=session["tasks"])

    tasks = []
    for _ in range(7):
        task = choice(base_tasks)
        base_tasks.pop(base_tasks.index(task))
        tasks.append(task)
    base_tasks = list(range(1, app_config.NUM_OF_TASKS + 1))
    if imposters <= 0 and good <= 0:
        isGood = True
    elif imposters > 0 and good > 0:
        var = [True] * good + [False] * imposters
        shuffle(var)
        isGood = choice(var)
    else:
        isGood = (imposters <= 0)

    session["role"] = app_config.GOOD_NAME if isGood else app_config.IMPOSTER_NAME
    session["tasks"] = tasks

    if isGood:
        good -= 1
        return render_template('index.html', role=app_config.GOOD_NAME, tasks=list(map(str, tasks)))
    imposters -= 1
    return render_template('index.html', role=app_config.IMPOSTER_NAME, tasks=list(map(str, tasks)))


@app.route("/restartHiTech2021L", methods=['POST'])
def reboot():
    global imposters, good, base_tasks
    imposters = app_config.IMPOSTER_MAX
    good = app_config.GOOD_MAX
    base_tasks = list(range(1, app_config.NUM_OF_TASKS + 1))
    for key in list(session.keys()):
        session.pop(key)
    for f in listdir("./flask_session"):
        remove("./flask_session/" + f)
    return "Reboot"


@app.route("/GetInfoHiTech2021L", methods=['GET'])
def get_info():
    return {"imposter": imposters, "good": good}


if __name__ == "__main__":
    app.run("127.0.0.1", 8000)
