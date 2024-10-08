from flask import Flask, render_template, request, redirect, url_for, flash
from database import Database, Field

app = Flask(__name__)
app.secret_key = "your_secret_key"
db = None

@app.route('/')
def index():
    return render_template('index.html', db=db)

@app.route('/create_db', methods=['POST'])
def create_database():
    global db
    db_name = request.form['db_name']
    db = Database(db_name)
    flash(f"База даних '{db_name}' створена!", "success")
    return redirect(url_for('index'))

@app.route('/create_table', methods=['POST'])
def create_table():
    if db is None:
        flash("Спочатку створіть базу даних.", "error")
        return redirect(url_for('index'))

    table_name = request.form['table_name']
    try:
        db.create_table(table_name)
        flash(f"Таблиця '{table_name}' створена!", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('index'))

@app.route('/add_field', methods=['POST'])
def add_field():
    if db is None:
        flash("Спочатку створіть базу даних.", "error")
        return redirect(url_for('index'))

    table_name = request.form['table_name']
    field_name = request.form['field_name']
    field_type = request.form['field_type']

    if not field_name or not field_type:
        flash("Введіть назву та тип поля.", "error")
        return redirect(url_for('index'))

    try:
        field = Field(field_name, field_type)
        db.add_field_to_table(table_name, field)
        flash(f"Поле '{field_name}' додане до таблиці '{table_name}'!", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('index'))

@app.route('/edit_field', methods=['POST'])
def edit_field():
    if db is None:
        flash("Спочатку створіть базу даних.", "error")
        return redirect(url_for('index'))

    table_name = request.form['table_name']
    old_field_name = request.form['old_field_name']
    new_field_name = request.form['new_field_name']
    new_field_type = request.form['new_field_type']

    try:
        new_field = Field(new_field_name, new_field_type)
        db.edit_field_in_table(table_name, old_field_name, new_field)
        flash(f"Поле '{old_field_name}' змінено на '{new_field_name}'!", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('index'))

@app.route('/remove_field', methods=['POST'])
def remove_field():
    if db is None:
        flash("Спочатку створіть базу даних.", "error")
        return redirect(url_for('index'))

    table_name = request.form['table_name']
    field_name = request.form['field_name']

    try:
        db.remove_field_from_table(table_name, field_name)
        flash(f"Поле '{field_name}' видалено з таблиці '{table_name}'!", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('index'))

@app.route('/remove_table', methods=['POST'])
def remove_table():
    if db is None:
        flash("Спочатку створіть базу даних.", "error")
        return redirect(url_for('index'))

    table_name = request.form['table_name']

    try:
        db.remove_table(table_name)
        flash(f"Таблиця '{table_name}' видалена!", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('index'))

@app.route('/view_table', methods=['POST'])
def view_table():
    if db is None:
        flash("Спочатку створіть базу даних.", "error")
        return redirect(url_for('index'))

    table_name = request.form['table_name']
    try:
        table_data = db.view_table(table_name)
        return render_template('table_view.html', table_name=table_name, table_data=table_data)
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('index'))

@app.route('/view_all_tables', methods=['GET'])
def view_all_tables():
    if db is None:
        flash("Спочатку створіть базу даних.", "error")
        return redirect(url_for('index'))

    try:
        tables = db.view_all_tables()
        return render_template('all_tables_view.html', tables=tables)
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('index'))

@app.route('/save_db', methods=['POST'])
def save_db():
    if db is None:
        flash("Спочатку створіть базу даних.", "error")
        return redirect(url_for('index'))

    try:
        db.save_to_disk()
        flash("База даних збережена!", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
