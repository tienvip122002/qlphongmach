from flask import Flask, render_template, request, redirect, url_for, flash, url_for
from app.models import Medicine
import dao
from app import app, db


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/medicine/index')
def medicine():
    thuoc = dao.get_medicine()
    return render_template('medicine/index.html', thuoc=thuoc)


@app.route('/medicine/create')
def medicine_add():
    return render_template('medicine/create.html')
    # insertthuoc = dao.insertthuoc()


@app.route('/medicine/create/submit', methods=['POST'])
def medicine_submit():
    if request.method == "POST":
        medicine_name = request.form['medicine_name']
        how_to_use = request.form['how_to_use']
        unit_name = request.form['unit_name']

        medicine = Medicine(medicine_name = medicine_name, how_to_use = how_to_use, unit_name = unit_name)

        db.session.add(medicine)
        db.session.commit()

    return redirect('/medicine/index')


@app.route('/medicine/delete/<int:id>')
def delete(id):
    task_to_delete = Medicine.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/medicine/index')
    except:
        return 'Có lỗi sảy ra khi xóa'


@app.route('/medicine/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Medicine.query.get_or_404(id)

    if request.method == "POST":
        task.tenthuoc = request.form['tenthuoc']
        task.cachdung = request.form['cachdung']
        task.soluong = request.form['soluong']
        task.donvi = request.form['donvi']

        try:
            db.session.commit()
            return redirect('/medicine/index')
        except:
            return 'Có lỗi sẩy ra khi cập nhật'

    else:
        return render_template('medicine/update.html', task=task)



@app.route('/home')
def home():
    return render_template('homepage/index.html')



@app.route('/home/services')
def services():
    return render_template('homepage/services.html')


if __name__ == "__main__":
    app.run(debug=True)
