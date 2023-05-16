from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    column1 = db.Column(db.String(50))
    column2 = db.Column(db.String(50))
    column3 = db.Column(db.String(50))

    def __repr__(self):
        return f'<Data {self.id}>'

def create_database():
    with app.app_context():
        db.create_all()

@app.route('/')
def index():
    data = Data.query.all()
    return render_template('index.html', data=data)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    df = pd.read_excel(file)
    with app.app_context():
        df.to_sql('data', con=db.engine, if_exists='append', index=False)
    return 'File uploaded successfully'

if __name__ == '__main__':
    create_database()
    app.run(debug=True)
