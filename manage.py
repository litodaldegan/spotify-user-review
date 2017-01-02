from app import manager
# from scripts.load_data import LoadData
from flask_migrate import MigrateCommand


# manager.add_command('load', LoadData)
manager.add_command('db', MigrateCommand)
manager.run()
