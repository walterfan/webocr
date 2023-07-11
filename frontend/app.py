from flask import Flask, render_template
from . import app, logger
from .forms import OcrForm, UploadForm
from . import views
import os

dir_path = os.path.dirname(os.path.realpath(__file__))



