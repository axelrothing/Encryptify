import random
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Encryption_Model
from .encryption_method import CaesarEncryption, CaesarDecryption
from . import db

crypt = Blueprint('crypt', __name__)

class GlobalData:
    def __init__(self):
        self.encrypted_text = None
        self.decrypted_text = None
        self.code = None


globaldata = GlobalData()

@crypt.route("/encrypt-result")
def encrypt_result():
    encrypted_text = globaldata.encrypted_text
    code = globaldata.code

    globaldata.encrypted_text = None
    globaldata.code = None

    return render_template("encrypt_result.html", encrypted_text=encrypted_text, code=code)

@crypt.route("/decrypt-result")
def decrypt_result():
    decrypted_text = globaldata.decrypted_text

    globaldata.decrypted_text = None

    return render_template("decrypt_result.html", decrypted_text=decrypted_text)


@crypt.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    if request.method == "POST":
        text = request.form.get("text")

        if len(text) < 2:
            flash("Text must be at least 2 characters.", category="error")
        else:

            used_codes = Encryption_Model.query.with_entities(Encryption_Model.code).all()

            encryption_data = CaesarEncryption(text=text, used_codes=used_codes)
            code = encryption_data.code
            shift = encryption_data.generated_shift
            new_encryption = Encryption_Model(code=code, shift=shift)
            db.session.add(new_encryption)
            db.session.commit()

            globaldata.encrypted_text = encryption_data.encrypted_text
            globaldata.code = encryption_data.code

            flash("Successfully Encrypted!", category="success")
            return redirect(url_for("crypt.encrypt_result"))

    return render_template("encrypt.html")


def check_for_letters(string: str):
    for char in string:
        if not char.isdigit():
            return True
    return False


@crypt.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    if request.method == "POST":
        text = request.form.get("text")
        code = request.form.get("password")

        if len(text) < 1:
            flash("Text must be at least 2 characters.", category="error")
        elif check_for_letters(code):
            flash("Code can only contain numbers.", category="error")
        elif len(code) != 6:
            flash("Length of code must be 6 numbers.", category="error")
        else:
            code = int(code)

            try:
                shift = Encryption_Model.query.filter_by(code=code).first().shift
                if shift:
                    decryption_data = CaesarDecryption(text=text, shift=shift)
                    decrypted_text = decryption_data.decrypted_text

                    globaldata.decrypted_text = decrypted_text

                    flash("Successfully Decrypted!", category="success")
                    return redirect(url_for("crypt.decrypt_result"))
                else:
                    flash("Wrong Code, try again...", category="error")
            except:
                flash("Wrong Code, try again...", category="error")

    return render_template("decrypt.html")
