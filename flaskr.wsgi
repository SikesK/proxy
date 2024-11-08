#! /usr/bin/python
import sys

# WSGI needs the path to your application. Adding application folder to the PYTHONPATH
#sys.path.insert(0, '/var/www/blackboxexp/user_interface/')
#sys.path.append('/var/www/blackboxexp/user_interface/flaskr/')
#sys.path.append('/home/steve/PycharmProjects/blackBoxExp/user_interface/flaskr/')

sys.path.insert(0, '/Users/kelseysikes/Desktop/user_study_nbw/flaskr/')


from flaskr import create_app

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)
