import os
import numpy as np
import cv2
import logging
from keras import models
from django.conf import settings
from sklearn.preprocessing import LabelEncoder
from PIL import Image
import base64
from scipy.ndimage import zoom
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt  
import nibabel as nib
import io



logger = logging.getLogger(__name__)


try:
    MODEL_PATH = os.path.join(settings.BASE_DIR, 'static', 'model', 'model_per_class.h5')
    model = models.load_model(MODEL_PATH)
    logger.info(f"Modelo cargado correctamente desde {MODEL_PATH}")
except Exception as e:
    logger.error(f"Error al cargar el modelo: {e}")
    raise

SEGMENT_CLASSES = {
    0: 'NOT tumor',
    1: 'NECROTIC/CORE',
    2: 'EDEMA',
    3: 'ENHANCING'
}

def preprocess_scan(scan):
    scan = (scan - np.min(scan)) / (np.max(scan) - np.min(scan))  # Normalizar
    zoom_factors = (128 / scan.shape[0], 128 / scan.shape[1], 128 / scan.shape[2])
    scan = zoom(scan, zoom_factors, order=1)
    central_slice = scan[:, :, 64]  
    return central_slice



def process_flair_t1ce(flair_path, t1ce_path):

    flair = preprocess_scan(nib.load(flair_path).get_fdata())
    t1ce = preprocess_scan(nib.load(t1ce_path).get_fdata())
    

    combined_input = np.expand_dims(np.stack([flair, t1ce], axis=-1), axis=0)
    prediction = model.predict(combined_input)
    
    segmentation = np.argmax(prediction[0], axis=-1)
    
    return flair, t1ce, segmentation

def create_colored_overlay(flair, mask):

    flair_uint8 = (flair * 255).astype(np.uint8)


    colors = {
        0: [0, 0, 0],       
        1: [255, 0, 0],      
        2: [0, 255, 0],      
        3: [0, 0, 255],      
    }


    colored_mask = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)

    for label, color in colors.items():
        colored_mask[mask == label] = color

   
    flair_rgb = np.stack([flair_uint8] * 3, axis=-1) 
    blended = cv2.addWeighted(flair_rgb, 0.7, colored_mask, 0.3, 0) 
    
    return blended


def create_segmentation_images(flair, t1ce, mask):
  


    images_base64 = {}


    fig, ax = plt.subplots()
    ax.imshow(flair, cmap='gray')
    ax.set_title('Original FLAIR Image')
    ax.axis('off')
    buf_flair = io.BytesIO()
    plt.savefig(buf_flair, format='png', bbox_inches='tight')
    buf_flair.seek(0)
    images_base64['flair'] = base64.b64encode(buf_flair.getvalue()).decode('utf-8')
    plt.close(fig)

    fig, ax = plt.subplots()
    ax.imshow(t1ce, cmap='gray')
    ax.set_title('Original T1CE Image')
    ax.axis('off')
    buf_t1ce = io.BytesIO()
    plt.savefig(buf_t1ce, format='png', bbox_inches='tight')
    buf_t1ce.seek(0)
    images_base64['t1ce'] = base64.b64encode(buf_t1ce.getvalue()).decode('utf-8')
    plt.close(fig)


    necrotic_mask = (mask == 1)
    fig, ax = plt.subplots()
    ax.imshow(flair, cmap='gray') 
    ax.imshow(necrotic_mask, cmap='Reds', alpha=0.5)  
    ax.set_title('NECROTIC/CORE')
    ax.axis('off')
    buf_necrotic = io.BytesIO()
    plt.savefig(buf_necrotic, format='png', bbox_inches='tight')
    buf_necrotic.seek(0)
    images_base64['necrotic_core'] = base64.b64encode(buf_necrotic.getvalue()).decode('utf-8')
    plt.close(fig)


    edema_mask = (mask == 2)
    fig, ax = plt.subplots()
    ax.imshow(flair, cmap='gray') 
    ax.imshow(edema_mask, cmap='Greens', alpha=0.5)  
    ax.set_title('EDEMA')
    ax.axis('off')
    buf_edema = io.BytesIO()
    plt.savefig(buf_edema, format='png', bbox_inches='tight')
    buf_edema.seek(0)
    images_base64['edema'] = base64.b64encode(buf_edema.getvalue()).decode('utf-8')
    plt.close(fig)

    enhancing_mask = (mask == 3)
    fig, ax = plt.subplots()
    ax.imshow(flair, cmap='gray')  
    ax.imshow(enhancing_mask, cmap='Blues', alpha=0.5)  
    ax.set_title('ENHANCING')
    ax.axis('off')
    buf_enhancing = io.BytesIO()
    plt.savefig(buf_enhancing, format='png', bbox_inches='tight')
    buf_enhancing.seek(0)
    images_base64['enhancing'] = base64.b64encode(buf_enhancing.getvalue()).decode('utf-8')
    plt.close(fig)

    return images_base64