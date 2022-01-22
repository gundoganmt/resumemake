from flask import render_template, Blueprint, jsonify
from flask_login import login_required, current_user
from resumemake.models import UserMails, Notifications
from resumemake import db

messages = Blueprint('messages',__name__)

@messages.route('/inbox')
@login_required
def inbox():
    notifs = Notifications.query.all()
    for notif in notifs:
        db.session.delete(notif)
    db.session.commit()
    return render_template('messages/inbox.html')

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
    mail = UserMails.query.filter_by(id=mail_id, mailed=current_user).first()
    if not mail:
        return jsonify({"success": False, "msg": "Something went wrong! Refresh the page."})

    db.session.delete(mail)
    db.session.commit()

    return jsonify({"success": True})
