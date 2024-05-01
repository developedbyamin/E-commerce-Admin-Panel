from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# SQLite database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    approved = db.Column(db.Boolean, default=False)

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class UserProblem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('problems', lazy=True))

class ProblemReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    response = db.Column(db.Text)
    problem_id = db.Column(db.Integer, db.ForeignKey('user_problem.id'), nullable=False)
    problem = db.relationship('UserProblem', backref=db.backref('reviews', lazy=True))

@app.route('/companies/awaiting_approval', methods=['GET'])
def get_companies_awaiting_approval():
    companies = Company.query.filter_by(approved=False).all()
    return jsonify([company.name for company in companies])

@app.route('/companies/approve', methods=['POST'])
def approve_company():
    company_id = request.json.get('company_id')
    company = Company.query.get(company_id)
    if company:
        company.approved = True
        db.session.commit()
        return jsonify({'message': 'Company approved successfully'})
    else:
        return jsonify({'message': 'Company not found'})

@app.route('/companies/reject', methods=['POST'])
def reject_company():
    company_id = request.json.get('company_id')
    company = Company.query.get(company_id)
    if company:
        db.session.delete(company)
        db.session.commit()
        return jsonify({'message': 'Company rejected successfully'})
    else:
        return jsonify({'message': 'Company not found'})

# Admin Management
@app.route('/admin/create', methods=['POST'])
def create_admin():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    hashed_password = generate_password_hash(password)
    new_admin = AdminUser(username=username, password_hash=hashed_password)
    db.session.add(new_admin)
    db.session.commit()

    return jsonify({'message': 'Admin created successfully'})

@app.route('/admin', methods=['GET'])
def get_admin_users():
    admins = AdminUser.query.all()
    return jsonify([admin.username for admin in admins])

@app.route('/user/register', methods=['POST'])
def user_register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/user/login', methods=['POST'])
def user_login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    return jsonify({'message': 'User logged in successfully', 'user_id': user.id}), 200

@app.route('/company/register', methods=['POST'])
def company_register():
    name = request.json.get('name')
    password = request.json.get('password')

    if not name or not password:
        return jsonify({'message': 'Name and password are required'}), 400

    existing_company = Company.query.filter_by(name=name).first()
    if existing_company:
        return jsonify({'message': 'Company name already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_company = Company(name=name, password_hash=hashed_password)
    db.session.add(new_company)
    db.session.commit()

    return jsonify({'message': 'Company registered successfully'}), 201

@app.route('/company/login', methods=['POST'])
def company_login():
    name = request.json.get('name')
    password = request.json.get('password')

    if not name or not password:
        return jsonify({'message': 'Name and password are required'}), 400

    company = Company.query.filter_by(name=name).first()
    if not company or not check_password_hash(company.password_hash, password):
        return jsonify({'message': 'Invalid name or password'}), 401

    return jsonify({'message': 'Company logged in successfully' , "compan_id": company.id}), 200

@app.route('/problems/submit', methods=['POST'])
def submit_problem():
    description = request.json.get('description')
    user_id = request.json.get('user_id')

    if not description or not user_id:
        return jsonify({'message': 'Description and user_id are required'}), 400

    new_problem = UserProblem(description=description, user_id=user_id)
    db.session.add(new_problem)
    db.session.commit()

    return jsonify({'message': 'Problem submitted successfully'}), 201

@app.route('/problems', methods=['GET'])
def get_problems():
    problems = UserProblem.query.all()
    return jsonify([problem.description for problem in problems])

@app.route('/admin/problems', methods=['GET'])
def get_all_problems():
    problems = UserProblem.query.all()
    return jsonify([{'problem_id': problem.id, 'description': problem.description} for problem in problems])

@app.route('/admin/review', methods=['POST'])
def review_problem():
    problem_id = request.json.get('problem_id')
    response = request.json.get('response')

    if not problem_id or not response:
        return jsonify({'message': 'Problem ID and response are required'}), 400

    problem = UserProblem.query.get(problem_id)
    if not problem:
        return jsonify({'message': 'Problem not found'}), 404

    new_review = ProblemReview(response=response, problem_id=problem_id)
    db.session.add(new_review)
    db.session.commit()

    return jsonify({'message': 'Problem reviewed successfully'}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
