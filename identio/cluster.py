import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from identio.db import get_db

bp = Blueprint("cluster", __name__, url_prefix="/cluster")

def get_cluster(id):
    db = get_db()
    cluster = db.execute(
        "SELECT c.cluster_id, c.cluster_name, c.identifier_id FROM cluster AS c WHERE c.identifier_id = ?",
        (id,)
    ).fetchone()

    if cluster is None:
      abort(404, f"Cluster {id} does not exist.")

    return cluster

@bp.route("/create/<int:id>", methods=("GET", "POST"))
def create(id):
    if request.method == "POST":
        cluster_name = request.form["cluster_name"]
        identifier_id = id
        db = get_db()
        error = None

        if not cluster_name:
            error = "Cluster name is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO cluster (cluster_name, identifier_id) VALUES (?, ?)",
                    (cluster_name, identifier_id),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Cluster {cluster_name} is already registered."
            else:
                return redirect(url_for("cluster.list", id=identifier_id))

        flash(error)

    return render_template("cluster/create.html")

@bp.route("/list/<int:id>")
def list(id):
    db = get_db()
    identifier_id = id
    clusters = db.execute(
        "SELECT c.cluster_id, c.cluster_name FROM cluster AS c WHERE c.identifier_id = ? ORDER BY c.cluster_name ASC",
        (identifier_id,)
    ).fetchall()

    return render_template("cluster/list.html", clusters=clusters)
