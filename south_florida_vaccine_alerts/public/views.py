# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (Blueprint, request, render_template, flash, url_for,
                   redirect, jsonify)
from flask_login import login_user, login_required, logout_user

from south_florida_vaccine_alerts.database import db_session
from south_florida_vaccine_alerts.extensions import login_manager
from south_florida_vaccine_alerts.user.models import User
from south_florida_vaccine_alerts.public.forms import LoginForm
from south_florida_vaccine_alerts.user.forms import RegisterForm
from south_florida_vaccine_alerts.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(db_session, int(user_id))


@blueprint.route("/", methods=['GET', 'POST'])
def home():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)
        db_session.add(new_user)
        db_session.commit()
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/about")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route("/status")
def status():
    return jsonify({'status': 'ok'})
