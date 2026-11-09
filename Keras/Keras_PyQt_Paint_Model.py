
# Zadanie 4: implementacja obsługi ładowania i predykcji modelu

import numpy as np

from PyQt6.QtGui import QImage

from keras_digits import classify, contains_digit, load_or_train_model

def qimage_to_array(image: QImage):
    """
    Funkcja konwertująca obiekt QImage do numpy array
    """
    image = image.convertToFormat(QImage.Format.Format_Grayscale8)
    ptr = image.bits()
    ptr.setsize(image.sizeInBytes())
    numpy_array = np.array(ptr).reshape(image.height(), image.bytesPerLine())[:, :image.width()]
    return numpy_array


def predict(image: QImage, model):
    """
    Funkcja wykorzystująca załadowany model sieci neuronowej do predykcji znaku na obrazie
    """
    numpy_array = qimage_to_array(image)
    if not contains_digit(numpy_array):
        return ""
    return classify(model, numpy_array)


def get_model():
    """
    Funkcja wczytująca nauczony model sieci neuronowej
    """
    return load_or_train_model()
