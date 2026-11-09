from pathlib import Path

import cv2
import keras
import numpy as np

MODEL_PATH = Path(__file__).with_name("digit_model.keras")
DRAWN_DIGIT_PATH = Path(__file__).with_name("drawn_digit.png")

MNIST_IMAGE_SIZE = 28
MNIST_DIGIT_SIZE = 20
INK_THRESHOLD = 40


# Zadanie 1: sieć neuronowa rozpoznająca cyfry ze zbioru MNIST

def to_network_input(images):
    return images.reshape(-1, MNIST_IMAGE_SIZE, MNIST_IMAGE_SIZE, 1).astype("float32") / 255


def build_model():
    model = keras.Sequential([
        keras.Input(shape=(MNIST_IMAGE_SIZE, MNIST_IMAGE_SIZE, 1)),
        keras.layers.Conv2D(32, kernel_size=3, activation="relu"),
        keras.layers.MaxPooling2D(),
        keras.layers.Conv2D(64, kernel_size=3, activation="relu"),
        keras.layers.MaxPooling2D(),
        keras.layers.Flatten(),
        keras.layers.Dropout(0.5),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(10, activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model


def train_model():
    (train_images, train_labels), (test_images, test_labels) = keras.datasets.mnist.load_data()
    model = build_model()
    model.fit(to_network_input(train_images), train_labels, epochs=5, batch_size=128, validation_split=0.1)
    _, test_accuracy = model.evaluate(to_network_input(test_images), test_labels, verbose=0)
    print(f"Dokładność na zbiorze testowym: {test_accuracy:.4f}")
    return model


# Zadanie 2: zapis i odczyt nauczonej sieci (model wraz z wagami)

def load_or_train_model():
    if MODEL_PATH.exists():
        return keras.models.load_model(MODEL_PATH)
    model = train_model()
    model.save(MODEL_PATH)
    return model


# Zadanie 3: klasyfikacja cyfry z narysowanego obrazu

def contains_digit(grayscale_image):
    return bool(np.any(grayscale_image > INK_THRESHOLD))


def center_like_mnist(grayscale_image):
    rows, columns = np.nonzero(grayscale_image > INK_THRESHOLD)
    digit = grayscale_image[rows.min():rows.max() + 1, columns.min():columns.max() + 1]

    scale = MNIST_DIGIT_SIZE / max(digit.shape)
    width, height = max(1, round(digit.shape[1] * scale)), max(1, round(digit.shape[0] * scale))
    digit = cv2.resize(digit, (width, height), interpolation=cv2.INTER_AREA)

    centered = np.zeros((MNIST_IMAGE_SIZE, MNIST_IMAGE_SIZE), dtype=np.uint8)
    top, left = (MNIST_IMAGE_SIZE - height) // 2, (MNIST_IMAGE_SIZE - width) // 2
    centered[top:top + height, left:left + width] = digit
    return centered


def classify(model, grayscale_image):
    probabilities = model(to_network_input(center_like_mnist(grayscale_image)), training=False)[0]
    return int(np.argmax(probabilities))


def classify_image_file(model, image_path):
    return classify(model, cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE))


if __name__ == "__main__":
    model = load_or_train_model()
    print(f"Cyfra na obrazie {DRAWN_DIGIT_PATH.name}: {classify_image_file(model, DRAWN_DIGIT_PATH)}")
