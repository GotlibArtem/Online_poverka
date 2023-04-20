from webapp.db import db


class Approved_types(db.Model):
    """
    Description of the table of approved types of measuring instruments
    """
    id_appr_type = db.Column(db.Integer, primary_key=True)
    number_si = db.Column(db.String(10), nullable=False)
    name_si = db.Column(db.Text)
    designation_si = db.Column(db.Text)
    number_record = db.Column(db.Integer)
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
    status_si = db.Column(db.String)


class Verification_data(db.Model):
    """
    Description of the table storing json files for the approved types
    """
    id_appr_type = db.Column(db.Integer, primary_key=True)
    model_si = db.Column(db.String(1024), nullable=False)
    ver_data = db.Column(db.VARCHAR(), nullable=False)
