from app.classes.Database import Database
from app.classes.Upload import Upload
from app.models.User import User
from flask import session
from flask import current_app as flask_app
import uuid, time

class Image():

    def __init__(self):
        return None

    #gets a max of 20imgs from Firebase
    def get_images(self, limit=20):
        
        error = None
        images = False

        try:
            #gets images from database
            database = Database()
            images = database.get_images(limit)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else:
            return images
            # Return on success


    #gets a max of 20imgs per catagory
    def get_category_images(self, category, limit=20):
        
        error = None
        images = False
        
        try:
            #gets images from database
            database = Database()
            images = database.get_category_images(category, limit)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else:
            return images
            # Return on success

    #Gets images id's
    def get_image(self, image_id):
        
        error = None
        image = False
        
        try:
            #gets images from database
            database = Database()
            image = database.get_image(image_id)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else:
            return image
            # Return on success

    #deletes images
    def delete_image(self, image_id):
        
        error = None
        
        try:
            #request is made to database to delete image
            database = Database()
            database.delete_image(image_id)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else: 
            return
            # Return on success

    #gets a maxium of 20 images uploaded by the user
    def get_user_images(self, limit=20):
        
        error = None
        images = False
        user_id = False

        #gets session data, then fetches images uploaded by the user via localId
        if (session['user'] and session['user']['localId']):
            user_id = session['user']['localId']
        try:
            #makes database request
            database = Database()
            images = database.get_images(limit, user_id)

        except Exception as err:
            flask_app.logger.info(err)
            error = err

        if error:
            # Raise error from failed Firebase request
            raise Exception(error)
        else:
            return images
            # Return on success


    #Upload img script
    def upload(self, request):
        #Image data
        image_id        = str(uuid.uuid1())
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']

        # Validates required registration fields
        error = None
        user_id = False

        if (session['user'] and session['user']['localId']):
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        else: 
            error = 'You must be logged in to upload an image.'

        if 'image' not in request.files:
            error = 'A file is required.'
        else:
            file = request.files['image']

        if not error:
            #gives error if file hasnt been uploaded
            if file.filename == '':
                error = 'A file is required.'
            
            #gives error if name is not set
            elif not name:
                error = 'An name is required.'

            #gives error if description is not set
            elif not description:
                error = 'A description is required.'

            #gives error if category is not set
            elif not category:
                error = 'A category is required.'
            else:
                try:
                    uploader = Upload()
                    upload_location = uploader.upload(file, image_id)
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      '/' + upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           int(time.time())
                    }
                    database = Database()
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err:
                    error = err
        if error:
            # Raise error from failed Firebase request
            flask_app.logger.info('################ UPLOAD ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            return image_id
            # Return on success


    #Image update script
    def update(self, image_id, request):
        #Requests Image data
        name            = request.form['name']
        description     = request.form['description']
        category        = request.form['category']
        image_filter    = request.form['filter']
        created_at      = request.form['created_at'] 
        upload_location = request.form['upload_location']  

        # Validates required registration fields
        error = None
        user_id = False

        if (session['user'] and session['user']['localId']):
            user_id     = session['user']['localId']
            user_name   = session['user']['first_name'] + " " + session['user']['last_name']
            user_avatar = session['user']['avatar']
        else: 
            #gives error if not logged in
            error = 'You must be logged in to update an image.'

        if not error:
            #gives error if name is not set
            if not name:
                error = 'An name is required.'

            #gives error if description is not set
            elif not description:
                error = 'A description is required.'

            #gives error if category is not set
            elif not category:
                error = 'A category is required.'
            else:
                try:
                    image_data = {
                        "id":                   image_id,
                        "upload_location":      upload_location,
                        "user_id":              user_id,
                        "user_name":            user_name,
                        "user_avatar":          user_avatar,
                        "name":                 name,
                        "description":          description,
                        "category":             category,
                        "filter":               image_filter,
                        "created_at":           created_at
                    }
                    database = Database()
                    #saves updated image data
                    uploaded = database.save_image(image_data, image_id)
                except Exception as err:
                    error = err
        if error:
            # Raise error from failed Firebase request
            flask_app.logger.info('################ UPDATE ERROR #######################')
            flask_app.logger.info(error)
            raise Exception(error)
        else:
            return
            # Return on success
