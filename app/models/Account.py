from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session, flash
from flask import current_app as flask_app

class Account():

    def __init__(self):
        self.user = User()
        return None

    def register(self, request):
        """ 
        Registration method. 
    
        Processes POST request, and registers user in Firebase on success

        Parameters: 
            request (obj): The POST request object
    
        Raises: 
            error (Exception): Error from failed Firebase request
    
        """

        # Extract required fields from POST request
        email = request.form['email']
        password = request.form['password']
        password_confirm = request.form['password_confirm']

        # Validates required registration fields
        error = None
        if not email:
            error = 'An email is required.'
        elif not password:
            error = 'Password is required.'
        elif 6 > len(password):
            error = 'Your password must be at least 6 characters long.'
        elif not password_confirm:
            error = 'Password confirmation is required.'
        elif password != password_confirm:
            error = 'Password and password confirmation should match.'
        else:
            try:
                user_data = {
                    "localId": "",
                    "email": email,
                    "first_name": "",
                    "last_name": "",
                    "avatar": ""
                }
                # Attempt to process valid registration request
                database = Database()
                user_auth = database.register(user_data, password)
            except Exception as err:
                # Raise error from failed Firebase request
                error = err
        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else:
            # Return on success
            return
    
    #Login Request
    def login(self, request):
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']

            #If a email or password hasnt been provided error is provided.
            error = None
            if not email:
                error = 'An email is required.'
            elif not password:
                error = 'Password is required.'
            else:
                try:
                    #Sends request if email and password is provided
                    database = Database()
                    user = database.login(email, password)
                    # TODO Remove for production
                    #flask_app.logger.info(user)
                    self.user.set_user(user)
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
            # Raise error from failed Firebase request
        else:
            # Return on success
            return
    
    #update a users proflie
    def update(self, request):
        if request.method == 'POST':
            first_name = request.form['firstname']
            last_name = request.form['lastname']

            error = None
            #if a first or last name is not provided an error is sent.
            if not first_name:
                error = 'A first name is required.'
            elif not last_name:
                error = 'A last name is required.'
            else:
                if 'avatar' in request.files:
                    file = request.files['avatar']
                    if file.filename:
                        uploader = Upload()
                        avatar = uploader.upload(file, session['user']['localId'])
                        session['user']['avatar'] = "/" + avatar.strip("/")
                try:
                    session['user']['first_name'] = first_name
                    session['user']['last_name'] = last_name
                    database = Database()
                    user_auth = database.update_user(session['user'])
                    session.modified = True
                except Exception as err:
                    error = err

        if error:
            raise Exception(error)
            # Raise error from failed Firebase request
        else:
            # Return on success
            return

    #liking system
    def like(self, image_id, like, request):
                
        changed = False
        likes = session['user']['likes']

        #if a image is liked then the image will apear as liked even if the like was made in another session
        if like == 'true':
            if image_id not in likes:
                likes.append(image_id)
                changed = True
        else:
            #if not then 
            if image_id in likes:
                likes.remove(image_id)
                changed = True
        #Sends like data to database
        if changed:
            session['user']['likes'] = likes
            database = Database()
            database.update_user(session['user'])
            session.modified = True

        return changed
        
        #if a logout request is made, the user will be logged out
    def logout(self):
        self.user.unset_user()

