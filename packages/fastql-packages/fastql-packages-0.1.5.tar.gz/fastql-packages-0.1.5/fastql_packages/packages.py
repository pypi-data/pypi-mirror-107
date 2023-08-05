import os
import errno
from .lib import file_exists
from jinja2 import Environment, FileSystemLoader
from .lib import load_environtment
import click

jinja_loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
jinja_env = Environment(loader=jinja_loader)

def create_init_file(fullpath):
    if not file_exists(os.path.join(fullpath, '__init__.py')):
        with open(os.path.join(fullpath, '__init__.py'), 'w') as bf:
            pass
def check_and_create_directory(fullpath):
    if not os.path.exists(fullpath):
        try:
            os.makedirs(fullpath)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    create_init_file(fullpath)

def create_database_config():
    if os.path.exists(os.path.join(os.getcwd(), 'app')):
            load_environtment()
            db_driver = os.getenv("DB_DRIVER", None)
            print("env load ")
            print("db driver {}".format(db_driver))
            if db_driver is None:
                click.secho("database data environment not found", fg="red")
                return 
            if db_driver == 'mysql' or db_driver == 'postgres':
                db_config_data = {
                    'dbdriver': db_driver,
                    'dbport': 3306 if db_driver == 'mysql' else 5432
                }
                check_and_create_directory(os.path.join(os.getcwd(), 'configs'))
                db_config_temp = jinja_env.get_template('config-db.fastql')
                db_config_output = db_config_temp.render(configs=db_config_data)

                set_location = os.path.join(os.getcwd(), 'configs/database.py')
                check_and_create_directory(os.path.dirname(set_location))

                with open(set_location, "w") as fr:
                    fr.write(db_config_output)
        
    else:
        click.secho("database configs unable to create, please make sure location of project is on root directory", fg="red")

        