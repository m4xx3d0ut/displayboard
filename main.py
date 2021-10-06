import os
from shutil import move
from flask import Blueprint, render_template, request, flash, redirect, current_app, url_for, session
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import db

main = Blueprint('main', __name__)

# List of allowed extensions and function to validate
valid_f_ext = set(['mp4', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in valid_f_ext

# Playlist vars
playfile = './playlist.txt'
playlist = []
playlen = []
# Static files
static = '%s/displayboard/static/' % (os.getcwd())
content = '%scontent/' % (static)

# Content list
content = os.listdir(content)
global dur_list
global asset_list

# Base URL for dynamic pages
base_url = 'http://192.168.254.153'


"""
The app home page displays currently set playlist and sets variables for
the /player/play slideshow function.  Available without login to view current
playlist.
"""
@main.route('/', methods=['GET', 'POST'])
def index():
    global playlist, playlen, content, dur_list, asset_list

    # asset_list = session['asset_list']
    # dur_list = session['dur_list']

    is_admin = False

    if current_user.is_authenticated:
        permissions = current_user.permissions
        if permissions == 'admin':
            is_admin = True

    if request.method == 'POST':
        if request.form['now_playing']:
            return redirect('/player/play')

    # Set variables for slideshow function
    def play_data(url, pl_line, redir_len):
        global dur_list, asset_list

        # asset_list = session['asset_list']
        # dur_list = session['dur_list']

        asset = pl_line[0]
        dur_url = pl_line[1]
        if int(dur_url) > 0:
            asset_list.append(asset)
            dur_list.append(dur_url)

        session['dur_list'] = dur_list
        session['asset_list'] = asset_list

    # Check if playfile exists and init vars
    if os.path.isfile(playfile) and len(playlist) == 0:
        with open(playfile, 'r') as pl:
            for line in pl.readlines():
                playlist.append(line.split(',')[0])
                playlen.append(line.split(',')[1].rstrip('\n'))
        session['playlist'] = playlist
        session['playlen'] = playlen

        pl.close

    plcontent = []
    dur_list = []
    asset_list = []

    for i in range(0, len(playlist)):
        if playlist[i] in content:
            if int(playlen[i]) > 0:
                plcontent.append([playlist[i], playlen[i]])

    for i in range(0, len(plcontent)):
        play_data(i, plcontent[i], len(plcontent))

    session['dur_list'] = dur_list
    session['asset_list'] = asset_list

    return render_template('index.html', content=plcontent, is_admin=is_admin)


"""
Multi file uploader.
User must be logged in.
"""
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
                flash('%s successfully uploaded' % (filename))

            else:
                flash('File type not accepted!')

        for file in \
        os.listdir(current_app.config['UPLOAD_FOLDER']):
            move('%s/%s' % (current_app.config['UPLOAD_FOLDER'] ,file), \
            '%scontent/%s' % (static, file))

        return render_template('upload.html')
    else:
        return render_template('upload.html')


"""
Admin page for user credential creation.
Must be logged in as admin to access
"""
@main.route('/admin')
@login_required
def admin():
    if current_user.permissions == 'admin':
        return render_template('admin.html')
    else:
        return render_template('index.html')


"""
Allows order and duration of playlist content.  Content can be deleted from
static by setting 'Duration' to 0 and ticking the 'Delete 0 duration files?'
box.
User must be logged in.
"""
@main.route('/player', methods=['GET', 'POST'])
@login_required
def player():
    global playlist, playlen, content#, asset_list, dur_list

    include = []
    content = os.listdir('%scontent/' % (static))

    # Remove items from playlist with duration of 0, deletes from static.
    def remzero():
        global content
        if len(delfiles) > 0 and delfiles[0] == 'on':
            line_queue = []
            with open(playfile, 'r') as pl:
                for line in pl.readlines():
                    if line.split(',')[1].rstrip('\n') == '0':
                        try:
                            os.remove('%scontent/%s' % (static, line.split(',')[0]))
                        except:
                            pass
                    else:
                        line_queue.append(line)
            pl.close
            content = os.listdir('%scontent/' % (static))
            with open(playfile, 'w') as pl:
                for line in line_queue:
                    if line.split(',')[0] in content:
                        pl.write('%s%s' % (line.rstrip('\n'), '\n'))

            pl.close

            flash('Deleting 0 duration files!')


    # Write data from select fields of /player to playfile
    if request.method == 'POST':
        content = os.listdir('%scontent/' % (static))
        session['playlist'] = request.form.getlist('order')
        session['playlen'] = request.form.getlist('time')
        playlist = session['playlist']
        playlen = session['playlen']
        delfiles = request.form.getlist('remfiles')
        if os.path.isfile(playfile):
            os.remove(playfile)
        for i in range(0, len(playlist)):
            with open(playfile, 'a') as pl:
                pl.write('%s,%s\n' % (playlist[i], playlen[i]))
            pl.close
        for i in range(0, len(playlist)):
            if int(playlen[i]) > 0:
                remzero()
                return redirect('/')
        remzero()
        flash('Duration must exceed zero on selected content!')
        # return redirect('/')

    return render_template('player.html', content=content)


"""
Renders a video or image HTML template of next content in queue.
Uses meta refresh to load next piece of content.
Duration of each item set in meta content.
"""
@main.route('/player/play', methods=['GET'])
def play(url='play'):
    # global asset_list, dur_list
    asset_list = session['asset_list']
    dur_list = session['dur_list']

    asset = 'content/%s' % (asset_list[0])
    dur_url = dur_list[0]

    asset_list += [asset_list.pop(0)]
    dur_list += [dur_list.pop(0)]

    session['dur_list'] = dur_list
    session['asset_list'] = asset_list

    if asset.split('.')[1] == 'mp4':
        return render_template('video.html', asset=asset, dur_url=dur_url)
    else:
        return render_template('img.html', asset=asset, dur_url=dur_url)