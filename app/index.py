from flask import Flask, render_template, request, redirect, url_for, flash, url_for
from app.models import Medicine, MedicineUnit, UserRoleEnum
import dao
from app import app, db, login, utils
from flask_login import login_user, logout_user, login_required


@app.route('/')
def index():
    return render_template('index.html', UserRoleEnum=UserRoleEnum)

# them1 sua xoa thuoc
@app.route('/medicine/index')
def medicine():
    get_medicine = dao.get_medicine()
    get_medicineunit = dao.get_medicineunit()
    return render_template('medicine/index.html', thuoc=get_medicine, get_medicineunit=get_medicineunit)


@app.route('/medicine/create')
def medicine_add():
    get_medicineunit = dao.get_medicineunit()
    return render_template('medicine/create.html', get_medicineunit=get_medicineunit)
    # insertthuoc = dao.insertthuoc()


@app.route('/medicine/create/submit', methods=['POST'])
def medicine_submit():
    if request.method == "POST":
        medicine_name = request.form['medicine_name']
        how_to_use = request.form['how_to_use']
        price = request.form['price']
        unit_id = request.form['unit_id']

        medicine = Medicine(medicine_name = medicine_name, how_to_use = how_to_use, price=price, unit_id=unit_id)

        db.session.add(medicine)
        db.session.commit()

    return redirect('/medicine/index')


@app.route('/medicine/delete/<int:id>')
def delete_medicine(id):
    task_to_delete = Medicine.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/medicine/index')
    except:
        return 'Có lỗi sảy ra khi xóa'


@app.route('/medicine/update/<int:id>', methods=['GET', 'POST'])
def update_medicine(id):
    task = Medicine.query.get_or_404(id)
    get_medicineunit = dao.get_medicineunit()
    if request.method == "POST":
        task.medicine_name = request.form['medicine_name']
        task.how_to_use = request.form['how_to_use']
        task.price = request.form['price']
        task.unit_id = request.form['unit_id']

        try:
            db.session.commit()
            return redirect('/medicine/index')
        except:
            return 'Có lỗi sẩy ra khi cập nhật'

    else:
        return render_template('medicine/update.html', task=task, get_medicineunit=get_medicineunit)

# them sua xoa don vi
@app.route('/medicineunit/index')
def medicineunit():
    get_medicineunit = dao.get_medicineunit()
    return render_template('medicineunit/index.html', get_medicineunit=get_medicineunit)

@app.route('/medicineunit/create')
def medicineunit_add():
    return render_template('medicineunit/create.html')

@app.route('/medicineunit/create/submit', methods=['POST'])
def medicineunit_submit():
    if request.method == "POST":
        unit_name = request.form['unit_name']

        medicineunit = MedicineUnit(unit_name = unit_name)

        db.session.add(medicineunit)
        db.session.commit()

    return redirect('/medicineunit/index')

@app.route('/medicineunit/update/<int:id>', methods=['GET', 'POST'])
def update_medicineunit(id):
    task2 = MedicineUnit.query.get_or_404(id)

    if request.method == "POST":
        task2.unit_name = request.form['unit_name']
        try:
            db.session.commit()
            return redirect('/medicineunit/index')
        except:
            return 'Có lỗi sẩy ra khi cập nhật'

    else:
        return render_template('medicineunit/update.html', task2=task2)

@app.route('/medicineunit/delete/<int:id>')
def delete_medicineunit(id):
    task_to_delete = MedicineUnit.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/medicineunit/index')
    except:
        return 'Có lỗi sảy ra khi xóa'


# tranh chính
@app.route('/home')
def home():
    return render_template('homepage/index.html', UserRoleEnum=UserRoleEnum)



@app.route('/home/services')
def services():
    return render_template('homepage/services.html')

@app.route('/admin-login', methods=['post'])
def signin_admin():
    err_msg = ""
    try:
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_userlogin(username=username,
                                 password=password,)
        if user:
            login_user(user=user)
            return redirect(url_for('index'))
        else:
            err_msg = 'Tài khoản hoặc mật khẩu không chính xác'
    except Exception as ex:
        err_msg = str(ex)
    return render_template('index.html', err_msg=err_msg)



@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            user = utils.check_userlogin(username=username, password=password)

            if user:
                login_user(user=user)
                return redirect(url_for('index'))
            else:
                err_msg = 'Tên đăng nhập hoặc mật khẩu không chính xác'
        except Exception as ex:
            err_msg = str(ex)
    return render_template('homepage/login.html', err_msg=err_msg)



@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        try:
            if password.strip().__eq__(confirm.strip()):
                utils.add_user(name=name, username=username, password=password)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Xác nhận mật khẩu không chính xác'
        except Exception as ex:
            err_msg = "Lỗi: " + str(ex)

    return render_template('homepage/register.html', err_msg=err_msg)



@login.user_loader
def get_user(user_id):
    return dao.get_user_by_id(user_id)

if __name__ == "__main__":
    app.run(debug=True)
