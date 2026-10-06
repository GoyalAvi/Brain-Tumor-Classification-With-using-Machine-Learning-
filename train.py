"""Train the VGG16 brain tumor classifier and save it for the Impact Map.

Same pipeline as brain_tumor_detection.py, but with a configurable dataset
path and the trained model saved to disk so it can be reused for inference.

Usage:
    python train.py --dataset ./brain_tumor_dataset --epochs 10
"""

import argparse
import json
import os

import cv2
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import AveragePooling2D, Dense, Dropout, Flatten, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff")


def load_dataset(path):
    images, labels = [], []
    for label in sorted(os.listdir(path)):
        folder = os.path.join(path, label)
        if not os.path.isdir(folder):
            continue
        for name in sorted(os.listdir(folder)):
            if not name.lower().endswith(IMAGE_EXTENSIONS):
                continue
            image = cv2.imread(os.path.join(folder, name))
            if image is None:
                continue
            images.append(cv2.resize(image, (224, 224)))
            labels.append(label)
    return np.array(images) / 255.0, np.array(labels)


def build_model():
    base_model = VGG16(weights="imagenet", input_tensor=Input(shape=(224, 224, 3)), include_top=False)
    x = AveragePooling2D(pool_size=(4, 4))(base_model.output)
    x = Flatten(name="flatten")(x)
    x = Dense(64, activation="relu")(x)
    x = Dropout(0.5)(x)
    x = Dense(2, activation="softmax")(x)
    for layer in base_model.layers:
        layer.trainable = False
    model = Model(inputs=base_model.input, outputs=x)
    model.compile(optimizer=Adam(learning_rate=1e-3), metrics=["accuracy"], loss="binary_crossentropy")
    return model


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dataset", default="./brain_tumor_dataset", help="folder containing 'yes' and 'no' subfolders")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--out", default="models", help="where to save the model and class names")
    args = parser.parse_args()

    images, labels = load_dataset(args.dataset)
    classes = sorted(set(labels))
    if classes != ["no", "yes"]:
        raise SystemExit(f"Expected 'no' and 'yes' subfolders in {args.dataset}, found {classes}")
    print(f"Loaded {len(images)} images: " + ", ".join(f"{c}={int((labels == c).sum())}" for c in classes))

    y = to_categorical([classes.index(label) for label in labels], num_classes=2)
    train_X, test_X, train_Y, test_Y = train_test_split(images, y, test_size=0.10, random_state=42, stratify=y)

    model = build_model()
    train_generator = ImageDataGenerator(fill_mode="nearest", rotation_range=15)
    model.fit(train_generator.flow(train_X, train_Y, batch_size=args.batch_size),
              steps_per_epoch=len(train_X) // args.batch_size,
              validation_data=(test_X, test_Y),
              epochs=args.epochs)

    predictions = np.argmax(model.predict(test_X, batch_size=args.batch_size), axis=1)
    actuals = np.argmax(test_Y, axis=1)
    print(classification_report(actuals, predictions, target_names=classes))
    print(confusion_matrix(actuals, predictions))

    os.makedirs(args.out, exist_ok=True)
    model.save(os.path.join(args.out, "brain_tumor_vgg16.keras"))
    with open(os.path.join(args.out, "classes.json"), "w") as f:
        json.dump(classes, f)
    print(f"Saved model to {args.out}/brain_tumor_vgg16.keras")


if __name__ == "__main__":
    main()
