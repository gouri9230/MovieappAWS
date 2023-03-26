from flask import Blueprint

mov = Blueprint('mov', __name__)
from . import routes