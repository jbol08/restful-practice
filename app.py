from flask import Flask, request, jsonify, render_template, url_for

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "111-222-4444-111"

connect_db(app)
# db.create_all()

@app.route('/')
def home():
    '''homepage'''

    return render_template('home.html')

@app.route('/api/cupcakes')
def cupcake_list():
    '''return a list of cupcakes'''
    cupcakes = [cupcake.cup_dict() for cupcake in Cupcake.query.all()]
    
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes',methods=["POST"])
def create_cupcake():
    '''user a form to make a cupcake'''

    data = request.json
    cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.cup_dict())


@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake_details(cupcake_id):
    '''get details on a specific cupcake'''

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.cup_dict())

@app.route('/api/cupcakes/<int:cupcake_id>',methods=["PATCH"])
def update_cupcake(cupcake_id):
    '''edit a specific cupcake'''
    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image'] 

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.cup_dict())

@app.route('/api/cupcakes/<int:cupcake_id>',methods=["DELETE"])
def delete_cupcake(cupcake_id):
    '''delete cupcake'''
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

