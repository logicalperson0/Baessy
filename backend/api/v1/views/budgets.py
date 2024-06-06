#!/usr/bin/python3
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.budget import Budget
from models.user import User

@app_views.route("/budgets", methods=["GET"])
def get_budgets():
    """
    retrieves all budget objects
    :return: json of all states
    """
    
    budgets = storage.all("Budget").values()

    return jsonify([budget.to_dict() for budget in budgets])


@app_views.route("/users/<user_id>/budgets", methods=["GET"])
def budgets_by_user(user_id):
    """
    Get the budget of the given user by their id
    """
    expense = storage.get(User, user_id)

    # exp = expense.expenses

    if expense is None:
        abort(404)

    #expe = expense.to_dict()
    expe = [exp.to_dict() for exp in expense.budgets]
    return jsonify(expe)

@app_views.route("/budgets/<budget_id>",  methods=["GET"])
def budget_by_id(budget_id):
    """
    gets a specific expense object by ID
    :param expense_id: expense object id
    :return: expense obj with the specified id or error
    """

    expense = storage.get(Budget, budget_id)

    if expense is None:
        abort(404)

    return jsonify(expense.to_dict())


@app_views.route("/budgets", methods=["POST"])
def budget_create():
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

    budget = Budget(**expense_json)
    budget.save()

    return jsonify(budget.to_dict()), 201


@app_views.route("/budgets/<budget_id>",  methods=["PUT"])
def budget_put(budget_id):
    """
    updates specific Expense object by ID
    :param expense_id: expense object ID
    :return: expense object and 200 on success, or 400 or
    404 on failure
    """
    expense_json = request.get_json(silent=True)
    if expense_json is None:
        abort(400, 'Not a JSON')

    expense = storage.get(Budget, budget_id)

    if expense is None:
        abort(404)

    for key, val in expense_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id"]:
            setattr(expense, key, val)
    expense.save()

    return jsonify(expense.to_dict())


@app_views.route("/budgets/<budget_id>", methods=["DELETE"])
def budget_delete_by_id(budget_id):
    """
    deletes Expense by id
    :param expense_id: expense object id
    :return: empty dict with 200 or 404 if not found
    """

    expense = storage.get(Budget, budget_id)

    if expense is None:
        abort(404)

    storage.delete(expense)
    storage.save()

    return jsonify({})
