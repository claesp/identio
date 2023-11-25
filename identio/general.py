import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from identio.db import get_db

bp = Blueprint("general", __name__, url_prefix="/")

@bp.route("/")
def index():
    return render_template("general/index.html")
