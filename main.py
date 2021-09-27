import os
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db

main = Blueprint('main', __name__)

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['mp4', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                flash('File(s) successfully uploaded')

            else:
                flash('File type not accepted!')

        return render_template('upload.html', name=current_user.name)
    else:
        return render_template('upload.html', name=current_user.name)

@main.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@main.route('/player')
def player():
    return render_template('player.html')