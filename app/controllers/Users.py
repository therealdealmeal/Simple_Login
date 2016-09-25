"""
    Sample Controller File

    A Controller should be in charge of responding to a request.
    Load models to interact with the database and load views to render them to the client.

    Create a controller using this template
"""
from system.core.controller import *

class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        self.load_model('User')
        self.db = self._app.db



    def index(self):

        return self.load_view('index.html')


    def success(self):
        return self.load_view('success.html')


    def create(self):

        user_info = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'pw_hash': request.form['pw_hash']
        }

        create_status = self.models['User'].create_user(user_info)
        if create_status['status'] == True:
            session['id'] = create_status['user']['id']
            session['first_name'] = create_status['user']['first_name']
            return self.load_view('success.html')
        else:
            for message in create_status['errors']:
                flash(message, 'regis_errors')
            return redirect('')


    def login(self):
        data = {
            'email': request.form['email'],
            'password': request.form['password']
            }
        login_status = self.models['User'].login_user(data)
        if login_status["status"] == True:
            print login_status
            session['id'] = login_status['user']['id']
            return redirect('/success')

        return redirect('/')


    def logout(self):
        session.pop('id', None)
        session.pop('first_name', None)
        return redirect('/')
