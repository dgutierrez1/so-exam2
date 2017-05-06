import json, time
from flask import Flask, abort, request
from flask_restplus import Resource, Api
from flask_restplus import fields, reqparse
from database import db
from check_subprocess import activate_httpd, run_process, stop_process, get_process_status, all_checks_query, cpu_query, inactivate_httpd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/check_user/repositories/parcial2/so-exam2/A00320176-DanielGutierrez/check_persistence.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

api = Api(app,version='1.0', title='API for system checks defrief', description='Flask RestPlus powered API for reading results of a python process checking system data(CPU usage percent, memory usage, disk usage, httpd service status ) and inserting it into a SQlite database ')


ns = api.namespace('v1.0/checks', description='Operations related to system checks')

@ns.route('/')
class CheckCollection(Resource):

    @api.response(200, 'List of checks successfully returned.')
    def get(self):
        """ returns a list of checks """
        list = all_checks_query()
        return (list), 200

    @api.response(201, 'Not aplicable.')
    def post(self):
        """ Not aplicable """
        return "Not aplicable ", 501 # Not found

    @api.response(501, 'Not aplicable .')
    def put(self):
        """ Not aplicable  """
        return "Not aplicable ", 501 # Not found

    @api.response(501, 'Not aplicable .')
    def delete(self):
        """ Not aplicable  """
        return "Not aplicable ", 501 # Not found


@ns.route('/start')
class Start(Resource):

    @api.response(200, 'Process started')
    def get(self):
    	run_process()
        #time.sleep(2)
        status = get_process_status()
        if(status):
            return "Checks subprocess successfully started", 200
        else:
            return "Error while starting checks subprocess", 400

@ns.route('/stop')
class Stop(Resource):

    @api.response(200, 'Process stopped')
    def get(self):
    	stop_process()
        #time.sleep(2)
        status = get_process_status()
        if not status:
            return "Checks subprocess successfully stopped", 200
        else:
            return "Error while stopping checks subprocess", 400


@ns.route('/cpu/history/')
class CpuCollection(Resource):

    @api.response(200, 'List of cpu checks of specified size')
    @api.doc(params={'size': 'CPU history size'})
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('size', type=int, help='Size cannot be converted')
        args = parser.parse_args()
        list = cpu_query(args.size)
        return list, 200

@ns.route('/start/httpd')
class HppdStart(Resource):

    @api.response(200, 'HTTPD Process started')
    def get(self):
    	activate_httpd()
        return "HTTPD subprocess successfully started", 200


@ns.route('/stop/httpd')
class HppdStop(Resource):

    @api.response(200, 'HTTPD Process started')
    def get(self):
    	inactivate_httpd()
        return "HTTPD subprocess successfully stopped", 200



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug='True')
