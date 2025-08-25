import plotlygrapher
import json
import ast
from flask import Flask, render_template, request
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    step = 1
    returnablectimes = None
    n_points = None
    error = None
    cstime = None
    cetime = None
    if request.method == "POST":
        if request.form["step"] != "2":
            cstime = request.form["cstime"]
            cetime = request.form["cetime"]
            start = datetime.strptime(cstime, "%Y-%m-%dT%H:%M")
            end = datetime.strptime(cetime, "%Y-%m-%dT%H:%M")
            start = start.replace(second=0, microsecond=0)
            if end.second > 0 or end.microsecond > 0:
                end = end.replace(second=0, microsecond=0) + timedelta(minutes=1)
            ctimes = []
            t = start
            while t <= end:
                ctimes.append(t)
                t += timedelta(minutes=1)
            n_points = len(ctimes)
            step = 2
            returnablectimes = json.dumps([actime.strftime("%Y-%m-%d %I:%M:%S %p") for actime in ctimes])

        else:
            cstime = request.form["cstime"]
            cetime = request.form["cetime"]
            n_points = int(request.form["n_points"])
            ctimes_str = request.form["ctimes"]
            ctimes = ast.literal_eval(ctimes_str)
            ctimes = [datetime.strptime(atime, "%Y-%m-%d %I:%M:%S %p") for atime in ctimes]
            returnablectimes = json.dumps([actime.strftime("%Y-%m-%d %I:%M:%S %p") for actime in ctimes])

            cxc = [float(x.strip()) for x in request.form["cxc"].split(",")]
            cyc = [float(y.strip()) for y in request.form["cyc"].split(",")]
            czc = [float(z.strip()) for z in request.form["czc"].split(",")]
            name = request.form["name"]
            showiss = request.form.get("showiss") == "on"

            if not (len(cxc) == len(cyc) == len(czc) == n_points):
                error = f"You must enter exactly {n_points} values for each coordinate."
                step = 2
            else:
                plotlygrapher.genfig()
                plotlygrapher.gentrajectory(cxc, cyc, czc, ctimes, name, showiss)
                plotlygrapher.stars(42, 150, 15000)
                plotlygrapher.showorbit()
                step = 3
    return render_template("main.html", step=step, n_points=n_points, error=error, cstime=cstime, cetime=cetime, ctimes=returnablectimes)

if __name__ == "__main__":
    app.run(debug=True)