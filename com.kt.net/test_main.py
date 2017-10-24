from flask import Flask
from flask_restful import Api

from PLTEConnector import PLTEConnector
from ServiceClass import Departments_Meta, Departments_Meta2
from ServiceClass2 import Departmental_Salary

#Create a engine for connecting to SQLite3.
app = Flask(__name__)
api = Api(app)

PLTEConnector.getInstance()
PLTEConnector.getInstance().sendMessage("Command",2)

 
api.add_resource(Departmental_Salary, '/dept/<string:department_name>')
api.add_resource(Departments_Meta, '/departments/<string:department_name>/<int:abc>')
api.add_resource(Departments_Meta2,'/departments/')

# def http_error_handler(error):
#     #return flask.render_template('error.html', error=error), error.code
#     return error, error.code
# 
# for error in (401, 404, 500): # or with other http code you consider as error
#     app.error_handler_spec[None][error] = http_error_handler

if __name__ == '__main__':
    app.run(threaded=True)