"""
程序启动入口
"""

from app_api_1_0 import app_create, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = app_create('default')
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
