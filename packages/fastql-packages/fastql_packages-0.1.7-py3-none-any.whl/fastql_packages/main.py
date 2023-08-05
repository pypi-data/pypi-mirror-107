import click
import requests
import os
from os import walk
import re
from zipfile import ZipFile
import shutil
import sys
from .modules import moduleIsNotExist, addModule, is_tool
from .lib import file_exists, load_environtment, file_exists_on_location
import inflect
import datetime
from jinja2 import Environment, FileSystemLoader
import errno
import secrets
import subprocess
from .packages import check_and_create_directory, create_database_config
lectEngine = inflect.engine()


jinja_loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
jinja_env = Environment(loader=jinja_loader)

@click.group()
def main():
    pass

@main.command()
@click.argument('query')
@click.option('--version', '-v', default=None)
def create(query, version):
    if os.path.exists(os.path.join(os.getcwd(), query)):
        click.secho('defined path/dir already exists',fg='red')
        click.secho('the current process is canceled',fg='red')
        return
    click.secho('On Request fastapigql info',fg='blue')
    if version == None:
        req_fastql_data = requests.get("https://api.github.com/repos/rachmanzz/fastapigql/releases/latest")
    else:
        req_fastql_data = requests.get("https://api.github.com/repos/rachmanzz/fastapigql/releases/tags/{}".format(version))
    
    # check if failed
    if req_fastql_data.status_code != 200:
        click.secho('download failed or version undefined', fg='red')
        return
    # get return json data
    reqJson = req_fastql_data.json()

    click.echo('please wait ....')
    click.secho('download resources in progress',fg='blue')
    
    get_zip_file = requests.get("https://github.com/rachmanzz/fastapigql/archive/refs/tags/{}.zip".format(reqJson['tag_name']))

    dispositionFile = get_zip_file.headers['content-disposition']
    filename_fastql = re.findall("filename=(.+)", dispositionFile)[0]


    click.echo('file on creating...')

    with open(os.path.join(os.getcwd(), filename_fastql), 'wb') as f:
        f.write(get_zip_file.content)
    
    # Retrieve HTTP meta-data

    # need make sure directory tm is not exits
    temporary_dir = os.path.join(os.getcwd(), '{}-temp'.format(query))

    click.secho('unzipping resources',fg='blue')
    with ZipFile(os.path.join(os.getcwd(), filename_fastql), 'r') as zipObj:
       # Extract all the contents of zip file in different directory
       zipObj.extractall(temporary_dir)
    
    _, dirnames, _ = next(walk(temporary_dir))
    click.echo('move resources ....')
    shutil.move(os.path.join(temporary_dir, dirnames[0]), os.path.join(os.getcwd(), query))
    click.echo('remove temporary directory ....')
    os.rmdir(temporary_dir)
    os.remove(filename_fastql)

    os.system("cd {} && fastql init".format(query))

    click.secho('=========done=======', fg='green')


