from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET","POST"])

def home():

    prediction=None
    equation=None

    if request.method=="POST":

        file=request.files["file"]

        filepath=os.path.join(app.config["UPLOAD_FOLDER"],file.filename)

        file.save(filepath)

        df=pd.read_csv(filepath)

        x=df["Hours"].values
        y=df["Marks"].values

        n=len(x)

        sumx=np.sum(x)
        sumy=np.sum(y)

        sumxy=np.sum(x*y)
        sumx2=np.sum(x*x)

        m=(n*sumxy-sumx*sumy)/(n*sumx2-sumx**2)

        c=(sumy-m*sumx)/n

        hours=float(request.form["hours"])

        marks=m*hours+c

        prediction=f"Predicted Marks = {marks:.2f}"

        equation=f"Equation : Y = {m:.2f}X + {c:.2f}"

        plt.figure(figsize=(6,4))

        plt.scatter(x,y,color='blue')

        plt.plot(x,m*x+c,color='red')

        plt.xlabel("Hours Studied")

        plt.ylabel("Marks")

        plt.title("Simple Linear Regression")

        plt.savefig("static/graph.png")

        plt.close()

    return render_template("index.html",
                           prediction=prediction,
                           equation=equation)


if __name__=="__main__":

    app.run(debug=True)