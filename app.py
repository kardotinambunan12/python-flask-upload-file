import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

path = os.getcwd()

# file Upload locations
UPLOAD_FOLDER = os.path.join(path, 'uploads')

# periksa apakah folder uploads sudah ada apa belum
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


jenis_extension_file = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','docx','xlsx'])

# lower berfungsi mengset namafile menjadi huruf kecil
def izinfile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in jenis_extension_file


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('tidak ada file yang ingin di upload')
            return redirect(request.url)
        if file and izinfile(file.filename):
            filename = secure_filename(file.filename)

            # alamat folder yang akan kita simpan
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('file sukses di upload ...')
            return redirect('/')
        else:
            flash('type file yang di izinkan txt, pdf, png, jpg, jpeg, gif, xlsx, docx')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host = '127.0.0.1',port = 2000, debug = False)