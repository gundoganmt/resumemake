from flask import render_template, Blueprint, request, jsonify, redirect, url_for, abort, send_file
from flask_login import current_user, login_required
from utils import (crop_max_square, allowed_img_file, allowed_pdf_file,
    get_extension, UPLOAD_PROFILE_FOLDER, UPLOAD_SERVICE_FOLDER,
    UPLOAD_TESTI_FOLDER, UPLOAD_PORT_FOLDER, UPLOAD_BACK_FOLDER, UPLOAD_PDF_FOLDER)
from werkzeug.utils import secure_filename
from PIL import Image
from resumemake import db
from resumemake.models import (WorkExperiences, Educations,
    Courses, Skills, Languages, Services,
    Testimonials, Portfolios, PortFiles, ResumeSite)
import os, uuid, bleach, validators, dns.resolver

resume = Blueprint('resume',__name__)

@resume.route('/resume-create')
@login_required
def resumecreate():
    site_id = request.args.get('site_id', str)
    site_name = request.args.get('site_name', str)
    resume_site = ResumeSite.query.filter_by(site_id=site_id, site_name=site_name, owner=current_user).first_or_404()
    return render_template('resume/resume-create.html', resume_site=resume_site)

@resume.route('/basicinfo/<site_id>', methods=['POST'])
def basic_info(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    current_user.name = request.form['FirstName']
    current_user.surname = request.form['LastName']
    resume_site.email = request.form['email']
    resume_site.phone_number = request.form['phone']
    resume_site.tagline = request.form['tagline']
    resume_site.province = request.form['city']
    resume_site.birth_day = request.form['birth_day']
    resume_site.country = request.form['country']

    if 'file' in request.files:
        file = request.files['file']
        filename = file.filename
        if allowed_img_file(filename):
            filename = secure_filename(filename)
            unique_filename = str(uuid.uuid4())+get_extension(filename)
            resume_site.profile_picture = unique_filename
            file.save(os.path.join(UPLOAD_PROFILE_FOLDER, unique_filename))
    db.session.commit()
    return jsonify({"success": True, "current_field": "b"})

@resume.route('/introduction/<site_id>', methods=['POST'])
def introduction(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    resume_site.introduction = request.form['introduction']
    resume_site.intro_title = request.form['intro_title']
    db.session.commit()
    return jsonify({"success": True, "current_field": "i"})

@resume.route('/social/<site_id>', methods=['POST'])
@login_required
def social(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    resume_site.twitter = request.form['twitter']
    resume_site.facebook = request.form['facebook']
    resume_site.instagram = request.form['instagram']
    resume_site.github = request.form['github']
    resume_site.youtube = request.form['youtube']
    resume_site.linkedin = request.form['linkedin']

    db.session.commit()
    return jsonify({"success": True, "current_field": "so"})

@resume.route('/workExp/<site_id>', methods=['POST'])
@login_required
def workExp(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()

    position = request.form['position']
    company = request.form['company']
    start_month = request.form['start_month_job']
    start_year = request.form['start_year_job']
    end_month = request.form['end_month_job']
    end_year = request.form['end_year_job']
    description = request.form['desc_work']

    workExp = WorkExperiences(position=position, company=company, start_month=start_month, 
        start_year=start_year, end_month=end_month, end_year=end_year,
        description=description, resume_id=resume_site.id)

    db.session.add(workExp)
    db.session.commit()

    context = {
        "success": True, 
        "current_field": 'w', 
        'workExp_id': workExp.id, 
        "position": position,
        "company": company,
        "duration": start_month + " " + str(start_year) + " - " + end_month + " " + str(end_year)
    }

    return jsonify(context)

@resume.route('/service/<site_id>', methods=['POST'])
def service(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first_or_404()
    service = Services(service_name=request.form['service_name'], 
        description=request.form['desc_service'], 
        resume_id=resume_site.id, picture=request.form['service_icon']
        )
    
    db.session.add(service)
    db.session.commit()
    return jsonify({"success": True, "current_field": "se", "service_id": service.id, "service_name": service.service_name})

@resume.route('/portfolio/<site_id>', methods=['POST'])
def portfolio(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    port = Portfolios(project_name=request.form['project_name'], website=request.form['website'],
        creation_time=request.form['creation_time'], tag=request.form['tag'],
        description=request.form['desc_port'], resume_id=resume_site.id)
    db.session.add(port)
    db.session.commit()

    for i in range(int(request.form['ins'])):
        key = 'port_pics' + str(i)
        if key in request.files:
            file = request.files[key]
            filename = file.filename
        if file and allowed_img_file(filename):
            filename = secure_filename(filename)
            unique_filename = str(uuid.uuid4())+get_extension(filename)
            port_files = PortFiles(filename=unique_filename, port_files_id=port.id)
            file.save(os.path.join(UPLOAD_PORT_FOLDER, unique_filename))
            db.session.add(port_files)

    db.session.commit()

    context = {
        "success": True, 
        "current_field": "p", 
        "port_id": port.id, 
        "project_name": port.project_name
    }

    return jsonify(context)

@resume.route('/testimonials/<site_id>', methods=['POST'])
def testimonials(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()

    testi = Testimonials(name=request.form['name'], company=request.form['company'],
        description=request.form['desc_testi'], resume_id=resume_site.id)

    if 'testi_pic' in request.files:
        file = request.files['testi_pic']
        filename = file.filename
    if file and allowed_img_file(filename):
        filename = secure_filename(filename)
        unique_filename = str(uuid.uuid4())+get_extension(filename)
        testi.picture = unique_filename
        image = Image.open(file)
        i = crop_max_square(image).resize((300, 300), Image.LANCZOS)
        i.save(os.path.join(UPLOAD_TESTI_FOLDER, unique_filename), quality=95)

    db.session.add(testi)
    db.session.commit()

    context = {
        "success": True, 
        "current_field": "t", 
        "testi_id": testi.id, 
        "name": testi.name, 
        "company": testi.company
    }

    return jsonify(context)

@resume.route('/edu/<site_id>', methods=['POST'])
@login_required
def edu(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()

    field = request.form['field']
    school = request.form['school']
    start_month = request.form['start_month_edu']
    start_year = request.form['start_year_edu']
    end_month = request.form['end_month_edu']
    end_year = request.form['end_year_edu']
    description = request.form['desc_edu']

    edu = Educations(field=field, school=school, start_month=start_month, 
        start_year=start_year, end_month=end_month, end_year=end_year,
        description=description, resume_id=resume_site.id)

    db.session.add(edu)
    db.session.commit()

    context = {
        "success": True,
        "current_field": 'e',
        "edu_id": edu.id,
        "field": field,
        "school": school,
        "duration": start_month + " " + str(start_year) + " - " + end_month + " " + str(end_year)
    }

    return jsonify(context)

@resume.route('/course/<site_id>', methods=['POST'])
@login_required
def course(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    course = Courses(course_name=request.form['course_name'], institution=request.form['institution'],
        start_month=request.form['start_month_course'], start_year=request.form['start_year_course'],
        end_month=request.form['end_month_course'], end_year=request.form['end_year_course'],
        description=request.form['desc_course'], resume_id=resume_site.id)
    db.session.add(course)
    db.session.commit()
    return jsonify({"success": True, "current_field": 'c', 'course_id': course.id, "course_name": course.course_name,
        "institution": course.institution, "duration": course.start_month + " " + str(course.start_year) + " - " + course.end_month + " " + str(course.end_year)})

@resume.route('/skill/<site_id>', methods=['POST'])
@login_required
def skill(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()

    skill = request.form['skill']
    level = request.form['level']
    category = request.form['category']

    if not skill or not category:
        return jsonify({'success': False, 'msg': 'Please enter valid values'})
    
    if int(level) > 100 or int(level) < 1:
        return jsonify({'success': False, 'msg': 'Level should be between 0 and 100'})
    
    if Skills.query.filter_by(skill=skill, resume_id=resume_site.id).first():
        return jsonify({'success': False, 'msg': 'You already have this skill'})

    skill = Skills(skill=skill, level=level, category=category, resume_id=resume_site.id)
    db.session.add(skill)
    db.session.commit()

    context = {
        "success": True,
        "current_field": "s",
        "skill_id": skill.id,
        "skill": skill.skill,
        "level": skill.level,
        "category": skill.category
    }

    return jsonify(context)

@resume.route('/language/<site_id>', methods=['POST'])
@login_required
def language(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    lang = Languages(language=request.form['lang'], level=request.form['level'], resume_id=resume_site.id)
    db.session.add(lang)
    db.session.commit()
    return jsonify({"success": True, "current_field": "l", "lang_id": lang.id, "lang": lang.language, "level": lang.level})

@resume.route('/connect_resume_domain/<site_id>', methods=['POST'])
@login_required
def connect_domain(site_id):
    site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    domain = request.form['domain']
    if not validators.url("https://" + domain):
        return jsonify({"success": False})
    site.domain = domain
    db.session.commit()
    return jsonify({"success": True})

@resume.route('/check_dns_status/<site_id>')
@login_required
def check_dns_status(site_id):
    site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    domain = site.domain
    resolver = dns.resolver.Resolver(); 
    try:
        answer = resolver.query(domain , "A")
    except:
        return jsonify({'success': False, 'msg': 'Cannot resolve dns information of this domain. Check your spelling.'})
    for item in answer:
        resultant_str = item.to_text()

    if resultant_str == '46.101.5.43':
        return jsonify({'success': True})

    return jsonify({'success': False, 'msg': 'Updating dns records takes some time to propagate. Come back later!'})
    
@resume.route('/site_settings/<site_id>', methods=['POST'])
@login_required
def site_settings(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    if not resume_site:
        return jsonify({'success': False, 'msg': "Some thing went wrong! Refresh the page."})
    else:
        if 'background_image' in request.files:
            file = request.files['background_image']
            filename = file.filename
            if allowed_img_file(filename):
                filename = secure_filename(filename)
                unique_filename = str(uuid.uuid4())+get_extension(filename)
                resume_site.background_picture = unique_filename
                file.save(os.path.join(UPLOAD_BACK_FOLDER, unique_filename))
            else:
                return jsonify({'success': False, 'msg': "invalid file extension. Allowed jpeg, jpg, png"})

        if 'pdf_resume' in request.files:
            file = request.files['pdf_resume']
            filename = file.filename
            if allowed_pdf_file(filename):
                filename = secure_filename(filename)
                unique_filename = str(uuid.uuid4())+get_extension(filename)
                resume_site.pdf_resume = unique_filename
                file.save(os.path.join(UPLOAD_PDF_FOLDER, unique_filename))
            else:
                return jsonify({'success': False, 'msg': "invalid file extension. Allowed pdf, doc, docx"})


        if request.form['contact_notify'] == 'true':
            resume_site.contact_email_notif = True
        else:
            resume_site.contact_email_notif = False

        if request.form['download_notify'] == 'true':
            resume_site.download_resume_notif = True
        else:
            resume_site.download_resume_notif = False

        db.session.commit()
        return jsonify({"success": True, "current_field": "ss"})

@resume.route('/deleteItem/<site_id>', methods=['POST'])
@login_required
def deleteItem(site_id):
    resume_site = ResumeSite.query.filter_by(site_id=site_id, owner=current_user).first()
    data = request.get_json(force=True)
    itemType, itemId = data['type_id'].split('_')
    if itemType == 'w':
        item = WorkExperiences.query.filter_by(id=itemId).first()
        if resume_site.id == item.resume_id:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"success": True, "current_field": "w"})
        else:
            return jsonify({"success": False})
    elif itemType == 'e':
        item = Educations.query.filter_by(id=itemId).first()
        if resume_site.id == item.resume_id:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"success": True, "current_field": "e"})
        else:
            return jsonify({"success": False})
    elif itemType == 'c':
        item = Courses.query.filter_by(id=itemId).first()
        if resume_site.id == item.resume_id:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"success": True, "current_field": "c"})
        else:
            return jsonify({"success": False})
    elif itemType == 's':
        item = Skills.query.filter_by(id=itemId).first()
        if resume_site.id == item.resume_id:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"success": True, "current_field": "s"})
        else:
            return jsonify({"success": False})
    elif itemType == 'l':
        item = Languages.query.filter_by(id=itemId).first()
        if resume_site.id == item.resume_id:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"success": True, "current_field": "l"})
        else:
            return jsonify({"success": False})
    elif itemType == 'se':
        item = Services.query.filter_by(id=itemId).first()
        if resume_site.id == item.resume_id:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"success": True, "current_field": "se"})
        else:
            return jsonify({"success": False})
    elif itemType == 't':
        item = Testimonials.query.filter_by(id=itemId).first()
        if resume_site.id == item.resume_id:
            os.remove(os.path.join(UPLOAD_TESTI_FOLDER, item.picture))
            db.session.delete(item)
            db.session.commit()
            return jsonify({"success": True, "current_field": "t"})
        else:
            return jsonify({"success": False})
    elif itemType == 'p':
        item = Portfolios.query.filter_by(id=itemId).first()
        if resume_site.id == item.resume_id:
            portfiles = PortFiles.query.filter_by(port_files_id=item.id).all()
            for portfile in portfiles:
                os.remove(os.path.join(UPLOAD_PORT_FOLDER, portfile.filename))
            db.session.delete(item)
            db.session.commit()
            return jsonify({"success": True, "current_field": "p"})
        else:
            return jsonify({"success": False})

@resume.route('/download/<filename>')
def download(filename):
    path = os.path.join(UPLOAD_PDF_FOLDER, filename)
    return send_file(path, as_attachment=True)