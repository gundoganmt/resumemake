from flask import render_template, Blueprint, request, Response, send_file, jsonify, redirect, url_for, abort
from flask_login import current_user
from resumemake.models import Users, Portfolios, UserMails, ResumeSite
import pdfkit
from resumemake import db
from utils import only_main, send_email
import requests

public = Blueprint('public',__name__)

@public.route('/')
def index():
    if request.host == '127.0.0.1:5000':
        return render_template('public/index.html')
    # else:
    #     blog_site = BlogSite.query.filter_by(domain=request.host).first()
    #     return render_template('preview/blogs/' + blog_site.template + '.html', blog_site=blog_site)


    #return render_template('public/index.html')
    #return redirect(url_for('.liveblog', site_name=blog_site.site_name))
    # elif request.host == 'www.jobby.net':
    #     user = Users.query.filter_by(domain=request.host).first()
    #     return render_template('preview/breezycv.html', user=user)
    # else:
    #     user = Users.query.filter_by(domain=request.host).first()
    #     return render_template('preview/breezycv.html', user=user)

@public.route('/preview/<template>')
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
def previewresume():
    site_id = request.args.get('site_id', str)
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first_or_404()
    return render_template('preview/resumes/ronaldo-rendered.html', resume_site=resume_site)

@public.route('/single-portfolio/<int:port_id>')
def singleport(port_id):
    port = Portfolios.query.filter_by(id=port_id).first()
    return render_template('preview/breezycv-single-port.html', port=port)

@public.route('/single-blog/<int:blog_id>')
def singleblog(blog_id):
    blog = BlogPosts.query.filter_by(id=blog_id).first()
    return render_template('blog/single-breezy-blog.html', blog=blog)

@public.route('/pdf')
def pdf():
    #config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    #rendered = render_template('preview/another.html')
    #pdf = pdfkit.from_url('127.0.0.1:5000/pdf1', False, configuration=config)

    #this could be used for proxy
    r = requests.get("", stream=True)
    # response = make_response()
    # if 'Content-Disposition' in r.headers:
    #     response.headers['Content-Disposition'] = r.headers['Content-Disposition'].replace("attachment;", "inline;")
    # response.data = r.content
    # response.headers['Content-Type'] = r.headers['Content-Type']


    return Response(r, headers={'Content-Disposition': 'attachment; ' 'filename=trial.mp4'})

@public.route('/pdf1')
def pdf1():
    return render_template('preview/another.html')

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
