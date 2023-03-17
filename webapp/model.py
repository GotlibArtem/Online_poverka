from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Approved_types(db.Model):
    id_appr_type = db.Column(db.Integer, primary_key=True)
    number_si = db.Column(db.String(10), nullable=False)
    name_si = db.Column(db.Text)
    designation_si = db.Column(db.Text)
<<<<<<< HEAD
    number_record = db.Column(db.Integer)
=======
    number_record = db.Column(db.Integer, unique=True, nullable=False)
>>>>>>> dfb0d327518a178863f85504e14f2d2f19649d4e
    id_arshin = db.Column(db.Integer, unique=True, nullable=False)
    publication_date = db.Column(db.Date)
    manufacturer_si = db.Column(db.String)
    description_si = db.Column(db.String)
    method_verif_si = db.Column(db.String)
    proced_si = db.Column(db.String)
    certificate_date = db.Column(db.Date)
    mpi_si = db.Column(db.String(20))
    next_verif_si = db.Column(db.Boolean)
    part_verif_si = db.Column(db.Boolean)
<<<<<<< HEAD
    status_si = db.Column(db.String)
=======
    status_si = db.Column(db.Boolean)
>>>>>>> dfb0d327518a178863f85504e14f2d2f19649d4e
