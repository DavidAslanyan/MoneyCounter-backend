from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
from datetime import datetime

db = SQLAlchemy()

def get_uuid():
  return uuid4().hex

def update_earned(user_id, earned):
    account = Accounts.query.get(user_id)
    account.cash += int(earned)
    db.session.commit()

def update_spent(user_id, spent):
    account = Accounts.query.get(user_id)
    account.cash -= int(spent)
    db.session.commit()


class Accounts(db.Model):
  __tablename__ = "accounts"
  id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
  name = db.Column(db.String(32), nullable=False)
  birth_year = db.Column(db.String(10), nullable=False)
  email = db.Column(db.String(345), unique=True)
  cash = db.Column(db.Numeric, default=0)
  password = db.Column(db.Text, nullable=False)


class Transactions(db.Model):
  __tablename__ = "transactions"
  id = db.Column(db.String(32), primary_key=True, default=get_uuid)
  user_id = db.Column(db.String(32), nullable=False)
  setDate = db.Column(db.String(10), nullable=False)
  earned = db.Column(db.Numeric, nullable=False, default=0)
  spent = db.Column(db.Numeric, nullable=False, default=0)
  typeSpent = db.Column(db.String)
  typeEarned = db.Column(db.String)
  time = db.Column(db.TIMESTAMP, default=datetime.utcnow)
  info = db.Column(db.String)
  foreign_key = db.ForeignKey('Accounts.id', ondelete='CASCADE')

  def to_dict(self):
    return {
      'id': self.id,
      'user_id': self.user_id,
      'setDate': self.setDate,
      'earned': str(self.earned),
      'spent': str(self.spent),
      'typeSpent': self.typeSpent,
      'typeEarned': self.typeEarned,
      'time': self.time.strftime("%Y-%m-%d %H:%M:%S"),
      'info': self.info
    }

  def to_stat(self):
    return {
      "earned": self.earned
    }