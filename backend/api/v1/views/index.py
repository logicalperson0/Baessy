#!/usr/bin/python3
"""
script that create a route /status on the object app_views that returns a JSON
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """create a Json of status"""
    return (jsonify({"status": "OK"}))


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    ta = storage.count("Tag")
    c = storage.count("Catagory")
    e = storage.count("Expense")
    b = storage.count("Budget")
    tr = storage.count("Transaction")
    u = storage.count("User")

    return (jsonify(tags=ta, catagories=c, expenses=e,
                    budgets=b, transactions=tr, users=u))