@main.command()
@click.argument('query', type=click.Choice(['model', 'migration', 'serialize', 'mutation']))
@click.option('--name', default=None, type=str, required=True)
@click.option('--migration/--no-migration', '-m', default=False, type=bool)
@click.option('--table', '-t', default=None, type=str)
@click.option('--serialize/--no-serialize', '-s', default=False, type=bool)
@click.option('--all/--no-all', '-a', default=False, type=bool)
@click.option('--depend', '-d', type=str, required=False)
@click.option('--arg-key', type=str, required=False)
def make(query, name, migration, table, serialize, all, depend, arg_key):


    # make sure first character is UpperCase
    FirstCharUpperCase = name[0].upper() + name[1:]
    
    # split character to array
    SplitChar = re.findall('[A-Z][^A-Z]*', FirstCharUpperCase)

    if query == 'model':
        

        modelName = name.capitalize()
        modelFile = name.lower()

        
        # check length 
        if len(SplitChar) > 1:
            modelName = ''.join(SplitChar)
            modelFile = '_'.join(SplitChar).lower()

        

        model_template = jinja_env.get_template('model.fastql')

        model_output = model_template.render(modelName=modelName)
        current_model_location = os.path.join(os.getcwd(), 'models/', '{}.py'.format(modelFile))

        if file_exists(current_model_location):
            click.secho("file model already exist", fg="red")
            click.secho("the current process is canceled", fg="red")
            return

        check_and_create_directory(os.path.dirname(current_model_location))

        with open(current_model_location, "w") as f:
            f.write(model_output)
        click.secho("model created", fg="blue")

    if query == 'migration' or migration and query == 'model' or all and query == 'model':
        migrationName = lectEngine.plural(name.capitalize())
        migrationFile = lectEngine.plural(name.lower())
        tableName = lectEngine.plural(name.lower()) if table == None else table

        if len(SplitChar) > 1:
            migrationName = ''.join(SplitChar[:-1]) + lectEngine.plural(SplitChar[-1])
            if table == None:
                tableName = ('_'.join(SplitChar[:-1]) + "_" + lectEngine.plural(SplitChar[-1])).lower()
            migrationFile = ('_'.join(SplitChar[:-1]) + "_" + lectEngine.plural(SplitChar[-1])).lower()

        timeNow = datetime.datetime.now()
        extend_table_name = "_create_" + migrationFile + "_" + 'table' if table == None else "_" + migrationFile + "_" + 'table'
        migrationFileName = timeNow.strftime("%Y_%m_%d_%H%M%S") + extend_table_name


        migr_template = jinja_env.get_template('migration.fastql') if table == None else jinja_env.get_template('migration-table.fastql')
        migr_output = migr_template.render(table={'nameCapitalize': migrationName, 'nameLower': tableName})

        current_migr_location = os.path.join(os.getcwd(), 'migrations/', '{}.py'.format(migrationFileName))

        if file_exists(current_migr_location):
            click.secho("file migration already exist", fg="red")
            click.secho("the current process is canceled", fg="red")
            return

        check_and_create_directory(os.path.dirname(current_migr_location))

        with open(current_migr_location, "w") as f:
            f.write(migr_output)
        click.secho("migration created", fg="blue")

    if query == 'serialize' or serialize and query == 'model' or all and query == 'model':
        serializeName = name.capitalize()
        serializeFile = name.lower()
        
        if len(SplitChar) > 1:
            serializeName = ''.join(SplitChar)
            serializeFile = '_'.join(SplitChar).lower()

        serialize_template = jinja_env.get_template('serialize.fastql')

        serialize_output = serialize_template.render(modelName=serializeName)
        current_serialize_location = os.path.join(os.getcwd(), 'app/serializers/', '{}_serialize.py'.format(serializeFile))

        if file_exists(current_serialize_location):
            click.secho("file serialize model already exist", fg="red")
            click.secho("the current process is canceled", fg="red")
            return

        check_and_create_directory(os.path.dirname(current_serialize_location))

        with open(current_serialize_location, "w") as f:
            f.write(serialize_output)
        click.secho("serialize model created", fg="blue")
    if query == 'mutation':
        mutationName = name.capitalize()
        mutationFile = name.lower()
        
        if len(SplitChar) > 1:
            mutationName = ''.join(SplitChar)
            mutationFile = '_'.join(SplitChar).lower()

        mutation_packages = []
        

        mutation: dict = {
            'class_name': mutationName,
            'has_argument': False
        }
        

        if depend != None and arg_key != None:
            # make sure first character is UpperCase
            FirstSerialUpperCase = depend[0].upper() + depend[1:]
            
            # split character to array
            SplitSerial = re.findall('[A-Z][^A-Z]*', FirstSerialUpperCase)

            SerialName = depend.capitalize()
            SerialFile = depend.lower()

            if len(SplitSerial) > 1:
                SerialName = ''.join(SplitSerial)
                SerialFile = '_'.join(SplitSerial).lower()

            mutation.update({'has_argument': True})
            mutation.update({'serialize_name': SerialName})
            mutation.update({'arg_key': arg_key})
            mutation_packages.append('from app.serializers.{}_serialize import {}Model, {}GrapheneInputModel, {}GrapheneModel'.format(SerialFile, SerialName, SerialName, SerialName))
        
        mutation_template = jinja_env.get_template('mutation.fastql')
        mutation_output = mutation_template.render(mutation=mutation, packages= mutation_packages)
        current_mutation_location = os.path.join(os.getcwd(), 'app/mutations/', '{}_mutation.py'.format(mutationFile))

        check_and_create_directory(os.path.dirname(current_mutation_location))

        if file_exists_on_location(current_mutation_location):
            click.secho("file mutation already exist", fg="red")
            click.secho("the current process is canceled", fg="red")
            return

        with open(current_mutation_location, "w") as f:
            f.write(mutation_output)
        click.secho("mutation file created", fg="blue")

        if not file_exists('app/mutation_schema.py'):
            mutation_schema_packages = [
                'from app.mutations.{}_mutation import {}'.format(mutationFile, mutationName)
            ]
            mutation_schema_data = {
                'name': mutationFile,
                'class': mutationName
            }

            mutation_schema_template = jinja_env.get_template('mutation-schema.fastql')
            mutation_schema_output = mutation_schema_template.render(mutation=mutation_schema_data, packages=mutation_schema_packages)

            current_mutation_schema_location = os.path.join(os.getcwd(), 'app/mutation_schema.py')
            with open(current_mutation_schema_location, "w") as f:
                f.write(mutation_schema_output)
            click.secho("mutation schema created", fg="blue")
        


