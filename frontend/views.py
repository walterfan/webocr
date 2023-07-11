from flask import render_template, redirect, url_for, flash, request, current_app
from .forms import OcrForm, UploadForm
from werkzeug.utils import secure_filename
from . import app, logger, ocr
import os


dir_path = os.path.dirname(os.path.realpath(__file__))

ALLOWED_EXTENSIONS = set(['gif', 'jpg', 'png', 'bmp'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    upload_form = UploadForm()
    ocr_form = OcrForm()
    return render_template('index.html', form=ocr_form, upload_form=upload_form)


@app.route('/tool', methods=['GET', 'POST'])
def tool():
    upload_form = UploadForm()
    ocr_form = OcrForm()
    links = []
    if ocr_form.validate_on_submit():
        logger.info("submit: {}".format(ocr_form.ocr_command.data))

        image_file = ocr_form.ocr_file.data
        if ocr_form.ocr_command.data == 1:
            links = ocr.extract_urls(image_file)
            ocr_form.output_content.data = "\n".join(links)
        elif ocr_form.ocr_command.data == 2:
            text = ocr.extract_text(image_file)
            ocr_form.output_content.data = text
    else:
        if ocr_form.is_submitted():
            logger.error(ocr_form.errors)

    return render_template('tool.html', form=ocr_form, links=links, upload_form=upload_form)



@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    app = current_app._get_current_object()
    upload_path = app.config['UPLOAD_FOLDER']
    download_path = app.config['DOWNLOAD_PATH']

    upload_form = UploadForm()
    tool_form = OcrForm()

    if upload_form.validate_on_submit():
        file = upload_form.script_file.data
        logger.info('filename={}'.format(file.filename))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            saved_path = os.path.join(upload_path, filename)
            file.save(saved_path)
            #input_content = "{}/{}".format(upload_path, file.filename)
            logger.info('File successfully uploaded: {}'.format(saved_path))
            tool_form.ocr_file.data = f"{download_path}/{file.filename}"
        else:
            logger.info(upload_form.errors)

    return render_template('tool.html', form=tool_form, upload_form=upload_form)
