from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Baca fail Excel
df = pd.read_excel('kamus.xlsx')

# Kemas nama lajur
df.columns = df.columns.str.strip().str.lower()

# =========================
# HALAMAN UTAMA
# =========================
@app.route('/', methods=['GET', 'POST'])
def home():
    global df
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

    # Kira jumlah perkataan
    jumlah_perkataan = len(df)

    return render_template(
        'index.html',
        hasil=hasil,
        jumlah_perkataan=jumlah_perkataan
    )

# =========================
# HALAMAN ADMIN
# =========================
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global df
    mesej = ''

    if request.method == 'POST':
        perkataan = request.form.get('perkataan', '').strip().lower()
        rintas = request.form.get('rintas', '').strip()

        if perkataan and rintas:

            # Elak duplicate
            if perkataan in df['perkataan'].astype(str).str.lower().values:
                mesej = f'Perkataan "{perkataan}" sudah wujud!'
            else:
                # Data baru
                data_baru = pd.DataFrame({
                    'perkataan': [perkataan],
                    'rintas': [rintas]
                })

                # Tambah ke dataframe
                df = pd.concat([df, data_baru], ignore_index=True)

                # Simpan semula ke Excel
                df.to_excel('kamus.xlsx', index=False)

                mesej = f'Perkataan "{perkataan}" berjaya ditambah!'

    return render_template('admin.html', mesej=mesej)

# =========================
# JALANKAN APP
# =========================
if __name__ == '__main__':
    app.run()