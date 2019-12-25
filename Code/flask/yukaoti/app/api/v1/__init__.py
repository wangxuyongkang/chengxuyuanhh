from flask import Blueprint
from . import index


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    index.api.register(bp_v1)
    return bp_v1