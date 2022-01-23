from flask import render_template, Blueprint, request, jsonify
from flask_login import login_required, current_user
from utils import allowed_img_file, get_extension, UPLOAD_PROFILE_FOLDER
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from resumemake import db
import os, uuid

settings = Blueprint('settings',__name__)

@settings.route('/settings', methods=['GET'])
@login_required
def setting():
    return render_template('settings/settings.html')

@settings.route('/accountGeneral', methods=['POST'])
@login_required
def accountGeneral():
    current_user.name = request.form['name']
    current_user.surname = request.form['surname']
    current_user.email = request.form['email']
    current_user.username = request.form['username']
    current_user.account_desc = request.form['account_desc']

    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        if allowed_img_file(filename):
            filename = secure_filename(filename)
            unique_filename = str(uuid.uuid4())+get_extension(filename)
            current_user.profile_picture = unique_filename
            file.save(os.path.join(UPLOAD_PROFILE_FOLDER, unique_filename))

    db.session.commit()

    context = {
        "success": True, 
        "current_field": "acc_g", 
    }
    return jsonify(context)

@settings.route('/changePass', methods=['POST'])
@login_required
def changePass():
    old_pass = request.form['old_pass']
    new_pass = request.form['new_pass']
    retype_pass = request.form['retype_pass']

    if len(new_pass.strip()) < 6 or new_pass != retype_pass or not check_password_hash(current_user.password, old_pass):
        return jsonify({"success": False, "msg": "Some thing went wrong. Reason might be your password length is less than 6, or passwords didn't match or your password is not on our systems!"})
    else:
        current_user.password = generate_password_hash(new_pass, method='sha256')
        db.session.commit()
        return jsonify({"success": True, "current_field": "cp", "msg": "Your password has been changed!"})

