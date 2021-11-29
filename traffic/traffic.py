
import os
import sys
import numpy as np
import cv2.cv2 as cv2
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = list()
    labels = list()

    for sub_dir in os.listdir(data_dir):
        for filename in os.listdir(os.path.join(data_dir, sub_dir)):
            with open(os.path.join(data_dir, sub_dir, filename)) as file:
                image = cv2.imread(file.name)
                resized = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))

                images.append(resized)
                labels.append(int(sub_dir))

    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = keras.Sequential(
        [
            layers.Dense(16, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), activation="relu", name="input"),

            layers.Conv2D(32, (2, 2), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Dense(64, activation="relu"),

            layers.Dropout(0.5),
            layers.Flatten(),

            layers.Dense(NUM_CATEGORIES, activation="softmax", name="output")
        ]
    )

    model.summary()

    model.compile(
        optimizer=keras.optimizers.Adam(),
        loss=keras.losses.CategoricalCrossentropy(),
        metrics=keras.metrics.Accuracy(),
    )

    return model


if __name__ == "__main__":
    main()
