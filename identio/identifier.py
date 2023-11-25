import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from identio.db import get_db

bp = Blueprint("identifier", __name__, url_prefix="/identifier")

def get_identifier(id):
    db = get_db()
    identifier = db.execute(
        "SELECT i.identifier_id, i.identifier_name, i.identifier_description, i.identifier_cluster_name FROM identifier AS i WHERE i.identifier_id = ?",
        (id,)
    ).fetchone()

    if identifier is None:
      abort(404, f"Identifier {id} does not exist.")

    return identifier

@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == "POST":
        identifier_name = request.form["identifier_name"]
        identifier_desc = request.form["identifier_description"]
        db = get_db()
        error = None

        if not identifier_name:
            error = "Identifier name is required."
        elif not identifier_desc:
            error = "Identifier description is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO identifier (identifier_name, identifier_description, identifier_cluster_name) VALUES (?, ?, \"Network\")",
                    (identifier_name, identifier_desc),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Identifier {identifier_name} is already registered."
            else:
                return redirect(url_for("identifier.list"))

        flash(error)

    return render_template("identifier/create.html")

@bp.route("/list")
def list():
    db = get_db()
    identifiers = db.execute(
        "SELECT i.identifier_id, i.identifier_name, i.identifier_description FROM identifier AS i ORDER BY i.identifier_name ASC"
    ).fetchall()

    return render_template("identifier/list.html", identifiers=identifiers)

@bp.route("/view/<int:id>")
def view(id):
    identifier = get_identifier(id)

    return render_template("identifier/view.html", identifier=identifier)

@bp.route("/edit/<int:id>", methods=("GET", "POST"))
def edit(id):
    if request.method == "POST":
        identifier_id = id
        identifier_name = request.form["identifier_name"]
        identifier_desc = request.form["identifier_description"]
        db = get_db()
        error = None

        if not identifier_name:
            error = "Identifier name is required."
        elif not identifier_desc:
            error = "Identifier description is required."

        if error is None:
            try:
                db.execute(
                    "UPDATE identifier SET identifier_name = ?, identifier_description = ? WHERE identifier_id = ?",
                    (identifier_name, identifier_desc, identifier_id),
                )
                db.commit()
            except:
                error = "Unknown error."
            else:
                return redirect(url_for("identifier.list"))

        flash(error)

    identifier = get_identifier(id)

    return render_template("identifier/edit.html", identifier=identifier)

@bp.route("/delete/<int:id>", methods=("GET", "POST"))
def delete(id):
    if request.method == "POST":
        identifier_id = id
        db = get_db()
        error = None

        if error is None:
            try:
                db.execute(
                    "DELETE FROM identifier WHERE identifier_id = ?",
                    (identifier_id,),
                )
                db.commit()
            except:
                error = "Unknown error."
            else:
                return redirect(url_for("identifier.list"))

        flash(error)

    identifier = get_identifier(id)

    return render_template("identifier/delete.html", identifier=identifier)

@bp.route("/config/<int:id>", methods=("GET", "POST"))
def config(id):
    if request.method == "POST":
        identifier_id = id
        cluster_name = request.form["cluster_name"]
        db = get_db()
        error = None

        if error is None:
            try:
                db.execute(
                    "UPDATE identifier SET identifier_cluster_name = ? WHERE identifier_id = ?",
                    (cluster_name, identifier_id,),
                )
                db.commit()
            except:
                error = "Unknown error."
            else:
                return redirect(url_for("identifier.view", id=identifier_id))

        flash(error)

    identifier = get_identifier(id)

    return render_template("identifier/config.html", identifier=identifier)
