import streamlit as st
import numpy as np
import joblib
import warnings
from feature import FeatureExtraction
from streamlit_option_menu import option_menu
import pickle
import os

st.set_page_config(page_title="Deanshing", layout="wide")

warnings.filterwarnings('ignore')

# Load the model
gbc = joblib.load("rf_url.joblib")

# Functions to save and load URL history
def save_url_history(url_history, filename="url_history.pkl"):
    with open(filename, 'wb') as file:
        pickle.dump(url_history, file)

def load_url_history(filename="url_history.pkl"):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return []

# Initialize session state
def initialize_session_state():
    if 'url_history' not in st.session_state:
        st.session_state['url_history'] = load_url_history()

# Welcome page
def welcome_page():
    st.title("Yohohohoho!")
    st.image("assets/heker.gif", use_column_width=True)
    st.markdown("""
        Teman-teman tau ga, phishing itu serangan cyber yang bahaya banget lohh, karena kalau kamu sampai terkena serangan ini, informasi-informasi sensitif seperti kata sandi kamu, informasi keuangan kamu, dan bahkan identitas kamu bisa digunakan oleh pihak yang tidak bertanggung jawab untuk melakukan sesuatu yang ilegal atas nama kamu, ya! sekali lagi ku katakan ATAS NAMA KAMU!!!. Jadi jangan dianggap sepele ya teman-teman.
    """)
    st.title("Awas hindari kaktus!!!")
    st.image("assets/dino.gif", use_column_width=True)
    st.markdown("""
        Untuk menghindari URL phishing, ada beberapa langkah yang bisa teman-teman lakukan, yaitu:
        - Periksa URL dengan cermat sebelum mengklik atau memasukkan informasi sensitif.
        - Gunakan alamat URL langsung daripada mengklik tautan dari email atau pesan yang mencurigakan.
        - Pastikan situs web menggunakan protokol HTTPS dan memiliki sertifikat keamanan yang valid.
        - Waspadai tanda-tanda umum phishing seperti tekanan waktu, ancaman, atau penawaran yang terlalu bagus untuk menjadi kenyataan.
    """)
    st.title("Yuk kenalan sama Random Forest")
    st.image("assets/security.gif", use_column_width=True)
    st.markdown("""
        [1] Pertama, coba bayangkan kamu memiliki sebuah alat untuk mengidentifikasi apakah sebuah URL aman atau berbahaya untuk dikunjungi. Nah, Random Forest adalah seperti tim ahli keamanan yang terdiri dari banyak orang dengan keahlian berbeda-beda dalam mengenali tanda-tanda URL phishing.

        [2] Nah, setiap "ahli keamanan" dalam tim ini (dalam kasus ini, setiap pohon di hutan Random Forest) memiliki cara unik untuk memeriksa URL. Mereka bisa memeriksa apakah domainnya mencurigakan, apakah menggunakan protokol HTTPS yang aman, atau apakah ada kata-kata atau pola tertentu dalam URL yang menunjukkan tanda phishing.

        [3] Sehingga, ketika kamu memasukkan sebuah URL ke dalam Random Forest, setiap pohon (ahli keamanan) akan memberikan pendapatnya sendiri berdasarkan fitur-fitur yang diperiksa. Misalnya, satu pohon mungkin melihat bahwa URL menggunakan domain yang tidak umum atau tidak lazim, sementara pohon lain mungkin mencatat bahwa URL tidak menggunakan protokol HTTPS.

        [4] Setelah itu, Random Forest pun kemudian mengumpulkan semua pendapat dari seluruh "ahli keamanan" dan menentukan mayoritasnya. Jika sebagian besar pohon mengatakan bahwa URL tersebut mencurigakan berdasarkan fitur-fitur yang diperiksa, maka Random Forest akan memutuskan bahwa URL tersebut kemungkinan besar berbahaya atau phishing.

        [5] Kelebihan dari Random Forest dalam konteks ini adalah kemampuannya untuk menangani berbagai jenis fitur dan pola dalam URL tanpa perlu penyetelan yang rumit secara manual. Ini membuatnya sangat efektif dalam memprediksi apakah sebuah URL aman atau berpotensi phishing, dengan memanfaatkan kekuatan kolektif dari banyak "ahli keamanan" yang bekerja bersama-sama.
    """)

# Extract features from URL
def extract_features(url):
    obj = FeatureExtraction(url)
    features = obj.getFeaturesList()
    return features

