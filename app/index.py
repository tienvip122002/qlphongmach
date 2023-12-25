from flask import Flask, render_template, request, redirect, url_for, flash
from app.models import Thuoc
import dao
from app import app , db

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/thuoc/index')
def thuoc():
    thuoc = dao.load_thuocs()
    return render_template('thuoc/index.html', thuoc = thuoc)

@app.route('/thuoc/create')
def themthuoc():
    return render_template('thuoc/create.html')
    # insertthuoc = dao.insertthuoc()

@app.route('/thuoc/create/submit', methods=['POST'])
def submitthuoc():
    if request.method == "POST":
        tenthuoc = request.form['tenthuoc']
        cachdung = request.form['cachdung']
        soluong = request.form['soluong']
        donvi = request.form['donvi']

        thuoc = Thuoc(tenthuoc = tenthuoc, cachdung = cachdung, soluong = soluong, donvi = donvi)

        db.session.add(thuoc)
        db.session.commit()

    return redirect('/thuoc/index')

@app.route('/thuoc/delete/<int:id>')
def delete(id):
    task_to_delete = Thuoc.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/thuoc/index')
    except:
        return 'Có lỗi sảy ra khi xóa'


@app.route('/thuoc/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Thuoc.query.get_or_404(id)

    if request.method == "POST":
        task.tenthuoc = request.form['tenthuoc']
        task.cachdung = request.form['cachdung']
        task.soluong = request.form['soluong']
        task.donvi = request.form['donvi']


        try:
            db.session.commit()
            return redirect('/thuoc/index')
        except:
            return 'Có lỗi sẩy ra khi cập nhật'

    else:
        return render_template('thuoc/update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)

