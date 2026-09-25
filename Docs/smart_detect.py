import cv2
import numpy as np
import glob
import sys

def test_grid():
    files = glob.glob('Assents/Listas_Crudas/*.jpg')
    print(f"Archivos encontrados: {len(files)}")
    for file in files:
        img = cv2.imread(file)
        if img is None:
            print("No se pudo leer", file)
            continue
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        
        # Dilate to enhance lines
        kernel = np.ones((5,1), np.uint8)
        thresh = cv2.dilate(thresh, kernel, iterations=1)
        
        # Vertical lines
        ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(img.shape[0]*0.1))) # 10% height minimum
        vertical_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, ver_kernel, iterations=2)
        
        cnts, _ = cv2.findContours(vertical_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        x_coords = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            if h > img.shape[0] * 0.3: # Must be at least 30% of image height
                x_coords.append(x)
                
        x_coords = sorted(x_coords)
        clean_x = []
        for x in x_coords:
            if not clean_x or x - clean_x[-1] > 30:
                clean_x.append(x)
                
        print(f"{file}: Found {len(clean_x)} vertical lines at: {clean_x}")
        # Calculate widths percentages
        w_img = img.shape[1]
        pcts = [round(x/w_img*100, 1) for x in clean_x]
        print(f"  Percentages: {pcts}")

test_grid()
