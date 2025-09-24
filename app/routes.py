# app/routes.py
from flask import Blueprint, jsonify
from .schedule import get_cache

routes = Blueprint("routes", __name__)


@routes.route("/trends")
def get_trends():
  return jsonify({"trends": get_cache()})