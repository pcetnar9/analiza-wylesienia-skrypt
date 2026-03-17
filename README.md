Analiza Wylesiania na Podstawie Zdjęć Satelitarnych
![Python](https://img.shields.io/badge/python-3.x-blue.svg)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?logo=opencv&logoColor=white)
![Matplotlib](https://img.shields.io/badge/matplotlib-%23ffffff.svg?logo=Matplotlib&logoColor=black)
![Rasterio](https://img.shields.io/badge/rasterio-geospatial-green.svg)


Projekt ten zawiera skrypty w języku Python służące do automatycznej analizy zmian zakresu zalesienia na przestrzeni lat (1985, 1993, 2001, 2011). Badania opierają się na przetwarzaniu obrazów satelitarnych w celu identyfikacji postępującego wylesiania.

Analiza została podzielona na dwa główne moduły:
1. **Analiza zdjęć RGB:** Wykorzystanie widzialnych indeksów roślinności (VARI, GLI, VIGREEN) na standardowych obrazach.
2. **Analiza zdjęć wielospektralnych:** Wyliczenie znormalizowanego wskaźnika wegetacji (NDVI) z wykorzystaniem kanału bliskiej podczerwieni (NIR).

Funkcjonalności:
- **Pre-processing:** Wyrównywanie histogramu zdjęć w przestrzeni barw HSV w celu poprawy wizualizacji.
- **Obliczenia matematyczne:** Generowanie map ciągłych dla wskaźników VARI, GLI, VIGREEN oraz NDVI.
- **Segmentacja:** Progowanie (thresholding) map indeksów w celu wygenerowania binarnych masek zalesienia (roślinność / brak roślinności).
- **Wizualizacja danych:** Zliczanie procentowego udziału lasów w całkowitej powierzchni i generowanie wykresów trendów (Matplotlib).

 Wymagania i instalacja
Skrypty wymagają środowiska Python oraz kilku bibliotek do przetwarzania obrazów i danych przestrzennych. Instalacja zależności:

```bash
pip install opencv-python numpy matplotlib rasterio
