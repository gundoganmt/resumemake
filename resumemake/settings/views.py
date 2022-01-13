from flask import render_template, Blueprint, request, jsonify
from flask_login import login_required, current_user
from utils import allowed_img_file, get_extension, UPLOAD_PROFILE_FOLDER
from werkzeug.utils import secure_filename
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
    return jsonify({"success": True, "current_field": "acc_g", "name": name, "filename": filename})
