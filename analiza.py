import cv2
import numpy as np
import matplotlib.pyplot as plt
import rasterio

# Konfiguracja
lata = ['1985', '1993', '2001', '2011']
pliki = [f'{rok}.png' for rok in lata]

# Empirycznie przyjęte progi dla indeksów
progi = {
    'VARI': 0.05,
    'GLI': 0.08,
    'VIGREEN': 0.05
}

# Słownik do przechowywania procentowego udziału obszarów leśnych dla każdego indeksu
obszary_lasow = {'VARI': [], 'GLI': [], 'VIGREEN': []}

plt.figure(figsize=(15, 10))

for i, (rok, plik) in enumerate(zip(lata, pliki)):
    # 1. Wczytanie obrazu
    img_bgr = cv2.imread(plik)
    if img_bgr is None:
        print(f"Nie znaleziono pliku: {plik}")
        continue

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # 2. Wyrównanie histogramu w przestrzeni HSV (tylko do wizualizacji)
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    h, s, v = cv2.split(img_hsv)
    v_eq = cv2.equalizeHist(v)
    img_hsv_eq = cv2.merge((h, s, v_eq))
    img_rgb_eq = cv2.cvtColor(img_hsv_eq, cv2.COLOR_HSV2RGB)

    # Przygotowanie do analizy na oryginalnych obrazach (bez wyrównania histogramu)
    R = img_rgb[:, :, 0].astype(np.float32)
    G = img_rgb[:, :, 1].astype(np.float32)
    B = img_rgb[:, :, 2].astype(np.float32)

    # Zapobieganie dzieleniu przez 0
    epsilon = 1e-8

    # 3. Obliczenie indeksów
    vari = (G - R) / (G + R - B + epsilon)
    gli = (2 * G - R - B) / (2 * G + R + B + epsilon)
    vigreen = (G - R) / (G + R + epsilon)

    # 4. Progowanie
    vari_thresh = vari > progi['VARI']
    gli_thresh = gli > progi['GLI']
    vigreen_thresh = vigreen > progi['VIGREEN']

    # 5. Obliczanie procentu zalesienia
    total_pixels = R.size
    obszary_lasow['VARI'].append(np.sum(vari_thresh) / total_pixels * 100)
    obszary_lasow['GLI'].append(np.sum(gli_thresh) / total_pixels * 100)
    obszary_lasow['VIGREEN'].append(
        np.sum(vigreen_thresh) / total_pixels * 100)

    # Wizualizacje dla pojedynczego roku

    fig, axs = plt.subplots(1, 5, figsize=(20, 4))
    fig.suptitle(f'Analiza dla roku {rok}')

    axs[0].imshow(img_rgb_eq)
    axs[0].set_title("RGB Eq")
    axs[0].axis('off')

    axs[1].imshow(vari, cmap='RdYlGn', vmin=-1, vmax=1)
    axs[1].set_title("VARI")
    axs[1].axis('off')

    axs[2].imshow(vari_thresh, cmap='viridis')
    axs[2].set_title("VARI Thresh")
    axs[2].axis('off')

    axs[3].imshow(gli_thresh, cmap='viridis')
    axs[3].set_title("GLI Thresh")
    axs[3].axis('off')

    axs[4].imshow(vigreen_thresh, cmap='viridis')
    axs[4].set_title("VIGREEN Thresh")
    axs[4].axis('off')

    plt.show()

# 6. Wykres zmian w czasie (Punkt 4)
plt.figure(figsize=(10, 6))
plt.plot(lata, obszary_lasow['VARI'], marker='o', label='VARI')
plt.plot(lata, obszary_lasow['GLI'], marker='o', label='GLI')
plt.plot(lata, obszary_lasow['VIGREEN'], marker='o', label='VIGREEN')

plt.title('Procent powierzchni zalesienia w czasie')
plt.xlabel('Rok')
plt.ylabel('Procent powierzchni zalesienia (%)')
plt.ylim(0, 100)
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

print("Zastosowane progi:")
print(progi)


# Wielkospektralna analiza NDVI


pliki_ms = ['1985api.tif', '1993api.tif', '2001api.tif', '2011api.tif']
lata = ['1985', '1993', '2001', '2011']
zalesienie_ndvi = []

for plik in pliki_ms:
    try:
        with rasterio.open(plik) as src:
            red = src.read(3).astype('float32')
            nir = src.read(4).astype('float32')

            # Obliczenie NDVI
            ndvi = (nir - red) / (nir + red + 1e-8)

            # Progowanie
            ndvi_mask = ndvi > 0.2

            zalesienie = np.sum(ndvi_mask) / ndvi.size * 100
            zalesienie_ndvi.append(zalesienie)

            # Wyświetlanie
            plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
            plt.title(f'NDVI {plik}')
            plt.colorbar()
            plt.show()

            plt.imshow(ndvi_mask, cmap='viridis')
            plt.title(f'NDVI Mask {plik}')
            plt.show()

    except Exception as e:
        print(f"Błąd przetwarzania {plik}: {e}")

# Wykres słupkowy dla NDVI
plt.figure(figsize=(10, 6))
plt.bar(lata, zalesienie_ndvi, color='tab:blue')
plt.title('Analiza wylesienia (NDVI)')
plt.xlabel('Lata')
plt.ylabel('Procent powierzchni zalesienia (%)')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()
