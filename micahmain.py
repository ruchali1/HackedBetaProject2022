from flask import Flask, redirect, url_for, render_template
#redirect and url_for allows us to return a redirect from a spec function

app = Flask(__name__)

@app.route('/') #automatically sends us to the home page
def home():
    return render_template("pippinflask.html") 

@app.route('/extra2.html')
def extra2():
    return render_template("extra2.html")

@app.route('/fivetoeight.html')
def fivetoeight():
    return render_template("fivetoeight.html")

@app.route('/chatbot.html')
def chatbot():
    return render_template("chatbot.html")

@app.route('/ninetoten.html')
def ninetoten():
    return render_template("ninetoten.html")

if __name__ == "__main__": 
    app.run(debug=True) 


'''

@app.route("/<name>") #whatever we put inside <> gets put into the name parameter
def user(name):
    return f"Hello {name}!"

@app.route("/admin")
def admin():
    return redirect(url_for("user", name="Admin"))
    #put name of function that will be redirected to 

'''
