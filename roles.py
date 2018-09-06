import logging
from models.database import db, Roles

admin = Roles(name='admin', description='Admin Role')
staff = Roles(name='staff', description='Regular Role')

def InitRoles():
	print Roles.query.filter_by(name=admin).first()
	if Roles.query.filter_by(name=admin).first() == 'None':
		logging.info("Creating admin role")
		db.session.add(admin)
		db.session.commit()

	if Roles.query.filter_by(name=staff).first() == 'None':
		logging.info("Creating staff role")
		db.session.add(staff)
		db.session.commit()
