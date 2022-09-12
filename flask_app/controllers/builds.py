from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import build
from flask_app.models import user
import os


from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/chris/OneDrive/Documents/Solo_Project/flask_app/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#HOME
@app.route('/home')
def home():
    if not 'user_id' in session:
        return redirect('/')
    all_builds = build.Build.get_builds()
    print('>>>>>>>>>>>>>>>>>>>>>>>>', all_builds)
    return render_template('home.html', all_builds = all_builds)

#CREATE BUILD 
@app.route('/new/build')
def new_build():
    if not 'user_id' in session:
        return redirect('/')
    return render_template('create.html')

@app.route('/new_build', methods = ['POST'])
def create_build():
    if not build.Build.validate_build(request.form):
        return redirect('/new/build')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/new/build')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/new/build')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            data = {
                'image_path': "/static/images/"+filename,
                'make_and_model': request.form['make_and_model'],
                'year_of_car': request.form['year_of_car'],
                'specs': request.form['specs'],
                'user_id': request.form['user_id']
            }
    build.Build.save(data)
    return redirect('/home')

#UPDATE BUILD
@app.route('/update/<int:id>')
def update_page(id):
    if not 'user_id' in session:
        return redirect('/')
    return render_template('update.html', build = build.Build.get_one_build(id))

@app.route('/update_build', methods = ['POST'])
def update_build():
    if not build.Build.validate_build(request.form):
        return redirect(f'/edit/{request.form["id"]}')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/update/<int:id>')
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect('/new/build')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            data = {
                'image_path': "/static/images/"+filename,
                'make_and_model': request.form['make_and_model'],
                'year_of_car': request.form['year_of_car'],
                'specs': request.form['specs'],
                'user_id': request.form['user_id']
            }
    build.Build.update(data)
    return redirect('/home')

#Show Build
@app.route('/view/<int:id>')
def view_page(id):
    if not 'user_id' in session:
        return redirect('/')
    all_builds = build.Build.get_builds()
    return render_template('view.html', build = build.Build.get_one_build(id), all_builds = all_builds)


#DELETE Build
@app.route('/delete/<int:id>', methods = ['POST'])
def delete_build(id):
    build.Build.delete_build(id)
    return redirect('/home')

#UPLOAD IMAGE?
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#@app.route('/image/post', methods=['GET', 'POST'])
#def upload_file():
    #if request.method == 'POST':
        # check if the post request has the file part
        #if 'file' not in request.files:
            #flash('No file part')
            #return redirect('/new/build')
        #file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        #if file.filename == '':
            #flash('No selected file')
            #return redirect('/new/build')
        #if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #print(filename)
            #data = {
                #'image_path': "/static/images/"+filename,
                #'make_and_model': request.form['make_and_model'],
                #'year_of_car': request.form['year_of_car'],
                #'specs': request.form['specs']
            #}
            #build.Build.save(data)
        #return redirect('/new/build')