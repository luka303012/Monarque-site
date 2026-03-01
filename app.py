from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

db_path = os.path.join(os.path.dirname(__file__), 'monarque.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route('/')
def about():
    return render_template('about.html')

@app.route('/shop')
def shop():
    products = [
        {"category": "FOOTWEAR", "name": "PHANTOM WHITE", "price": "240", "desc": "Architectural design. Matte finish.", "img": "images/shoe1.png"},
        {"category": "FOOTWEAR", "name": "ONYX EDGE", "price": "180", "desc": "Limited performance silhouette.", "img": "images/shoe2.png"}
    ]
    return render_template('shop.html', items=products)

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'POST':
        user = request.form.get('user')
        text = request.form.get('text')
        if user and text:
            db.session.add(Review(user=user, text=text))
            db.session.commit()
            return redirect(url_for('reviews'))
    all_reviews = Review.query.order_by(Review.date.desc()).all()
    return render_template('reviews.html', reviews=all_reviews)

if __name__ == '__main__':
    app.run(debug=True, port=5001)