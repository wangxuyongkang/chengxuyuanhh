from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from app import db
import pymysql
from app.models.comment import MemberComments
pymysql.install_as_MySQLdb()
app = create_app('dev')
Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


import www

if __name__ == '__main__':
    
    manager.run()
