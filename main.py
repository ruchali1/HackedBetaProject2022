from flask import Flask, redirect, url_for, render_template
#redirect and url_for allows us to return a redirect from a spec function

app = Flask(__name__)

@app.route("/") #automatically sends us to the home page
def home():
    return render_template("index.html")

@app.route("/<name>") #whatever we put inside <> gets put into the name parameter
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin!"))
    #put name of function that will be redirected to

if __name__ == "__main__":
    app.run(debug=True) 