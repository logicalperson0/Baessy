#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.expense import Expense
from models.user import User

@app_views.route("/expenses", methods=["GET"])
def get_expenses():
    """
    retrieves all expenses objects
    :return: json of all states
    """
    
    expenses = storage.all("Expense").values()

    return jsonify([expense.to_dict() for expense in expenses])


@app_views.route("/users/<user_id>/expenses", methods=["GET"])
def expense_by_user(user_id):
    """
    Get the expenses of the given user by their id
    """
    expense = storage.get(User, user_id)

    # exp = expense.expenses

    if expense is None:
        abort(404)

    #expe = expense.to_dict()
    expe = [exp.to_dict() for exp in expense.expenses]
    return jsonify(expe)

@app_views.route("/expenses/<expense_id>",  methods=["GET"])
def expense_by_id(expense_id):
    """
    gets a specific expense object by ID
    :param expense_id: expense object id
    :return: expense obj with the specified id or error
    """

    expense = storage.get(Expense, expense_id)

    if expense is None:
        abort(404)

    return jsonify(expense.to_dict())


@app_views.route("/expenses", methods=["POST"])
def expense_create():
    """
    create expense route
    :return: newly created expense obj
    """
    expense_json = request.get_json(silent=True)
    if expense_json is None:
        abort(400, 'Not a JSON')

    if "user_id" not in expense_json:
        abort(400, 'Missing user_id')
    if not storage.get(User, expense_json["user_id"]):
        abort(404)
    #if not User.get(expense_json["user_id"]):
     #   abort(404)

    expense = Expense(**expense_json)
    expense.save()

    return jsonify(expense.to_dict()), 201


@app_views.route("/expenses/<expense_id>",  methods=["PUT"])
def expense_put(expense_id):
    """
    updates specific Expense object by ID
    :param expense_id: expense object ID
    :return: expense object and 200 on success, or 400 or
    404 on failure
    """
    expense_json = request.get_json(silent=True)
    if expense_json is None:
        abort(400, 'Not a JSON')

    expense = storage.get(Expense, expense_id)

    if expense is None:
        abort(404)

    for key, val in expense_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id"]:
            setattr(expense, key, val)
    expense.save()

    return jsonify(expense.to_dict())


@app_views.route("/expenses/<expense_id>", methods=["DELETE"])
def expense_delete_by_id(expense_id):
    """
    deletes Expense by id
    :param expense_id: expense object id
    :return: empty dict with 200 or 404 if not found
    """

    expense = storage.get(Expense, expense_id)

    if expense is None:
        abort(404)

    storage.delete(expense)
    storage.save()

    return jsonify({})