# Detect page
def detect_page():
    initialize_session_state()  # Ensure session state is initialized

    st.markdown("""Video Demo:""")
    st.video("assets/kenalan.mp4")
    st.markdown("""
        Penjelasan Video:
        
        Kategori Phishing
        - Alamat URL "yutup.hub" mencoba menyerupai "YouTube" namun menggunakan ejaan yang tidak lazim dan domain ".hub", yang tidak umum untuk situs resmi seperti YouTube. Ini adalah teknik umum yang digunakan oleh situs phishing untuk menipu pengguna agar percaya bahwa mereka mengunjungi situs yang sah.
        - URL ini menggunakan protokol "http" bukan "https". Situs yang sah biasanya menggunakan "https" untuk memastikan keamanan data pengguna melalui enkripsi. Ketidakadaan HTTPS bisa menjadi tanda bahwa situs tersebut tidak aman dan mungkin berbahaya.
        - Domain ".hub" tidak umum digunakan oleh situs terpercaya. Situs phishing sering kali menggunakan domain yang tidak biasa atau baru untuk menghindari deteksi dan memberikan rasa urgensi atau keunikan palsu kepada pengguna.
        
        Kategori Non-Phishing
        - Domain "google.com" adalah domain resmi milik Google, salah satu perusahaan teknologi terbesar dan terpercaya di dunia. Ini adalah domain yang umum dan diakui secara global.
        - URL ini menggunakan protokol "https", yang menunjukkan bahwa situs ini memiliki sertifikat keamanan dan mengenkripsi data pengguna untuk melindungi informasi pribadi mereka.
        - Google telah lama dikenal sebagai penyedia layanan yang sah dengan banyak pengguna di seluruh dunia. Situs ini sering diverifikasi oleh berbagai otoritas dan memiliki reputasi yang sangat baik, sehingga kecil kemungkinan untuk menjadi situs phishing.
    """)
    url = st.text_input("Masukkan link di bawah ini")
    
    if st.button("Periksa"):
        if url:
            features = extract_features(url)
            x = np.array(features).reshape(1, -1) 
            y_pred = gbc.predict(x)[0]
            
            result = "aman" if y_pred == 1 else "berbahaya"
            st.session_state['url_history'].append((url, result))  # Add URL and result to history
            save_url_history(st.session_state['url_history'])  # Save the history to file
            
            if y_pred == 1:
                st.success(f"Horaay link yang kamu masukkan aman untuk diakses.")
                st.image("assets/s.gif")
                st.warning("""Mengapa demikian? karena URL tersebut sudah menggunakan protokol "https" yang menunjukkan bahwa URL tersebut memiliki sertifikat keamanan dan mengenkripsi data untuk melindungi informasi pribadi kamu.""")
            else:
                st.error(f"Waspadaa!!! link yang kamu berikan kemungkinan berbahaya.")
                st.image("assets/e.gif")
                st.warning("""Mengapa demikian? karena URL tersebut menggunakan protokol "http" bukan "https". Situs yang sah biasanya menggunakan "https" untuk memastikan keamanan data pengguna melalui enkripsi. Ketidakadaan HTTPS bisa menjadi tanda bahwa situs tersebut tidak aman dan mungkin berbahaya, karena bisa saja ada penyusup yang bisa meretas dan mengambil data pribadi yang kamu kirimkan.""")
        else:
            st.warning("Uhm.. sepertinya kamu belum memasukkan URLnya kawan :)")
            st.image("assets/w.gif")

# About page
def about_page():
    st.image("assets/profil.jpg", use_column_width=True)

    st.markdown("""
        <div style="display: flex; flex-direction: row; justify-content: center;">
            <div style="text-align: center; margin-right: 80px;">
                <a href="https://github.com/anan109019234/deanshing.git">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Octicons-mark-github.svg/200px-Octicons-mark-github.svg.png" alt="GitHub" style="width:30px;height:30px;">
                </a>
                <p style="margin-top: 5px;">Direktori</p>
            </div>
            <div style="text-align: center; margin-left: 80px;">
                <a href="https://www.kaggle.com/eswarchandt/phishing-website-detector">
                    <img src="https://cdn4.iconfinder.com/data/icons/logos-and-brands/512/189_Kaggle_logo_logos-512.png" alt="Kaggle" style="width:30px;height:30px;">
                </a>
                <p style="margin-top: 5px;">Dataset</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# URL list page
def url_list_page():
    initialize_session_state()  # Ensure session state is initialized

    st.markdown("### Daftar URL yang telah diperiksa:")
    if len(st.session_state['url_history']) > 0:
        for url, result in st.session_state['url_history']:
            color = "green" if result == "aman" else "red"
            st.markdown(f"<span style='color:{color}'>{url} - {result}</span>", unsafe_allow_html=True)
    else:
        st.warning("Belum ada URL yang diperiksa.")

# Main function
def main():
    initialize_session_state()  # Ensure session state is initialized

    selected = option_menu(
        menu_title=None,  
        options=["Selamat Datang", "Periksa Disini", "Daftar URL", "Tentang Saya"],  
        icons=["house", "book", "list", "envelope"],  
        menu_icon="cast",  
        default_index=0,  
        orientation="horizontal",
    )

    if selected == "Selamat Datang":
        welcome_page()
    elif selected == "Periksa Disini":
        detect_page()
    elif selected == "Daftar URL":
        url_list_page()
    elif selected == "Tentang Saya":
        about_page()

if __name__ == "__main__":
    main()
