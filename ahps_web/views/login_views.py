#
# AHPS Web - web server for managing an AtHomePowerlineServer instance
# Copyright (C) 2014  Dave Hocker (email: AtHomeX10@gmail.com)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the LICENSE file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (the LICENSE file).  If not, see <http://www.gnu.org/licenses/>.
#


from ahps_web import app
from flask import Flask, render_template_string, request, redirect, url_for, render_template, flash
from flask.ext.babel import Babel
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter

# Initialize Flask extensions
babel = Babel(app)                              # Initialize Flask-Babel
db = SQLAlchemy(app)                            # Initialize Flask-SQLAlchemy


# AHPS does not allowed unsolicited registration. The site admin
# is the only user who can create a new user account.
def register_disabled():
    return render_template("register_user_warning.html")


# Translations are used by the Flask-User package. AHPS itself
# does not use translations. It is English only.
@babel.localeselector
def get_locale():
    translations = [str(translation) for translation in babel.list_translations()]
    return request.accept_languages.best_match(translations)


# Define User model. Make sure to add flask.ext.user UserMixin!!
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')


# Create all database tables
db.create_all()


# Setup Flask-User
db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
user_manager = UserManager(db_adapter, app,
    register_view_function = register_disabled # disable user self-registration
    )     # Init Flask-User and bind to app


# Seed the admin account
admin = User.query.filter_by(username='admin').first()
if not admin:
    print "admin account does not exist. Creating..."
    user1 = User(username='admin', active=True,
            password=user_manager.hash_password('Password1'))
    db.session.add(user1)
    db.session.commit()
    print "admin account created. Be sure to change the password."


# The Profile page requires a logged-in user
@app.route('/new_user_page')
@login_required                                 # Use of @login_required decorator
def new_user_page():
    if current_user.username != "admin":
        return render_template("register_user_warning.html")
    return render_template("new_user_page.html")


# The Profile page requires a logged-in user
@app.route('/new_user_page/save', methods=["POST"])
@login_required                                 # Use of @login_required decorator
def save_new_user():
    if request.form["password"] != request.form["retype-password"]:
        return "Passwords do not match. Re-enter passwords."
    user1 = User(username=request.form["user_name"], active=True,
            password=user_manager.hash_password(request.form["password"]))
    db.session.add(user1)
    db.session.commit()

    flash("User {0} was created".format(request.form["user_name"]))

    return redirect(url_for("administration"))


# The Administration page
@app.route('/administration')
@login_required                                 # Use of @login_required decorator
def administration():
    # Only the admin user can perform user administration tasks
    if current_user.username != "admin":
        return render_template("register_user_warning.html")
    users = User.query.all()
    return render_template("user_admin.html", users=users)


# The Administration page
@app.route('/user/remove/<userid>')
@login_required                                 # Use of @login_required decorator
def remove_user(userid):
    # Only the admin user can perform user administration tasks
    if current_user.username != "admin":
        return render_template("register_user_warning.html")
    user = User.query.get(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("administration"))
