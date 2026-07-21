from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Baca fail Excel
df = pd.read_excel('kamus.xlsx')

# Kemas nama lajur
df.columns = df.columns.str.strip().str.lower()

@app.route('/', methods=['GET', 'POST'])
def home():
    hasil = ''

    if request.method == 'POST':
        ayat = request.form.get('perkataan', '').lower()
        senarai_perkataan = ayat.split()

        hasil_terjemahan = []

        for perkataan in senarai_perkataan:
            cari = df[df['perkataan'].astype(str).str.lower() == perkataan]

            if not cari.empty:
                hasil_terjemahan.append(str(cari.iloc[0]['rintas']))
            else:
                hasil_terjemahan.append(f'[{perkataan}]')

        hasil = ' '.join(hasil_terjemahan)

    # Kira jumlah perkataan dalam Excel
    jumlah_perkataan = len(df)

    return render_template(
        'index.html',
        hasil=hasil,
        jumlah_perkataan=jumlah_perkataan
    )

if __name__ == '__main__':
    app.run()