from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.categories.models import Category
from application.categories.forms import CategoryForm
from application.transactions.models import Transaction

@app.route("/categories", methods = ["GET", "POST"])
@login_required(roles=["USER","ADMIN"])
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
@login_required(roles=["USER","ADMIN"])
def delete_category(category_id):

    u = current_user
    cat = Category.query.filter_by(id=category_id).first()

    if cat.name == "No Category":
        return redirect(url_for("categories", error="Category \"No Category\" cannot be deleted!"))

    if u.id == cat.user_id:
        #TODO: remove this category from all transactions

        transactions = Transaction.query.filter_by(category_id = cat.id)
        noCat = Category.query.filter_by(user_id=u.id, name = "No Category").first()

        for t in transactions:
            t.category_id = noCat.id
            db.session.add(t)
            db.session.commit()

        db.session.delete(cat)
        db.session.commit()
        return redirect(url_for("categories", error=""))
    
    return "Not found"

@app.route("/categories/<category_id>")
@login_required(roles=["USER","ADMIN"])
def category(category_id):
    
    c = Category.query.get(category_id)
    if c.user_id == current_user.id:
        # Category information: The name of the category, transactions in that category, accounts in that category
        category_data = Category.get_transactions_by_account_for_category(category_id)
        return render_template("/categories/categorysummary.html", transactions = category_data, category = c)
    else:
        return "Unauthorized, fool!"
