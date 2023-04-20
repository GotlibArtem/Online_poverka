from webapp.db import db


class Tasks(db.Model):
    """
    Table of registered tasks for verification
    """
    id_task = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, nullable=False)
    id_appr_type = db.Column(db.Integer, nullable=False)
    model_mi = db.Column(db.String(512))
    serial_number = db.Column(db.Integer)
    protocol_number = db.Column(db.String(64))
    id_status = db.Column(db.Integer, nullable=False)
