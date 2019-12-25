from app.models.cart import MemberCart
from flask import jsonify
from app.models.order import PayOrder,PayOrderItem
from app.models.food import Food
from app.models.address import MemberAddress
import hashlib
import time
import random
from app import db



class OrderService:


    @staticmethod
    def orderSuccess(self, pay_order_id=0, params=None):
        try:
            pay_order_info = PayOrder.query.filter_by(id=pay_order_id).first()
            if not pay_order_info or pay_order_info.status not in [-8, -7]:
                return True

            pay_order_info.pay_sn = params['pay_sn'] if params and 'pay_sn' in params else ''
            pay_order_info.status = -7
            pay_order_info.express_status = -7
            db.session.add(pay_order_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            return False
        return True

def geneOrderSn():
    m = hashlib.md5()
    sn = None
    while True:
        str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
        m.update(str.encode("utf-8"))
        sn = m.hexdigest()
        if not PayOrder.query.filter_by(order_sn=sn).first():
            break
    return sn