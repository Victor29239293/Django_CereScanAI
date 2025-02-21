

# 🧠 CereScanAI - Análisis de Resonancias Magnéticas con IA 🏥  

**CereScanAI** es una plataforma avanzada para la detección automática de **anomalías y tumores en resonancias magnéticas cerebrales**, utilizando inteligencia artificial y visión por computadora. Desarrollado con **Django**, **OpenCV** y **AWS**, este sistema está diseñado para ayudar a profesionales de la salud como **neuro-oncólogos, radiólogos y neurólogos** a analizar imágenes médicas de manera más rápida y precisa.  

## 🚀 Características  
🔹 **Carga y procesamiento de resonancias magnéticas** (FLAIR y T1CE)  
🔹 **Detección automática de tumores mediante un modelo basado en VGG16**  
🔹 **Resaltado de áreas anómalas en las imágenes procesadas**  
🔹 **Generación de informes médicos con detalles como tipo de anomalía y nivel de gravedad**  
🔹 **Seguimiento de pacientes y almacenamiento seguro de sus datos**  
🔹 **Autenticación con Google y gestión de usuarios (pacientes, médicos, administradores)**  
🔹 **Análisis estadístico de casos detectados**  

## 🛠️ Tecnologías utilizadas  
- **Backend:** Django + PostgreSQL  
- **IA & Procesamiento de imágenes:** OpenCV, Keras (VGG16)  
- **Almacenamiento en la nube:** AWS S3  
- **Autenticación:** Google OAuth  
- **Otras librerías:** TensorFlow, NumPy, Pandas  

## 📦 Instalación  
1. Clona el repositorio:  
   ```bash
   git clone https://github.com/tuusuario/CereScanAI.git
   ```  
2. Entra en el directorio del proyecto:  
   ```bash
   cd CereScanAI
   ```  
3. Crea un entorno virtual e instala las dependencias:  
   ```bash
   python -m venv venv  
   source venv/bin/activate  # En Windows: venv\Scripts\activate  
   pip install -r requirements.txt
   ```  
4. Configura las variables de entorno para la conexión a la base de datos y AWS.  
5. Aplica las migraciones:  
   ```bash
   python manage.py migrate
   ```  
6. Inicia el servidor:  
   ```bash
   python manage.py runserver
   ```  

## 📌 Notas  
- Es necesario configurar credenciales de AWS para almacenar imágenes en S3.  
- Se requiere una clave de Google OAuth para la autenticación.  

