
from flask import Blueprint
from . import member,food,cart,order,address,comment


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)
    member.api.register(bp_v1)
    food.api.register(bp_v1)
    cart.api.register(bp_v1)
    order.api.register(bp_v1)
    address.api.register(bp_v1)
    comment.api.register(bp_v1)


    return bp_v1