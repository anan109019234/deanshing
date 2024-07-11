import streamlit as st
import numpy as np
import joblib
import warnings
from feature import FeatureExtraction
from streamlit_option_menu import option_menu

st.set_page_config(
    page_title="Deanshing",
    page_icon="d.ico",
    layout="wide")

warnings.filterwarnings('ignore')

gbc = joblib.load("rf_url.joblib")

def welcome_page():
    st.title("Yohohohoho!")
    st.image("assets/heker.gif", use_column_width=True)
    st.markdown("""
        Teman-teman tau ga, phishing itu serangan cyber yang bahaya banget lohh, karena kalau kamu sampai terkena serangan ini, informasi-informasi sensitif seperti kata sandi kamu, informasi keuangan kamu, dan bahkan identitas kamu bisa digunakan oleh pihak yang tidak bertanggung jawab untuk melakukan sesuatu yang ilegal atas nama kamu, ya! sekali lagi ku katakan ATAS NAMA KAMU!!!. Jadi jangan dianggap sepele ya teman-teman.
    """)
    
    st.image("assets/dino.gif", use_column_width=True)
    st.markdown("""
        Untuk menghindari URL phishing, ada beberapa langkah yang bisa teman-teman lakukan, yaitu:
        - Periksa URL dengan cermat sebelum mengklik atau memasukkan informasi sensitif.
        - Gunakan alamat URL langsung daripada mengklik tautan dari email atau pesan yang mencurigakan.
        - Pastikan situs web menggunakan protokol HTTPS dan memiliki sertifikat keamanan yang valid.
        - Waspadai tanda-tanda umum phishing seperti tekanan waktu, ancaman, atau penawaran yang terlalu bagus untuk menjadi kenyataan.
    """)

def detect_page():
    st.markdown("""Video Demo:""")
    st.video("assets/demo.mp4")
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
            obj = FeatureExtraction(url)
            x = np.array(obj.getFeaturesList()).reshape(1, -1)
            
            y_pred = gbc.predict(x)[0]
            y_pro_phishing = gbc.predict_proba(x)[0, 0]
            y_pro_non_phishing = gbc.predict_proba(x)[0, 1]
            
            if y_pred == 1:
                st.success(f"Horaay link yang kamu masukkan  {y_pro_non_phishing * 100:.2f}% aman untuk diakses.")
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Checkmark.svg/1024px-Checkmark.svg.png", width=100)
            else:
                st.error(f"Waspadaa!!! link yang kamu berikan {y_pro_phishing * 100:.2f}% kemungkinan berbahaya.")
                st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Red_X.svg/1024px-Red_X.svg.png", width=100)
        else:
            st.warning("Uhm.. sepertinya kamu belum memasukkan URLnya kawan :)")
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Exclamation_mark_red.png/1024px-Exclamation_mark_red.png", width=100)

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

def main():
    selected = option_menu(
        menu_title=None,  
        options=["Selamat Datang", "Periksa Disini", "Tentang Saya"],  
        icons=["house", "book", "envelope"],  
        menu_icon="cast",  
        default_index=0,  
        orientation="horizontal",
    )

    if selected == "Selamat Datang":
        welcome_page()
    elif selected == "Periksa Disini":
        detect_page()
    elif selected == "Tentang Saya":
        about_page()

if __name__ == "__main__":
    main()
