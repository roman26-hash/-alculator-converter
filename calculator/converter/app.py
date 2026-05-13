from flask import Flask, render_template, request, redirect, url_for
from converters import (
    convert_length, convert_weight, convert_temperature,
    convert_currency, get_available_currencies
)

app = Flask(__name__)

CONVERSION_TYPES = {
    'length': 'Длина',
    'weight': 'Вес',
    'temperature': 'Температура',
    'currency': 'Валюта'
}

DEFAULT_UNITS = {
    'length': ('m', 'km'),
    'weight': ('kg', 'g'),
    'temperature': ('c', 'f'),
    'currency': ('USD', 'EUR')
}


@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    from_value = ''
    to_value = ''
    amount = ''
    conv_type = 'length'
    from_unit = ''
    to_unit = ''
    error = None

    if request.method == 'POST':
        conv_type = request.form.get('conv_type', 'length')
        amount_str = request.form.get('amount', '').strip()

        if not amount_str:
            error = 'Введите число для конвертации'
        else:
            try:
                amount = float(amount_str)
            except ValueError:
                error = 'Введите корректное число (например: 123.45)'
                amount = amount_str

        from_unit = request.form.get('from_unit', '')
        to_unit = request.form.get('to_unit', '')

        if not from_unit or from_unit not in get_units_for_type(conv_type):
            from_unit = DEFAULT_UNITS[conv_type][0]
        if not to_unit or to_unit not in get_units_for_type(conv_type):
            to_unit = DEFAULT_UNITS[conv_type][1]

        if not error:
            if conv_type == 'length':
                result = convert_length(amount, from_unit, to_unit)
                from_value = f"{amount} {from_unit}"
                to_value = f"{result:.4f} {to_unit}"

            elif conv_type == 'weight':
                result = convert_weight(amount, from_unit, to_unit)
                from_value = f"{amount} {from_unit}"
                to_value = f"{result:.4f} {to_unit}"

            elif conv_type == 'temperature':
                result = convert_temperature(amount, from_unit, to_unit)
                from_value = f"{amount}°{from_unit.upper()}"
                to_value = f"{result:.2f}°{to_unit.upper()}"

            elif conv_type == 'currency':
                result = convert_currency(amount, from_unit, to_unit)
                from_value = f"{amount:.2f} {from_unit}"
                to_value = f"{result:.2f} {to_unit}"

    if not from_unit:
        from_unit = DEFAULT_UNITS[conv_type][0]
    if not to_unit:
        to_unit = DEFAULT_UNITS[conv_type][1]

    length_units = ['m', 'km', 'cm', 'mm', 'mile', 'ft', 'in']
    weight_units = ['kg', 'g', 'mg', 'lb', 'oz', 't']
    temp_units = ['c', 'f', 'k']
    currency_units = get_available_currencies()

    return render_template('index.html',
                           result=result,
                           from_value=from_value,
                           to_value=to_value,
                           amount=amount,
                           conv_type=conv_type,
                           from_unit=from_unit,
                           to_unit=to_unit,
                           error=error,
                           CONVERSION_TYPES=CONVERSION_TYPES,
                           length_units=length_units,
                           weight_units=weight_units,
                           temp_units=temp_units,
                           currency_units=currency_units)


def get_units_for_type(conv_type):
    if conv_type == 'length':
        return ['m', 'km', 'cm', 'mm', 'mile', 'ft', 'in']
    elif conv_type == 'weight':
        return ['kg', 'g', 'mg', 'lb', 'oz', 't']
    elif conv_type == 'temperature':
        return ['c', 'f', 'k']
    elif conv_type == 'currency':
        return get_available_currencies()
    return []


if __name__ == '__main__':
    app.run(debug=True)