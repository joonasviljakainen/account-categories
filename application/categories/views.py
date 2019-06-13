from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.categories.models import Category
from application.categories.forms import CategoryForm

@app.route("/categories", methods = ["GET", "POST"])
@login_required
def categories(*args, **kwargs):
    if request.method == "GET":
        categories = Category.query.filter_by(user_id=current_user.id)
        error = kwargs.get("error", "")
        return render_template("/categories/categories.html",
            categories=categories, 
            form=CategoryForm(),
            error=error)
    else:
        form = CategoryForm(request.form)

        # If the user already has a category by that name, let's not create a duplicate
        alreadyExists = db.session.query(db.exists().where(Category.name == form.name.data).where(Category.user_id == current_user.id)).scalar()

        if alreadyExists:
            return redirect(url_for('categories', error=1))
        
        c = Category()
        c.name = form.name.data
        c.user_id = current_user.id
        db.session().add(c)
        db.session().commit()
        return redirect(url_for('categories', error=""))


@app.route("/categories/<category_id>/deletions", methods=["POST"])
@login_required
def delete_category(category_id):

    u = current_user
    cat = Category.query.filter_by(id=category_id).first()

    if u.id == cat.user_id:
        #TODO: remove this category from all transactions

        db.session.delete(cat)
        db.session.commit()
        return redirect(url_for("categories", error=""))
    
    return "Not found"

@app.route("/categories/<category_id>")
@login_required
def category(category_id):
    return "NOT IMPLEMENTED YET " + category_id