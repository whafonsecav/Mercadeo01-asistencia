import cv2
import numpy as np
import os
import glob

def generate_test_masks():
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'Assents', 'Listas_Crudas')
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Assents', 'Listas_Prueba')
    os.makedirs(out_dir, exist_ok=True)
    
    files = glob.glob(os.path.join(raw_dir, '*.jpg'))
    
    for file in files:
        img = cv2.imread(file)
        if img is None: continue
        h, w = img.shape[:2]
        
        # Vamos a pintar en rojo lo que se va a pixelar
        overlay = img.copy()
        
        # ZONA: Mitad derecha de cédula + Firma (Ajustado)
        # Intentemos de 52% a 80% del ancho, para evitar los checks a la derecha (>80%)
        # y evitar el total de asistentes (bottom right).
        x1 = int(w * 0.52)
        x2 = int(w * 0.82)
        y1 = int(h * 0.15)
        y2 = int(h * 0.85)
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 255), -1) # Rojo
        
        # ZONA: Firma Docente (Ajustado al centro abajo)
        tx1 = int(w * 0.20)
        tx2 = int(w * 0.80)
        ty1 = int(h * 0.85)
        ty2 = int(h * 0.98)
        cv2.rectangle(overlay, (tx1, ty1), (tx2, ty2), (0, 0, 255), -1)
        
        # Transparencia
        alpha = 0.4
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        
        filename = os.path.basename(file)
        cv2.imwrite(os.path.join(out_dir, filename), img)
        print(f"Prueba generada: {filename}")

if __name__ == '__main__':
    generate_test_masks()
