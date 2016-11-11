from flask import render_template, flash, redirect, url_for, request
from .forms import LoginForm
from . import auth
from ..models import User
from flask.ext.login import login_user, login_required, logout_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            if user.verify_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(request.args.get('next') or url_for('main.root'))
            flash('Invalid password.')
        else:
            flash('Invalid username.')

    return render_template('auth/login.html',
                           title='Sign In',
                           form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))