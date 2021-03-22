# importing the modules
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

# app config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///food.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# food model
class FoodModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),nullable=False)
    price = db.Column(db.Float,nullable=False)

    def __repr__(self):
        return '<Food %s>' % self.name



# create and get
@app.route("/",methods=['GET','POST'])
def index():
    if request.method == "POST":
        foodname = request.form['foodname']
        price = request.form['price']
        food = FoodModel(name=foodname,price=float(price))
        try:
            db.session.add(food)
            db.session.commit()
            return redirect("/")
        except:
            return "Food Addition Failed. Please Try Again"
    else:
        foods = FoodModel.query.all()
        return render_template('index.html',foods=foods)

# delete food
@app.route("/delete/<int:id>")
def delete(id):
    food_to_delete = FoodModel.query.get_or_404(id)
    try:
        db.session.delete(food_to_delete)
        db.session.commit()
        return redirect("/")
    except:
        return 'Deletion Failed. Please Try Again'


# update food
@app.route("/update/<int:id>",methods=["GET","POST"])
def update(id):
    if request.method == "POST":
        food_to_update = FoodModel.query.get_or_404(id)
        foodname = request.form['foodname']
        price = request.form['price']
        try:
            food_to_update.name = foodname
            food_to_update.price = float(price)
            db.session.commit()
            return redirect("/")
        except: 
            return 'Updation Failed. Please Try Again'
    else:
        food_to_update = FoodModel.query.get_or_404(id)
        return render_template("update.html",food=food_to_update)

# run server
if __name__ == "__main__":
    app.run(debug=True)