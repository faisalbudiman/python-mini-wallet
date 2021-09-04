from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, set_access_cookies
)
from flask_bcrypt import Bcrypt

from database.database_factory import DatabaseFactory
from services.user_service import UserService
from services.wallet_service import WalletService
from os import environ



app = Flask(__name__)
app.config.from_object(environ.get('CONFIG_SETTING'))
engine = DatabaseFactory.get()

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET'])
def home():
    return {'status': 'success'}

################# INIT ACCOUNT ######################
@app.route("/api/v1/init", methods=['POST'])
def init_account():
    try:
        id = request.form.get("id")
        user = UserService(engine).insert_new_user(id)
        if user:
            access_token = create_access_token(identity=user.get('id'))
            resp = jsonify({
                        "status": "success",
                        'data': {
                            "token": access_token
                        }
                    })
            set_access_cookies(resp, access_token)
            return resp, 200
        else:
            return jsonify({'status': 'fail', 'data': {"user": "Failed to init user."}}), 400
    except:
        return jsonify({'status': 'fail', 'data': None}), 401

################# ACTIVATE WALLET ######################
@app.route("/api/v1/wallet", methods=['POST'])
@jwt_required
def activate_wallet():
    try:
        user_id = get_jwt_identity()
        user = UserService(engine).get_user_by_id(user_id)
        if user:
            balance = WalletService(engine).activate_wallet(user_id)
            return {"status": "success",
                    "data": {
                        "wallet": balance
                    }}, 200
        else:
            return jsonify({'status': 'fail', 'data': {"user": "User not found."}}), 400
    except:
        return jsonify({'status': 'fail', 'data': None}), 400

################# MY WALLET ######################
@app.route("/api/v1/wallet", methods=['GET'])
@jwt_required
def my_wallet():
    try:
        user_id = get_jwt_identity()
        user = UserService(engine).get_user_by_id(user_id)
        if user:
            wallet_service = WalletService(engine)
            my_wallet = wallet_service.my_wallet(user_id)
            if my_wallet:
                return {"status": "success",
                        "data": {
                            "wallet": my_wallet
                        }}, 200
        else:
            return jsonify({'status': 'fail', 'data': {"user": "User not found."}}), 400
    except:
        return jsonify({'status': 'fail', 'data': None}), 400

################# DEPOSITE ######################
@app.route("/api/v1/wallet/deposits", methods=['POST'])
@jwt_required
def deposite():
    try:
        user_id = get_jwt_identity()
        amount = request.form.get("amount")
        if int(amount) <= 0:
            return jsonify({'status': 'fail', 'data': {"amount": "must be positif integer"}}), 400
        reference_id = request.form.get("reference_id")
        user = UserService(engine).get_user_by_id(user_id)
        if user:
            wallet_service = WalletService(engine)
            deposite = wallet_service.deposite(user_id, int(amount), reference_id)
            if deposite:
                return {"status": "success",
                        "data": {
                            "deposite": deposite
                        }}, 200
        else:
            return jsonify({'status': 'fail', 'data': {"user": "User not found."}}), 400
    except:
        return jsonify({'status': 'fail', 'data': None}), 400

################# WITHDRAWALS ######################
@app.route("/api/v1/wallet/withdrawals", methods=['POST'])
@jwt_required
def withdrawals():
    try:
        user_id = get_jwt_identity()
        amount = request.form.get("amount")
        if int(amount) <= 0:
            return jsonify({'status': 'fail', 'data': {"amount": "must be positif integer"}}), 400
        reference_id = request.form.get("reference_id")
        user = UserService(engine).get_user_by_id(user_id)
        if user:
            wallet_service = WalletService(engine)
            deposite = wallet_service.withdrawals(user_id, int(amount), reference_id)
            if deposite:
                return {"status": "success",
                        "data": {
                            "deposite": deposite
                        }}, 200
        else:
            return jsonify({'status': 'fail', 'data': {"user": "User not found."}}), 400
    except:
        return jsonify({'status': 'fail', 'data': None}), 400

################# DEACTIVATE WALLET ######################
@app.route("/api/v1/wallet", methods=['PATCH'])
@jwt_required
def deactivate_wallet():
    try:
        user_id = get_jwt_identity()
        user = UserService(engine).get_user_by_id(user_id)
        if user:
            balance = WalletService(engine).deactivate_wallet(user_id)
            return {"status": "success",
                    "data": {
                        "wallet": balance
                    }}, 200
        else:
            return jsonify({'status': 'fail', 'data': {"user": "User not found."}}), 400
    except:
        return jsonify({'status': 'fail', 'data': None}), 400

if __name__ == '__main__':
    app.run()