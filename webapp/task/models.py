from webapp.db import db


class Tasks(db.Model):
    """
    Table of registered tasks for verification
    """
    id_task = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    id_appr_type = db.Column(db.Integer,
                             db.ForeignKey('approved_types.id_appr_type'))
    model_mi = db.Column(db.String(512))
    serial_number = db.Column(db.Integer)
    protocol_number = db.Column(db.String(64))
    id_status = db.Column(db.Integer, db.ForeignKey('status_task.id_status'))


class Status_task(db.Model):
    """
    Table of task status names
    """
    id_status = db.Column(db.Integer, primary_key=True)
    status_name = db.Column(db.String(32))
    tasks = db.relationship('Tasks', backref='tasks_status', lazy='dynamic')
