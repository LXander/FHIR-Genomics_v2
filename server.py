import subprocess
from argparse import ArgumentParser
from multiprocessing import cpu_count

from config import APP_CONFIG,HOST
from fhir import db,create_app




# use this for WSGI server
# e.g. `$ gunicorn server:app`

app = create_app(APP_CONFIG)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

def clear_db(app):
    '''
    Wipes the database associated with the app.
    '''
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == '__main__':
    arg_parser = ArgumentParser()
    arg_parser.add_argument('option', nargs='?', default='run', choices=('run', 'clear'))
    arg_parser.add_argument('-d', '--debug', action='store_true')
    args = arg_parser.parse_args()
    if args.option == 'run':
        if args.debug == True:
            #app.run(debug=True)
            app.run(port=2048, debug=True)
        else:
            num_workers = cpu_count() * 2 + 1
            subprocess.call('gunicorn -w %d -b %s -D server:app --log-level error --log-file fhir.log'% (num_workers, HOST), shell=True)
    elif args.option == 'clear':
        clear_db(app)
