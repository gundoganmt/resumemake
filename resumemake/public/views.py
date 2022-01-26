from flask import render_template, Blueprint, request, Response, send_file, jsonify, redirect, url_for, abort
from flask_login import current_user
from resumemake.models import Users, Portfolios, UserMails, ResumeSite, Notifications
import pdfkit
from resumemake import db
from utils import only_main, send_email
import requests

public = Blueprint('public',__name__)

@public.route('/')
def index():
    if request.host == 'webpaget.com':
        return render_template('public/index.html')
    else:
        resume_site = ResumeSite.query.filter_by(domain=request.host).first_or_404()
        if resume_site.current_plan == 'published':
            return render_template('preview/resumes/' + resume_site.template + '.html', resume_site=resume_site)
        else:
            return jsonify({'success': 'Pending', 
                'msg': 'your domain appears to be connected but not published. Please publish first.'})

@public.route('/preview/<template>')
@only_main()
def preview(template):
    if template == 'sunshine':
        return render_template('preview/resumes/sunshine.html')

    elif template == 'ronaldo':
        return render_template('preview/resumes/ronaldo.html')

    elif template == 'elegant':
        return render_template('preview/resumes/elegant.html')

    else:
        return abort(404), 404

@public.route('/previewresume')
@only_main()
def previewresume():
    site_id = request.args.get('site_id', str)
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first_or_404()
    return render_template('preview/resumes/' + resume_site.template + '-rendered.html', resume_site=resume_site)

@public.route('/single-portfolio/<int:port_id>')
def singleport(port_id):
    port = Portfolios.query.filter_by(id=port_id).first()
    return render_template('preview/resumes/single-port.html', port=port)

@public.route('/usermails/<site_id>', methods=['POST'])
def usermails(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id).first()
    if not resume_site:
        return jsonify({"success": False, "msg": "Sorry, Something went wrong!"})

    mail = UserMails(full_name=request.form['full_name'],
        email=request.form['email'],
        subject=request.form['subject'],
        content=request.form['content'],
        mailed=resume_site.owner
    )
    notif = Notifications(resume_id=resume_site.id, not_to=resume_site.owner.id, not_type=1)

    db.session.add(notif)
    db.session.add(mail)
    db.session.commit()
    
    return jsonify({"success": True})

@public.route('/contact', methods=['POST'])
def contact():
    name=request.form['name']
    email=request.form['email']
    subject=request.form['subject']
    message=request.form['message']
    honey=request.form['honey']

    if honey:
        return jsonify({"success": False, "msg": "Sorry something bad happened. Try again"})
    else:
        send_email(name, email, subject, message)
        return jsonify({"success": True, "msg": "Your message has been successfully sent. We will get back to you as soon as possible."})

@public.app_errorhandler(404)
def page_not_found(e):
    return render_template('public/404.html'), 404

@public.app_errorhandler(400)
def expired(e):
    return jsonify({'success': False, 'msg': 'Error occured. Probably csrf token expired. Please refresh the page and try again!'})
