import cv2
import numpy as np
import os
import glob

def pixelate_image(image, blocks=15):
    h, w = image.shape[:2]
    if h == 0 or w == 0: return image
    # Reducir imagen fuertemente
    small = cv2.resize(image, (max(1, w//blocks), max(1, h//blocks)), interpolation=cv2.INTER_LINEAR)
    # Volver a ampliarla usando NEAREST para crear el efecto mosaico/pixelado
    pixelated = cv2.resize(small, (w, h), interpolation=cv2.INTER_NEAREST)
    return pixelated

def process_attendance_list(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: No se pudo leer {image_path}")
        return

    h, w = img.shape[:2]

    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 1. Encontrar la "tinta" (texto escrito) usando un threshold
    # Papel blanco (~255), tinta oscura (< 150)
    _, ink_mask = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Dilatar la máscara para abarcar los trazos completos y no dejar bordes nítidos
    kernel = np.ones((5,5), np.uint8)
    ink_mask = cv2.dilate(ink_mask, kernel, iterations=3)

    # 2. Generar versión pixelada de toda la imagen
    pixelated_full = pixelate_image(img, blocks=20) # Nivel de pixelado alto

    # 3. Definir Zonas Sensibles (Cajas delimitadoras relativas a la hoja)
    zone_mask = np.zeros_like(ink_mask)
    
    # ZONA A: Estudiantes (Cédula mitad derecha y Firma completa)
    # Suponiendo que Cédula y firma están en el lado derecho de la hoja (x: 65% a 95%)
    # y excluyendo el encabezado (y: 15% a 85%)
    cv2.rectangle(zone_mask, (int(w*0.65), int(h*0.15)), (int(w*0.95), int(h*0.85)), 255, -1)
    
    # ZONA B: Firma Docente
    # Suponiendo que firma al final de la página, centrada (bottom 15%)
    cv2.rectangle(zone_mask, (int(w*0.1), int(h*0.85)), (int(w*0.9), int(h*0.98)), 255, -1)

    # 4. Intersecar: Solo pixelaremos donde haya TINTA y esté dentro de la ZONA SENSIBLE
    final_mask = cv2.bitwise_and(zone_mask, ink_mask)

    # Convertir máscara a 3 canales para mezclarla con la imagen a color
    final_mask_3c = cv2.cvtColor(final_mask, cv2.COLOR_GRAY2BGR)

    # 5. Aplicar la pixelación solo en la máscara resultante
    # Si la celda está vacía (no hay tinta), final_mask será 0, por ende se conserva el pixel original (blanco)
    result = np.where(final_mask_3c == 255, pixelated_full, img)

    cv2.imwrite(output_path, result)
    print(f"Anonimizada y guardada: {os.path.basename(output_path)}")

def main():
    raw_dir = os.path.join(os.path.dirname(__file__), '..', 'Assents', 'Listas_Crudas')
    out_dir = os.path.join(os.path.dirname(__file__), '..', 'Assents', 'Listas')
    
    os.makedirs(out_dir, exist_ok=True)
    
    files = glob.glob(os.path.join(raw_dir, '*.jpg'))
    if not files:
        print(f"No se encontraron imágenes en {raw_dir}")
        return

    print(f"Iniciando anonimización de {len(files)} listas...")
    for file in files:
        filename = os.path.basename(file)
        out_path = os.path.join(out_dir, filename)
        process_attendance_list(file, out_path)
    
    print("¡Proceso completado exitosamente!")

if __name__ == '__main__':
    main()