@main.command()
@click.option('--reload/--no-reload', '-r', default=False, type=bool)
def run_server(reload):
    if reload is None:
        os.system("uvicorn main:app")
    else:
         os.system("uvicorn main:app --reload")

@main.command()
@click.option('--rollback/--no-rollback', default=False, type=bool)
@click.option('--reset/--no-reset', default=False, type=bool)
@click.option('--status/--no-status', default=False, type=bool)
def migrate(rollback, reset, status):

    if not file_exists('.env'):
        click.secho("make sure to create .env file first", fg="red")
        click.echo("try to run fastql init")
        return

    

    if moduleIsNotExist('orator'):
        addModule('orator')

    create_database_config()

    if rollback:
        os.system('orator migrate:rollback -c configs/database.py')
    elif reset:
        os.system('orator migrate:reset -c configs/database.py')
    elif status:
        os.system('orator migrate:status -c configs/database.py')
    else:
        os.system('orator migrate -c configs/database.py')

@main.command()
def init():
    if not is_tool('poetry') and moduleIsNotExist('poetry'):
        os.system('pip install poetry')

    os.system('poetry init --python ">=3.6,<4/0"')
    environ_dict: dict = {}

    secret_key = secrets.token_hex(48)
    environ_dict.update({'secret_key': secret_key})

    db_init = click.prompt("do you want to initialize database config ?", type=click.Choice(['yes', 'no'], case_sensitive=False), default='no')
    db_driver = None
    if db_init.lower() == 'yes':
        db_driver = click.prompt('please enter database driver', type=click.Choice(['mysql', 'postgres', 'sqlite'], case_sensitive=False), default='sqlite')
        environ_dict.update({'db_driver': db_driver.lower()})
        
        if db_driver.lower() == 'sqlite':
            db_file = click.prompt('database file location', default='db/database.db', type=str)
            environ_dict.update({'db_file': db_file})
        if db_driver.lower() == 'mysql' or db_driver == 'postgres':
            db_host = click.prompt('database host:', default='localhost', type=str)
            db_name = click.prompt('database name:', default='fastapigql', type=str)
            db_user = click.prompt('database user:', default='root', type=str)
            db_pass = click.prompt('database password:', default='', type=str)
            environ_dict.update({
                'db_host': db_host,
                'db_name': db_name,
                'db_user': db_user,
                'db_password': db_pass
            })
        if db_driver.lower() == 'mysql':
            db_port = click.prompt('database port:', default=3306, type=int)
            environ_dict.update({'db_port': db_port})
        if db_driver.lower() == 'postgres':
            db_port = click.prompt('database port:', default=5432, type=int)
            environ_dict.update({'db_port': db_port})



    with open(os.path.join(os.getcwd(), '.env'), 'w') as env:
        for x in environ_dict:
            env.write("{}={}".format(x.upper(), environ_dict[x]))
            env.write("\n")


    if db_driver != None and db_driver != 'sqlite':
        create_database_config()
        db_install_driver = click.prompt("do you want to install database driver ?", type=click.Choice(['yes', 'no'], case_sensitive=False), default='no')
        if db_install_driver.lower() == 'yes':
            if db_driver.lower() == 'mysql':
                choose_db_driver = click.prompt("which database driver do you want to install?", type=click.Choice(['PyMySQL', 'mysqlclient'], case_sensitive=True), default='mysqlclient')
                addModule(choose_db_driver)
            if db_driver.lower() == 'postgres':
                addModule('psycopg2')

    click.secho('the project has been initialized', fg='blue')







    

        
        
        





        


        
        

    