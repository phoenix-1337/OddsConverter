from flask import Flask, render_template, request
from fractions import Fraction

app = Flask(__name__)

def validate_fractional_input(fractional_odds):
    if '/' in fractional_odds and all(part.isdigit() for part in fractional_odds.split('/')):
        return True
    return False

def fractional_to_decimal(fractional_odds):
    if validate_fractional_input(fractional_odds):
        numerator, denominator = map(int, fractional_odds.split('/'))
        return numerator / denominator + 1
    else:
        return None

def decimal_to_all(odds):
    fractional = decimal_to_fractional(odds)
    american = decimal_to_american(odds)
    percentage = decimal_to_percentage(odds)
    return {'decimal': odds, 'fractional': fractional, 'american': american, 'percentage': percentage}

def percentage_to_decimal(percentage):
    return round(100 / percentage, 2)

def decimal_to_fractional(decimal_odds):
    if decimal_odds == 1:
        return "1/1"
    fractional_odds = Fraction(decimal_odds - 1).limit_denominator()
    return f"{fractional_odds.numerator}/{fractional_odds.denominator}"

def decimal_to_american(decimal_odds):
    if decimal_odds >= 2.0:
        american_odds = int((decimal_odds - 1) * 100)
    else:
        american_odds = int(-100 / (decimal_odds - 1))
    return american_odds

def decimal_to_percentage(decimal_odds):
    percentage = round((1 / decimal_odds) * 100, 2)
    return percentage

def american_to_decimal(american_odds):
    if american_odds > 0:
        return american_odds / 100 + 1
    else:
        return 100 / abs(american_odds) + 1

@app.route('/', methods=['GET', 'POST'])
def index():
    converted_odds = None
    if request.method == 'POST':
        odds_input = request.form['odds']
        format = request.form['format']

        try:
            if format == 'decimal':
                odds = float(odds_input)
            elif format == 'fractional':
                odds = fractional_to_decimal(odds_input)
            elif format == 'american':
                odds = american_to_decimal(float(odds_input))
            elif format == 'percentage':
                odds = percentage_to_decimal(float(odds_input))

            if odds is not None:
                converted_odds = decimal_to_all(odds)
        except (ValueError, TypeError):
            pass  # Handle the error or return an error message

    return render_template('index.html', converted_odds=converted_odds)

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug=False)  # Set debug to False for production
