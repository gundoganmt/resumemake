from flask import render_template, Blueprint, request, jsonify, redirect, url_for
from flask_login import current_user, login_required
from utils import RESUME_SITES_NAMES
from resumemake import db
from resumemake.models import ResumeSite
import uuid

dashboard = Blueprint('dashboard',__name__)

@dashboard.route('/templates')
@login_required
def templates():
    return render_template('dashboard/create-site.html')

@dashboard.route('/my-sites')
@login_required
def mysites():
    return render_template('dashboard/my-sites.html')

@dashboard.route('/delete-site/<sitetype>/<site_id>')
@login_required
def deletesite(sitetype, site_id):
    if sitetype == 'resume':
        site = ResumeSite.query.filter_by(id=site_id, owner=current_user).first()
    if site:
        db.session.delete(site)
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@dashboard.route('/create-site', methods=['POST'])
@login_required
def createsite():
    site_name = request.form['site_name']
    template = request.form['template']
    if len(site_name.strip()) < 3 or len(site_name.strip()) > 30:
        return jsonify({'success': False, "msg": "Site name should be between 3 and 30 characters!"})
    else:
        if template in RESUME_SITES_NAMES:
            if ResumeSite.query.filter_by(site_name=site_name, owner=current_user).first():
                return jsonify({'success': False, "msg": "This site of yours already exist!"})
            else:
                site_id = str(uuid.uuid4())
                new_site = ResumeSite(site_id=site_id, site_name=site_name, template=template, user_id=current_user.id)
                db.session.add(new_site)
                db.session.commit()
                return jsonify({'success': True, "msg": url_for('resume.resumecreate', site_id=site_id, site_name=site_name)})
        else:
            return jsonify({'success': False, "msg": "Something went wrong! Refresh the page please."})

@dashboard.route('/pricing')
@login_required
def pricing():
    return render_template('pricing/pricing.html')

@dashboard.route('/publish/<site_name>')
@login_required
def publish(site_name):
    # site = BlogSite.query.filter_by(site_name=site_name).first()
    # site.current_plan = 'Premium'
    # db.session.commit()
    return render_template('pricing/thanks.html', site_name=site_name)
