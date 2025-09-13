from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import os
from dateutil.relativedelta import relativedelta

app = Flask(__name__)

# Configuration de la base de données
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration pour la production
if os.environ.get('DATABASE_URL'):
    # Production (Heroku, Railway, etc.)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
else:
    # Développement local
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "finance.db")}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle de données pour les transactions
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'income' ou 'expense'
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_recurring = db.Column(db.Boolean, default=False)
    recurring_parent_id = db.Column(db.Integer, db.ForeignKey('recurring_transaction.id'), nullable=True)

# Modèle pour les transactions récurrentes
class RecurringTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(10), nullable=False)  # 'income' ou 'expense'
    category = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(20), nullable=False)  # 'daily', 'weekly', 'monthly', 'yearly'
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)  # None pour récurrence infinie
    next_occurrence = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'transaction_type': self.transaction_type,
            'category': self.category,
            'frequency': self.frequency,
            'start_date': self.start_date.strftime('%Y-%m-%d'),
            'end_date': self.end_date.strftime('%Y-%m-%d') if self.end_date else None,
            'next_occurrence': self.next_occurrence.strftime('%Y-%m-%d'),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        }

# Méthode to_dict pour Transaction
def transaction_to_dict(transaction):
    return {
        'id': transaction.id,
        'description': transaction.description,
        'amount': transaction.amount,
        'transaction_type': transaction.transaction_type,
        'category': transaction.category,
        'date': transaction.date.strftime('%Y-%m-%d'),
        'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'is_recurring': transaction.is_recurring
    }

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# API pour ajouter une transaction
@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    try:
        data = request.get_json()
        
        transaction = Transaction(
            description=data['description'],
            amount=float(data['amount']),
            transaction_type=data['transaction_type'],
            category=data['category'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date()
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Transaction ajoutée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# API pour récupérer toutes les transactions
@app.route('/api/transactions')
def get_transactions():
    transactions = Transaction.query.order_by(Transaction.date.desc()).all()
    return jsonify([transaction_to_dict(t) for t in transactions])

# API pour supprimer une transaction
@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Transaction supprimée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# API pour obtenir le solde total
@app.route('/api/balance')
def get_balance():
    try:
        income = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.transaction_type == 'income'
        ).scalar() or 0
        
        expenses = db.session.query(db.func.sum(Transaction.amount)).filter(
            Transaction.transaction_type == 'expense'
        ).scalar() or 0
        
        balance = income - expenses
        
        return jsonify({
            'balance': balance,
            'income': income,
            'expenses': expenses
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# API pour les statistiques par catégorie
@app.route('/api/statistics')
def get_statistics():
    try:
        # Statistiques des dépenses par catégorie
        expense_stats = db.session.query(
            Transaction.category,
            db.func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.transaction_type == 'expense'
        ).group_by(Transaction.category).all()
        
        # Statistiques des revenus par catégorie
        income_stats = db.session.query(
            Transaction.category,
            db.func.sum(Transaction.amount).label('total')
        ).filter(
            Transaction.transaction_type == 'income'
        ).group_by(Transaction.category).all()
        
        return jsonify({
            'expenses_by_category': [{'category': cat, 'amount': float(total)} for cat, total in expense_stats],
            'income_by_category': [{'category': cat, 'amount': float(total)} for cat, total in income_stats]
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# API pour les transactions récurrentes
@app.route('/api/recurring-transactions', methods=['GET'])
def get_recurring_transactions():
    try:
        recurring = RecurringTransaction.query.filter_by(is_active=True).all()
        return jsonify([r.to_dict() for r in recurring])
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/recurring-transactions', methods=['POST'])
def create_recurring_transaction():
    try:
        data = request.get_json()
        
        # Calculer la prochaine occurrence
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        next_occurrence = calculate_next_occurrence(start_date, data['frequency'])
        
        recurring = RecurringTransaction(
            description=data['description'],
            amount=float(data['amount']),
            transaction_type=data['transaction_type'],
            category=data['category'],
            frequency=data['frequency'],
            start_date=start_date,
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None,
            next_occurrence=next_occurrence
        )
        
        db.session.add(recurring)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Transaction récurrente créée avec succès'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# API pour le calendrier
@app.route('/api/calendar/<int:year>/<int:month>')
def get_calendar_data(year, month):
    try:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)
        
        # Récupérer les transactions du mois
        transactions = Transaction.query.filter(
            Transaction.date >= start_date,
            Transaction.date <= end_date
        ).all()
        
        # Récupérer les transactions récurrentes qui devraient se déclencher ce mois
        recurring = RecurringTransaction.query.filter(
            RecurringTransaction.is_active == True,
            RecurringTransaction.next_occurrence >= start_date,
            RecurringTransaction.next_occurrence <= end_date
        ).all()
        
        calendar_data = {}
        
        # Ajouter les transactions normales
        for transaction in transactions:
            day = transaction.date.day
            if day not in calendar_data:
                calendar_data[day] = {'transactions': [], 'total_income': 0, 'total_expense': 0}
            
            calendar_data[day]['transactions'].append({
                'id': transaction.id,
                'description': transaction.description,
                'amount': transaction.amount,
                'type': transaction.transaction_type,
                'category': transaction.category,
                'is_recurring': transaction.is_recurring
            })
            
            if transaction.transaction_type == 'income':
                calendar_data[day]['total_income'] += transaction.amount
            else:
                calendar_data[day]['total_expense'] += transaction.amount
        
        # Ajouter les transactions récurrentes
        for recurring_trans in recurring:
            day = recurring_trans.next_occurrence.day
            if day not in calendar_data:
                calendar_data[day] = {'transactions': [], 'total_income': 0, 'total_expense': 0}
            
            calendar_data[day]['transactions'].append({
                'id': f"recurring_{recurring_trans.id}",
                'description': recurring_trans.description + " (récurrent)",
                'amount': recurring_trans.amount,
                'type': recurring_trans.transaction_type,
                'category': recurring_trans.category,
                'is_recurring': True,
                'recurring_id': recurring_trans.id
            })
            
            if recurring_trans.transaction_type == 'income':
                calendar_data[day]['total_income'] += recurring_trans.amount
            else:
                calendar_data[day]['total_expense'] += recurring_trans.amount
        
        return jsonify(calendar_data)
    except Exception as e:
        return jsonify({'error': str(e)})

# Fonction utilitaire pour calculer la prochaine occurrence
def calculate_next_occurrence(start_date, frequency):
    if frequency == 'daily':
        return start_date + timedelta(days=1)
    elif frequency == 'weekly':
        return start_date + timedelta(weeks=1)
    elif frequency == 'monthly':
        return start_date + relativedelta(months=1)
    elif frequency == 'yearly':
        return start_date + relativedelta(years=1)
    else:
        return start_date

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=3000)
