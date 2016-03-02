from app.models import Profile
from app import db
admin = Profile('admi', 'admin@example.com','21','M')
guest = Profile('g', 'gu','76','M')
# add and commit the new users to the database
db.session.add(admin)
db.session.add(guest)
db.session.commit()
