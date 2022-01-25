from flask_login import UserMixin
from resumemake import db
from sqlalchemy import or_
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json

class Users(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=True)
    name = db.Column(db.String(50), nullable=True, default="")
    surname = db.Column(db.String(50), nullable=True, default="")
    email = db.Column(db.String(50), unique=True, nullable=False)
    profile_picture = db.Column(db.String(80), nullable=True, default="guest.jfif")
    account_desc = db.Column(db.Text, default="")
    password = db.Column(db.String(80))
    email_approved = db.Column(db.Boolean, default=False)
    setting_completed = db.Column(db.Boolean, default=False)
    member_since = db.Column(db.DateTime)
    twitter = db.Column(db.String(100), nullable=True, default="")
    facebook = db.Column(db.String(100), nullable=True, default="")
    instagram = db.Column(db.String(100), nullable=True, default="")
    github = db.Column(db.String(100), nullable=True, default="")
    youtube = db.Column(db.String(100), nullable=True, default="")
    linkedin = db.Column(db.String(100), nullable=True, default="")
    not_to = db.relationship('Notifications', foreign_keys='Notifications.not_to', backref='notification_to', cascade='all, delete-orphan')
    mailed = db.relationship('UserMails', backref='mailed', cascade='all, delete-orphan', lazy='dynamic')
    resumes = db.relationship('ResumeSite', backref='owner', cascade='all, delete-orphan', lazy='dynamic')

    def full_name(self):
        return self.name + " " + self.surname

    def new_notifications(self):
        return Notifications.query.filter_by(notification_to=self, seen=False).all()

    def num_not(self):
        return Notifications.query.filter_by(notification_to=self, seen=False).count()

    def all_notifications(self):
        return Notifications.query.filter_by(notification_to=self).all()

    def get_confirmation_token(self, expires_sec=1800):
        s = Serializer("qazxswedcvfrtgb", expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_confirmation_token(token):
        s = Serializer("qazxswedcvfrtgb")
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Users.query.get(user_id)

    def get_mails(self):
        return UserMails.query.filter_by(user_id=self.id).all()

    def sites(self):
        return ResumeSite.query.filter_by(user_id=self.id).all()

    def __repr__(self):
        return self.username

class ResumeSite(db.Model):
    __tablename__ = "ResumeSite"
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(50), nullable=False)
    site_id = db.Column(db.String(80), nullable=False, unique=True)
    profile_picture = db.Column(db.String(80), nullable=True, default="blank.png")
    background_picture = db.Column(db.String(80), nullable=True, default='bg-sunshine.jpg')
    pdf_resume = db.Column(db.String(80), nullable=True)
    contact_email_notif = db.Column(db.Boolean, default=False)
    download_resume_notif = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(50), nullable=True, default="")
    birth_day = db.Column(db.String(50), nullable=True, default="")
    country = db.Column(db.String(50), nullable=True, default="")
    introduction = db.Column(db.Text, default="")
    creation_time = db.Column(db.DateTime, default=datetime.utcnow)
    current_plan = db.Column(db.String(25), nullable=True, default="draft")
    intro_title = db.Column(db.String(150), nullable=True, default="")
    province = db.Column(db.String(25), nullable=True, default="")
    tagline = db.Column(db.String(80), nullable=True, default="")
    phone_number = db.Column(db.String(15), nullable=True, default="")
    domain = db.Column(db.String(50), nullable=True, default="")
    template = db.Column(db.String(50), nullable=True, default="")
    twitter = db.Column(db.String(100), nullable=True, default="")
    facebook = db.Column(db.String(100), nullable=True, default="")
    instagram = db.Column(db.String(100), nullable=True, default="")
    github = db.Column(db.String(100), nullable=True, default="")
    youtube = db.Column(db.String(100), nullable=True, default="")
    linkedin = db.Column(db.String(100), nullable=True, default="")
    notification = db.relationship('Notifications', backref='notedResume', cascade='all, delete-orphan')
    work_experience = db.relationship('WorkExperiences', backref='Worker', cascade='all, delete-orphan')
    educations = db.relationship('Educations', backref='student', cascade='all, delete-orphan')
    skills = db.relationship('Skills', backref='Skilled', cascade='all, delete-orphan')
    langs = db.relationship('Languages', backref='speak', cascade='all, delete-orphan')
    serv = db.relationship('Services', backref='server', cascade='all, delete-orphan', lazy='dynamic')
    testi = db.relationship('Testimonials', backref='testimo', cascade='all, delete-orphan', lazy='dynamic')
    port = db.relationship('Portfolios', backref='portfos', cascade='all, delete-orphan', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def workExps(self):
        return WorkExperiences.query.filter_by(resume_id=self.id).all()

    def edus(self):
        return Educations.query.filter_by(resume_id=self.id).all()

    def courses(self):
        return Courses.query.filter_by(resume_id=self.id).all()

    def skills(self):
        return Skills.query.filter_by(resume_id=self.id).all()

    def langs(self):
        return Languages.query.filter_by(resume_id=self.id).all()

    def services(self):
        return Services.query.filter_by(resume_id=self.id).all()

    def testimos(self):
        return Testimonials.query.filter_by(resume_id=self.id).all()

    def ports(self):
        return Portfolios.query.filter_by(resume_id=self.id).all()

    def get_port_tags(self):
        return db.session.query(Portfolios.tag).filter_by(resume_id=self.id).distinct().all()
    
    def get_port_from_tag(self, tag):
        return Portfolios.query.filter_by(resume_id=self.id, tag=tag).all()

    def unique_sk_category(self):
        category = []
        for sk in self.skills():
            if sk.category not in category:
                category.append(sk.category)
        return category

    def get_skills_by_cat(self, category):
        return Skills.query.filter_by(category=category, resume_id=self.id).all()

    def basic_exists(self):
        if self.email or self.phone_number or self.birth_day or self.country or self.province or self.introduction:
            return True
        return False

    def __repr__(self):
        return self.site_name

class Notifications(db.Model):
    __tablename__ = 'Notifications'
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('ResumeSite.id'))
    not_to = db.Column(db.Integer, db.ForeignKey('Users.id'))
    not_type = db.Column(db.Integer)
    seen = db.Column(db.Boolean, default=False)

