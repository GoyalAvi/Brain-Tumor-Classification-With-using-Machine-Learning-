"""Load the trained classifier, predict, and compute a Grad-CAM heatmap."""

import json
import os

import cv2
import numpy as np
import tensorflow as tf

IMAGE_SIZE = 224


def load_image(path):
    """Read an image exactly the way train.py does (OpenCV BGR, 224x224, scaled to [0, 1])."""
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE)).astype("float32") / 255.0


def load_classifier(model_dir="models"):
    model = tf.keras.models.load_model(os.path.join(model_dir, "brain_tumor_vgg16.keras"))
    with open(os.path.join(model_dir, "classes.json")) as f:
        classes = json.load(f)
    return model, classes


def last_conv_layer_name(model):
    for layer in reversed(model.layers):
        if isinstance(layer, tf.keras.layers.Conv2D):
            return layer.name
    raise ValueError("Model has no Conv2D layer for Grad-CAM")


def predict_with_gradcam(model, classes, image, target_class="yes"):
    """Return (class probabilities, Grad-CAM heatmap in [0, 1] at image resolution)."""
    grad_model = tf.keras.Model(model.inputs,
                                [model.get_layer(last_conv_layer_name(model)).output, model.output])
    x = tf.convert_to_tensor(image[None])
    with tf.GradientTape() as tape:
        conv, preds = grad_model(x)
        score = preds[:, classes.index(target_class)]
    grads = tape.gradient(score, conv)[0]
    weights = tf.reduce_mean(grads, axis=(0, 1))
    cam = tf.nn.relu(tf.reduce_sum(conv[0] * weights, axis=-1)).numpy()
    cam = cv2.resize(cam, (image.shape[1], image.shape[0]))
    if cam.max() > 0:
        cam = cam / cam.max()
    probabilities = {c: float(p) for c, p in zip(classes, preds[0].numpy())}
    return probabilities, cam
