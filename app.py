import streamlit as st
import numpy as np
import joblib
import warnings
from feature import FeatureExtraction
from streamlit_option_menu import option_menu

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
        - Periksa URL dengan cermat sebelum mengklik atau memasukkan informasi sensitif ([Periksa Disini](#)).
        - Gunakan alamat URL langsung daripada mengklik tautan dari email atau pesan yang mencurigakan.
        - Pastikan situs web menggunakan protokol HTTPS dan memiliki sertifikat keamanan yang valid.
        - Waspadai tanda-tanda umum phishing seperti tekanan waktu, ancaman, atau penawaran yang terlalu bagus untuk menjadi kenyataan.
    """)

def detect_page():
    st.video("assets/demo.mp4")
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
            else:
                st.error(f"Waspadaa!!! link yang kamu berikan {y_pro_phishing * 100:.2f}% kemungkinan berbahaya.")
        else:
            st.warning("Uhm.. sepertinya kamu belum memasukkan URLnya kawan :)")

def about_page():
    st.image("assets/profil.jpg", use_column_width=True)

    st.markdown("""
        <div style="display: flex; flex-direction: row; justify-content: center;">
            <div style="text-align: center; margin-right: 80px;">
                <a href="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwirmYrJn56HAxXaSGwGHWaQD8kQFnoECAYQAQ&url=https%3A%2F%2Fgithub.com%2F&usg=AOvVaw38IHvcyBra8HGhmSxvlCGw&opi=89978449">
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