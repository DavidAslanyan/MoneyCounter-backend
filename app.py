from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from config import ApplicationConfig
from models import db, Accounts, Transactions, update_earned, update_spent

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object(ApplicationConfig)

bcrypt = Bcrypt(app)
server_session = Session(app)
db.init_app(app)

with app.app_context():
  db.create_all()



@app.route("/@me")
def get_current_user():
  user_id = session.get("user_id")
  
  if user_id:
    account = Accounts.query.filter_by(id=user_id).first()
    return jsonify({
      "id": account.id,
      "name": account.name,
      "email": account.email,
      "cash": account.cash
    })

  else:
    return jsonify({"error": "unauthorized"})


@app.route("/register", methods=["POST"])
def register():
  name = request.json["name"]
  birthYear = request.json["date"]
  email = request.json["email"]
  password = request.json["password"]

  if not name or not birthYear or not email or not password:
    return jsonify({"error": "Invalid credentials"}), 401

  accountExists = Accounts.query.filter_by(email=email).first() is not None

  if accountExists:
    return jsonify({"error": "User already exists"}), 409

  hashPassword = bcrypt.generate_password_hash(password).decode('utf8')
  new_account = Accounts(name=name, birth_year=birthYear, email=email, password=hashPassword)
  db.session.add(new_account)
  db.session.commit()

  session["user_id"] = new_account.id

  return jsonify({
    "id": new_account.id,
    "name": new_account.name,
    "email": new_account.email
  })


@app.route("/login", methods=["POST"])
def login():
  email = request.json["email"]
  password = request.json["password"]

  account = Accounts.query.filter_by(email=email).first()

  if account is None:
    return jsonify({"error": "Unauthorized"}), 401

  if not bcrypt.check_password_hash(account.password, password):
    return jsonify({"error": "Unauthorized"}), 401

  session["user_id"] = account.id

  return jsonify({
    "id": account.id,
    "name": account.name,
    "email": account.email
  })


@app.route("/modify", methods=["POST"])
def modify():
  user_id = session.get("user_id")

  if not user_id:
    return jsonify({"error": "Unauthorized"}), 401


  EXPANCETYPES = [
  "food",
  "family",
  "gifts",
  "utilities",
  "debts",
  "bills",
  "car",
  "clothes",
  "fun",
  "calls"
  "health",
  "pets",
  "sports",
  "taxi",
  "toiletry",
  "transport"
  "other"
  ]

  INCOMETYPES = [
    "salary",
    "savings",
    "gifts",
    "credit",
    "other"
  ]

  TYPENONE = 'none'

  setDate = request.json["setDate"]
  earned = request.json["earned"]
  spent = request.json["spent"]
  typeSpent = request.json["newTypeSpent"]
  typeEarned = request.json["newTypeEarned"]
  info = request.json["info"]

  if not spent or spent == '':
    spent = 0

  if not earned or earned == '':
    earned = 0

  if not typeSpent or typeSpent == '':
    typeSpent = TYPENONE

  if typeSpent not in EXPANCETYPES:
    typeSpent = TYPENONE

  if not typeEarned or typeEarned == '':
    typeEarned = TYPENONE

  if typeEarned not in INCOMETYPES:
    typeEarned = TYPENONE

  if not setDate or setDate == '':
    setDate = 'No date'

  if not info or info == '':
    info = 'No info'

  newTransaction = Transactions(
    user_id = user_id,
    setDate=setDate, earned=earned, 
    spent=spent, typeEarned=typeEarned, 
    typeSpent=typeSpent, info=info)
  
  db.session.add(newTransaction)
  db.session.commit()

  if spent == 0:
    update_earned(user_id, earned)

  if earned == 0:
    update_spent(user_id, spent)

  return jsonify({
    "id": newTransaction.id,
    "setDate": newTransaction.setDate,
    "earned": newTransaction.earned,
    "spent": newTransaction.spent,
    "typeEarned": newTransaction.typeEarned,
    "typeSpent": newTransaction.typeSpent,
    "info": newTransaction.info,
  })



@app.route("/history", methods=['GET'])
def history():
  user_id = session.get("user_id")
  if not user_id:
    return jsonify({"error": "Unauthorized"})

  results = Transactions.query.filter_by(user_id=user_id).all()
  results = [result.to_dict() for result in results]
  return jsonify(results)


@app.route("/logout", methods=["POST"])
def logout():
  session.pop("user_id")
  return "200"


if __name__ == "__main__":
  app.run(debug=True)