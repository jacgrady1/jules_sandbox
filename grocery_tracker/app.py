from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery_inventory.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Item model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    target_quantity = db.Column(db.Integer, default=1)
    unit = db.Column(db.String(20), default='pcs')
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Item {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'target_quantity': self.target_quantity,
            'unit': self.unit,
            'date_added': self.date_added.strftime('%Y-%m-%d %H:%M:%S'),
            'last_updated': self.last_updated.strftime('%Y-%m-%d %H:%M:%S')
        }

# --- CRUD Operations ---

# Create
@app.route('/add', methods=['POST'])
def add_item():
    try:
        data = request.form
        new_item = Item(
            name=data.get('name'),
            quantity=int(data.get('quantity', 1)),
            target_quantity=int(data.get('target_quantity', 1)),
            unit=data.get('unit', 'pcs')
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index_page'))
    except Exception as e:
        db.session.rollback()
        # A better error page or flash message would be good here later
        return jsonify({'error': str(e)}), 400

# Read All
@app.route('/')
def index_page():
    items = Item.query.order_by(Item.date_added.desc()).all()
    return render_template('index.html', items=items, message="Grocery Inventory")

# Route to render the edit item page
@app.route('/edit/<int:item_id>', methods=['GET'])
def edit_item_page(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('edit_item.html', item=item)

# Read One (JSON endpoint)
@app.route('/item/<int:item_id>')
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())

# Update
@app.route('/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    try:
        item = Item.query.get_or_404(item_id)
        data = request.form

        item.name = data.get('name', item.name)
        item.quantity = int(data.get('quantity', item.quantity))
        item.target_quantity = int(data.get('target_quantity', item.target_quantity))
        item.unit = data.get('unit', item.unit)
        item.last_updated = datetime.datetime.utcnow()

        db.session.commit()
        return redirect(url_for('index_page'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Delete
@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    try:
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('index_page'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
