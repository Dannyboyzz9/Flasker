import os
from flask import Flask, flash, request, redirect, url_for
from flask import current_app as flask_app
from app import SITE_ROOT

class Upload():

    #Sets valid file types to png, jpg, jpeg and gif
    def __init__(self):
        self.extensions = {'png', 'jpg', 'jpeg', 'gif'}

    #If file type is png, jpg, jpeg, or gif the file will be saved as file_name.extension_name to the /static/uploads folder
    def upload(self, file, filename):
        allowed_extension = self.allowed_file(file.filename)
        if allowed_extension:
            fullname = filename + '.' + allowed_extension
            destination = os.path.join('static/uploads', fullname)
            file.save(os.path.join(SITE_ROOT, destination))
            return destination
        else:
            #sends a error message if above statment is false
            raise Exception("Only allowed filetypes: ".join(self.extensions.values()))

    def allowed_file(self, filename):
        #Makes sure code is in the correct format
        if ('.' in filename and filename.rsplit('.', 1)[1].lower() in self.extensions):
            return filename.rsplit('.', 1)[1].lower()
        return False