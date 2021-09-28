import os
from flask import Blueprint, render_template, request, flash, redirect, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db

main = Blueprint('main', __name__)

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['mp4', 'png', 'jpg', 'jpeg', 'gif'])

# Content list TEST
content = ['test.gif', 'test.mp4', 'test.png']

# Playlist vars
playfile = './playlist.txt'
playlist = []
playlen = []
# include = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    global playlist, playlen

    # Check if playfile exists and init vars
    if os.path.isfile(playfile) and len(playlist) == 0:
        with open(playfile, 'r') as pl:
            for line in pl.readlines():
                playlist.append(line.split(',')[0])
                playlen.append(line.split(',')[1].rstrip('\n'))
        pl.close

    content = []

    for i in range(0, len(playlist)):
        content.append([playlist[i], playlen[i]])


    return render_template('index.html', content=content)

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

@main.route('/player', methods=['GET', 'POST'])
@login_required
def player():
    global playlist, playlen

    include = []

    # Write data from select fields of /player to playfile
    if request.method == 'POST':
        playlist = request.form.getlist('order')
        playlen = request.form.getlist('time')
        include = request.form.getlist('include')
        if os.path.isfile(playfile):
            os.remove(playfile)
        for i in range(0, len(playlist)):
            with open(playfile, 'a') as pl:
                pl.write('%s,%s\n' % (playlist[i], playlen[i]))
            pl.close
        # print(playlist)
        # print(playlen)
        print('Include:')
        print(include)
        if request.form.get('remfiles') == 'on':
            print('Deleting unused files...')
        for i in range(0, len(playlist)):
            print(playlist[i])
            print(playlen[i])
            if int(playlen[i]) > 0:
                return redirect('/')
            else:
                print('Failed')
        flash('Duration must exceed zero on selected content!')
        # return redirect('/')

    return render_template('player.html', content=content)