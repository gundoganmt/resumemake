from resumemake import create_app
from flask_admin import Admin
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask import abort
from resumemake.models import (Users, ResumeSite,
    WorkExperiences, Educations,
    Courses, Skills, Languages, Services,
    Testimonials, Portfolios, PortFiles,
    UserMails, Notifications)

from resumemake import db

class MyModelView(sqla.ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return abort(404), 404

        if current_user.is_authenticated:
            return True

        return abort(404), 404

    # can_edit = True
    edit_modal = True
    create_modal = True
    can_export = True
    can_view_details = True
    details_modal = True

app = create_app()
admin = Admin(app, name='resumemake', template_mode='bootstrap3')
admin.add_view(MyModelView(Users, db.session))
admin.add_view(MyModelView(ResumeSite, db.session))
admin.add_view(MyModelView(Notifications, db.session))
admin.add_view(MyModelView(WorkExperiences, db.session))
admin.add_view(MyModelView(Services, db.session))
admin.add_view(MyModelView(Educations, db.session))
admin.add_view(MyModelView(Courses, db.session))
admin.add_view(MyModelView(Skills, db.session))
admin.add_view(MyModelView(Languages, db.session))
admin.add_view(MyModelView(Testimonials, db.session))
admin.add_view(MyModelView(Portfolios, db.session))
admin.add_view(MyModelView(PortFiles, db.session))
admin.add_view(MyModelView(UserMails, db.session))

if __name__ == '__main__':
    app.run(debug=True)
