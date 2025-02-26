from flask import Flask, render_template, jsonify
import random
import json

app = Flask(__name__)

# Load Quran data
with open('data/uthmani.json', 'r', encoding='utf-8') as f:
    uthmani_data = json.load(f)

with open('data/english.json', 'r', encoding='utf-8') as f:
    english_data = json.load(f)

with open('data/audio.json', 'r', encoding='utf-8') as f:
    audio_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/random_ayat')
def random_ayat():
    # Pilih surah dan ayat secara acak dari uthmani.json
    random_surah = random.choice(uthmani_data['data']['surahs'])
    random_ayat = random.choice(random_surah['ayahs'])

    # Cari terjemahan dan audio yang sesuai
    english_ayat = next(
        (ayah for surah in english_data['data']['surahs'] 
         for ayah in surah['ayahs'] 
         if ayah['number'] == random_ayat['number']),
        None
    )

    audio_ayat = next(
        (ayah for surah in audio_data['data']['surahs'] 
         for ayah in surah['ayahs'] 
         if ayah['number'] == random_ayat['number']),
        None
    )

    return jsonify({
        'surah': random_surah['name'],  # Nama Surah dalam Arab
        'surah_latin': random_surah['englishName'],  # Nama Surah dalam Alfabet Latin
        'surah_translation': random_surah['englishNameTranslation'],  # Nama Surah dalam Terjemahan English
        'surah_translation_ind': random_surah['indonesianNameTranslation'],  # Nama Surah dalam Terjemahan Indonesia
        'ayah': random_ayat['numberInSurah'],  # Tampilkan numberInSurah di UI
        'total_ayat': len(random_surah['ayahs']),
        'arabic': random_ayat['text'],
        'english': english_ayat['text'] if english_ayat else 'Translation not available',
        'indonesian': english_ayat['text_ind'] if english_ayat else 'Terjemahan tidak tersedia',
        'audio': audio_ayat['audio'] if audio_ayat else 'Audio not available',
        'surah_number': random_surah['number'],  # Menyertakan number surah untuk navigasi
        'ayah_number': random_ayat['number'],  # Mengembalikan number untuk navigasi
        'tafsir_kemenag': english_ayat.get('tafsir_kemenag', 'Tafsir tidak tersedia')  # Tafsir Kemenag
    })

@app.route('/next_ayat/<int:ayah_number>')
def next_ayat(ayah_number):
    all_ayahs = [ayah for surah in uthmani_data['data']['surahs'] for ayah in surah['ayahs']]
    
    # Cari index ayat yang sekarang
    current_ayah_index = next((i for i, ayah in enumerate(all_ayahs) if ayah['number'] == ayah_number), None)

    # Tentukan ayat berikutnya
    if current_ayah_index is not None and current_ayah_index + 1 < len(all_ayahs):
        next_ayah = all_ayahs[current_ayah_index + 1]
    else:
        next_ayah = all_ayahs[0]  # Kembali ke ayat pertama jika sudah di ayat terakhir
    
    # Cari surah yang sesuai untuk ayat berikutnya
    surah = next(surah for surah in uthmani_data['data']['surahs'] if next_ayah['number'] in [ayah['number'] for ayah in surah['ayahs']])

    # Cari terjemahan dan audio yang sesuai untuk ayat berikutnya
    english_ayat = next(
        (ayah for surah in english_data['data']['surahs'] 
         for ayah in surah['ayahs'] 
         if ayah['number'] == next_ayah['number']),
        None
    )

    audio_ayat = next(
        (ayah for surah in audio_data['data']['surahs'] 
         for ayah in surah['ayahs'] 
         if ayah['number'] == next_ayah['number']),
        None
    )

    return jsonify({
        'surah': surah['name'],
        'surah_latin': surah['englishName'],
        'surah_translation': surah['englishNameTranslation'],
        'surah_translation_ind': surah['indonesianNameTranslation'],
        'ayah': next_ayah['numberInSurah'],  # Tampilkan numberInSurah di UI
        'total_ayat': len(surah['ayahs']),
        'arabic': next_ayah['text'],
        'english': english_ayat['text'] if english_ayat else 'Translation not available',
        'indonesian': english_ayat['text_ind'] if english_ayat else 'Terjemahan tidak tersedia',
        'audio': audio_ayat['audio'] if audio_ayat else 'Audio not available',
        'surah_number': surah['number'],
        'ayah_number': next_ayah['number'],  # Mengembalikan number untuk navigasi
        'tafsir_kemenag': english_ayat.get('tafsir_kemenag', 'Tafsir tidak tersedia')  # Tafsir Kemenag
    })

@app.route('/previous_ayat/<int:ayah_number>')
def previous_ayat(ayah_number):
    all_ayahs = [ayah for surah in uthmani_data['data']['surahs'] for ayah in surah['ayahs']]
    
    # Cari index ayat yang sekarang
    current_ayah_index = next((i for i, ayah in enumerate(all_ayahs) if ayah['number'] == ayah_number), None)

    # Tentukan ayat sebelumnya
    if current_ayah_index is not None and current_ayah_index - 1 >= 0:
        previous_ayah = all_ayahs[current_ayah_index - 1]
    else:
        previous_ayah = all_ayahs[-1]  # Kembali ke ayat terakhir jika sudah di ayat pertama
    
    # Cari surah yang sesuai untuk ayat sebelumnya
    surah = next(surah for surah in uthmani_data['data']['surahs'] if previous_ayah['number'] in [ayah['number'] for ayah in surah['ayahs']])

    # Cari terjemahan dan audio yang sesuai untuk ayat sebelumnya
    english_ayat = next(
        (ayah for surah in english_data['data']['surahs'] 
         for ayah in surah['ayahs'] 
         if ayah['number'] == previous_ayah['number']),
        None
    )

    audio_ayat = next(
        (ayah for surah in audio_data['data']['surahs'] 
         for ayah in surah['ayahs'] 
         if ayah['number'] == previous_ayah['number']),
        None
    )

    return jsonify({
        'surah': surah['name'],
        'surah_latin': surah['englishName'],
        'surah_translation': surah['englishNameTranslation'],
        'surah_translation_ind': surah['indonesianNameTranslation'],
        'ayah': previous_ayah['numberInSurah'],  # Tampilkan numberInSurah di UI
        'total_ayat': len(surah['ayahs']),
        'arabic': previous_ayah['text'],
        'english': english_ayat['text'] if english_ayat else 'Translation not available',
        'indonesian': english_ayat['text_ind'] if english_ayat else 'Terjemahan tidak tersedia',
        'audio': audio_ayat['audio'] if audio_ayat else 'Audio not available',
        'surah_number': surah['number'],  # Menyertakan number surah untuk navigasi
        'ayah_number': previous_ayah['number'],  # Mengembalikan number untuk navigasi
        'tafsir_kemenag': english_ayat.get('tafsir_kemenag', 'Tafsir tidak tersedia')  # Tafsir Kemenag
    })

if __name__ == '__main__':
    app.run(debug=True)