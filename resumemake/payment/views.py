from flask import render_template, Blueprint, jsonify, request
from flask_login import login_required, current_user
from resumemake import db, csrf

payment = Blueprint('payment',__name__)

@csrf.exempt
@payment.route('/paddle_webhook', methods=['POST'])
def paddle_webhook():
    ip_white = ['34.194.127.46', '54.234.237.108', '3.208.120.145']
    if request.remote_addr in ip_white:
        return jsonify({'msg': 'yes in whitelist'})
    if request.form['ip'] in ip_white:
        return jsonify({'msg': 'check request ip'})
    event_type = request.form['alert_name']
    if event_type == 'payment_succeeded':
        return jsonify({'msg': 'payment succeeded'})
