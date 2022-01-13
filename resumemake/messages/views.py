from flask import render_template, Blueprint, jsonify
from flask_login import login_required, current_user
from resumemake.models import UserMails
from resumemake import db

messages = Blueprint('messages',__name__)

@messages.route('/inbox')
@login_required
def inbox():
    return render_template('messages/inbox.html')

@messages.route('/notifications')
@login_required
def notifications():
    return render_template('messages/notifications.html')

@messages.route('/get-message/<int:mail_id>')
@login_required
def getMessage(mail_id):
    data = UserMails.query.filter_by(id=mail_id).first()
    if not data:
        return jsonify({"msg": "Something went wrong! Refresh the page."})
    if current_user == data.mailed:
        return jsonify({"success": True, "content": data.content, "subject": data.subject})
    else:
        return jsonify({"msg": "You do not have a permission!"})

@messages.route('/delete-message/<int:mail_id>')
@login_required
def deleteMessage(mail_id):
    mail = UserMails.query.filter_by(id=mail_id).first()
    if not mail:
        return jsonify({"msg": "Something went wrong! Refresh the page."})
    if current_user == mail.mailed:
        db.session.delete(mail)
        db.session.commit()
        return jsonify({"success": True})
    else:
        return jsonify({"msg": "You do not have a permission!"})
