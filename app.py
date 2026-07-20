from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__)

# Sambung Firebase (Render)
firebase_key = json.loads(os.environ.get("FIREBASE_KEY"))

cred = credentials.Certificate(firebase_key)

firebase_admin.initialize_app(cred)

db = firestore.client()


# Ambil data kamus dari Firebase
def ambil_kamus():
    data = []

    docs = db.collection("kamus").stream()

    for doc in docs:
        data.append(doc.to_dict())

    return data


@app.route("/", methods=["GET", "POST"])
def home():

    hasil = ""

    data_kamus = ambil_kamus()

    if request.method == "POST":

        ayat = request.form.get("perkataan", "").lower()

        senarai_perkataan = ayat.split()

        hasil_terjemahan = []

        for perkataan in senarai_perkataan:

            jumpa = False

            for item in data_kamus:

                if item["perkataan"].lower() == perkataan:
                    hasil_terjemahan.append(item["rintas"])
                    jumpa = True
                    break

            if not jumpa:
                hasil_terjemahan.append(f"[{perkataan}]")

        hasil = " ".join(hasil_terjemahan)


    jumlah_perkataan = len(data_kamus)

    return render_template(
        "index.html",
        hasil=hasil,
        jumlah_perkataan=jumlah_perkataan
    )


@app.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "POST":

        perkataan_baru = request.form.get("perkataan")
        rintas_baru = request.form.get("rintas")

        db.collection("kamus").add({
            "perkataan": perkataan_baru,
            "rintas": rintas_baru
        })


    return render_template("admin.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )