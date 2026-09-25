import cv2
import numpy as np
import os
import glob

def pixelate_image(image, blocks=20):
    h, w = image.shape[:2]
    if h == 0 or w == 0: return image
    small = cv2.resize(image, (max(1, w//blocks), max(1, h//blocks)), interpolation=cv2.INTER_LINEAR)
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    return pixelated

def process_attendance_list(image_path, output_path):
    filename = os.path.basename(image_path)
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: No se pudo leer {image_path}")
        return

    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Encontrar la "tinta"
    _, ink_mask = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((5,5), np.uint8)
    ink_mask = cv2.dilate(ink_mask, kernel, iterations=3)

    pixelated_full = pixelate_image(img, blocks=20)

    # 3. Definir Zonas Sensibles
    zone_mask = np.zeros_like(ink_mask)
    
    # Lógica especial para la primera lista que fue a mano alzada
    if "01. Aug 06" in filename:
        # Mitad de las cédulas
        cv2.rectangle(zone_mask, (int(w*0.75), int(h*0.10)), (int(w*0.85), int(h*0.65)), 255, -1)
        # Firma Docente (Centro Abajo)
        cv2.rectangle(zone_mask, (int(w*0.50), int(h*0.65)), (int(w*0.85), int(h*0.85)), 255, -1)
    else:
        # Lógica para las listas impresas en formato tabla estándar
        
        # ZONA A: Mitad derecha de la CÉDULA + Columna FIRMA completa
        # Cédula está ~43-58%. Firma está ~58-85%. 
        # Mitad de cédula a fin de firma = 50% a 84%.
        # Protegemos <50% (nombres y primer plano de cédula) y >84% (columna de Checks).
        cv2.rectangle(zone_mask, (int(w*0.50), int(h*0.15)), (int(w*0.84), int(h*0.85)), 255, -1)
        
        # ZONA B: Firma Docente
        # En la plantilla impresa, la firma está abajo a la izquierda (5% a 40%).
        # Protegemos el cuadro de 'Total Estudiantes' que está a la derecha.
        cv2.rectangle(zone_mask, (int(w*0.05), int(h*0.85)), (int(w*0.40), int(h*0.98)), 255, -1)

    # Intersecar máscara de zona con la tinta
    final_mask = cv2.bitwise_and(zone_mask, ink_mask)
    final_mask_3c = cv2.cvtColor(final_mask, cv2.COLOR_GRAY2BGR)

    # Mezclar y guardar
    result = np.where(final_mask_3c == 255, pixelated_full, img)
    cv2.imwrite(output_path, result)
    print(f"Anonimizada y guardada: {filename}")

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'Assents', 'Listas_Crudas')
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Assents', 'Listas')
    os.makedirs(out_dir, exist_ok=True)
    
    files = glob.glob(os.path.join(raw_dir, '*.jpg'))
    for file in files:
        process_attendance_list(file, os.path.join(out_dir, os.path.basename(file)))

if __name__ == '__main__':
    main()