class WorkExperiences(db.Model):
    __tablename__ = "WorkExperiences"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(25), nullable=True)
    start_month = db.Column(db.String(20), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_month = db.Column(db.String(20), nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('ResumeSite.id'))

    def __repr__(self):
        return self.position

class UserMails(db.Model):
    __tablename__ = "UserMails"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

    def __repr__(self):
        return self.subject

class Services(db.Model):
    __tablename__ = 'Services'
    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('ResumeSite.id'))

    def __repr__(self):
        return self.service_name

class Portfolios(db.Model):
    __tablename__ = 'Portfolios'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(150), nullable=True)
    tag = db.Column(db.String(150), nullable=False)
    creation_time = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('ResumeSite.id'))
    port_files = db.relationship('PortFiles', backref='portf', cascade='all, delete-orphan')

    def portpic(self):
        portpic = PortFiles.query.filter_by(port_files_id=self.id).first()
        return portpic.filename

    def portpics(self):
        filenames = []
        portpics = PortFiles.query.filter_by(port_files_id=self.id).all()
        for portpic in portpics:
            filenames.append(portpic.filename)
        return filenames

    def __repr__(self):
        return self.project_name

class PortFiles(db.Model):
    __tablename__ = 'PortFiles'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(80), nullable=True)
    port_files_id = db.Column(db.Integer, db.ForeignKey('Portfolios.id'))

    def __repr__(self):
        return self.filename

class Testimonials(db.Model):
    __tablename__ = 'Testimonials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    company = db.Column(db.String(50), nullable=False)
    picture = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('ResumeSite.id'))

    def __repr__(self):
        return self.name

class Educations(db.Model):
    __tablename__ = "Educations"
    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(100), nullable=False)
    school = db.Column(db.String(100), nullable=False)
    start_month = db.Column(db.String(20), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_month = db.Column(db.String(20), nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('ResumeSite.id'))

    def __repr__(self):
        return self.field

class Courses(db.Model):
    __tablename__ = "Courses"
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    start_month = db.Column(db.String(20), nullable=False)
    start_year = db.Column(db.Integer, nullable=False)
    end_month = db.Column(db.String(20), nullable=False)
    end_year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('ResumeSite.id'))

    def __repr__(self):
        return self.course_name

class Skills(db.Model):
    __tablename__ = 'Skills'
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(50), nullable=True, default="My")
    resume_id = db.Column(db.Integer, db.ForeignKey('ResumeSite.id'))

    def __repr__(self):
        return self.skill

class Languages(db.Model):
    __tablename__ = 'Languages'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String(50), nullable=False)
    level = db.Column(db.String(50), nullable=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('ResumeSite.id'))

    def __repr__(self):
        return self.language
