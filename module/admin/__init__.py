from flask import Blueprint, render_template
admin1 = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

from module.admin import adminroutes