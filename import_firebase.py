import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate(
    "sistem-terjemahan-rintas-firebase-adminsdk-fbsvc-0006ce7902.json"
)

firebase_admin.initialize_app(cred)

db = firestore.client()


df = pd.read_excel("kamus.xlsx")


for index, row in df.iterrows():

    db.collection("kamus").add({
        "perkataan": str(row["perkataan"]),
        "rintas": str(row["rintas"])
    })

    print("Tambah:", row["perkataan"])


print("SELESAI IMPORT!")