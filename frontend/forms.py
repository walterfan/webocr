from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, HiddenField
from wtforms import BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Optional
import datetime

class UploadForm(FlaskForm):
    script_file = FileField('Upload Script', validators=[FileAllowed(['png', 'jpg', 'bmp'])])
    submit_file = SubmitField('Upload')

class OcrForm(FlaskForm):

    input_content = TextAreaField('input', validators=[Optional()],
                                   render_kw={
                                       "class": "form-control",
                                       "rows": 5})
    output_content = TextAreaField('output', validators=[Optional()],
                                   render_kw={
                                       "class": "form-control",
                                       "rows": 5,
                                       "cols": 60})

    ocr_command = SelectField('ocr_command',
                              choices=[(1, 'Extract URLs'),
                                        (2, 'Extract Text')
                                        ],
                              render_kw={"class": "form-control"},
                              coerce=int)

    ocr_params = StringField('ocr_params', validators=[Optional()],
                             render_kw={"class": "form-control"})

    ocr_file = StringField('ocr_file', validators=[DataRequired(), Length(1, 256)],
                               render_kw={"class": "form-control"})

    submit_button = SubmitField('Submit', render_kw={"class": "btn btn-primary"})