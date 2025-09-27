# Brain Tumor Detection using CNN & Transfer Learning 🧠

This project implements a deep learning model to classify brain MRI scans for the presence of a tumor. It's a binary classification task that distinguishes between images containing a tumor ('yes') and those without ('no'). The model leverages a Convolutional Neural Network (CNN) with transfer learning for high accuracy, even with a relatively small dataset.

-----

## 🛠️ Technology Stack

The project is built using Python and several key data science and machine learning libraries:

  * **Python** 3.x
  * **TensorFlow** 2.4.1
  * **Keras** 2.4.0
  * **Scikit-learn** 0.24.1
  * **OpenCV** 4.5.2
  * **NumPy** 1.19.2
  * **Matplotlib** 3.3.4

-----

## 📖 Dataset

The model is trained on the **Brain Tumor Classification Dataset**, which contains a total of 253 MRI images.

  * **'yes' folder:** 155 images with brain tumors.
  * **'no' folder:** 98 images without brain tumors.

You can download the dataset from here: [Brain Tumor Dataset](https://www.kaggle.com/datasets/navoneel/brain-mri-images-for-brain-tumor-detection).

-----

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

Ensure you have Python 3 installed. You can install all the necessary libraries using the `requirements.txt` file.

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/brain-tumor-classification.git
    cd brain-tumor-classification
    ```

2.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

    *(Note: A `requirements.txt` file should be created with the libraries and versions listed above.)*

3.  **Organize the dataset:**

      * Download the dataset from the link above.
      * Create a directory named `brain_tumor_dataset` in the project's root folder.
      * Place the `yes` and `no` folders inside the `brain_tumor_dataset` directory.

-----

## 💻 Project Workflow

The project follows a standard machine learning pipeline:

### 1\. Data Preprocessing & Augmentation

  * **Image Loading:** Images from the `yes` and `no` directories are loaded using OpenCV.
  * **Resizing & Normalization:** All images are resized to `224x224` pixels and their pixel values are normalized to a range of `[0, 1]` for better model performance.
  * **Label Encoding:** The categorical labels ('yes', 'no') are converted into a one-hot encoded format.
  * **Data Augmentation:** To prevent overfitting and expand the small dataset, `ImageDataGenerator` is used to apply random rotations and transformations to the training images, creating more varied data.

### 2\. Model Architecture (Transfer Learning)

  * **Base Model:** We use the **VGG16** model, pre-trained on the ImageNet dataset, as the convolutional base for feature extraction. The final, fully connected layer of VGG16 is removed.
  * **Custom Head:** A new classification head is added on top of the VGG16 base. This head consists of:
      * An `AveragePooling2D` layer to reduce spatial dimensions.
      * A `Flatten` layer to convert the feature maps into a 1D vector.
      * A `Dense` layer with `ReLU` activation.
      * A `Dropout` layer to prevent overfitting.
      * A final `Dense` layer with `Softmax` activation for binary classification output.
  * **Freezing Layers:** The layers of the VGG16 base are frozen, so their weights are not updated during training. This ensures we only train the weights of our custom classifier head, significantly reducing training time.

### 3\. Training & Evaluation

  * **Compilation:** The model is compiled using the **Adam optimizer**, with `binary_crossentropy` as the loss function and `accuracy` as the evaluation metric.
  * **Training:** The model is trained for **10 epochs** with a batch size of 8.
  * **Evaluation:** After training, the model's performance is evaluated on the test set using a **classification report** and a **confusion matrix** to assess precision, recall, and F1-score for each class.

-----

## 📊 Results

The model achieved a final accuracy of **96.5%** on the test dataset. The training history below shows the model's loss and accuracy curves over 10 epochs, demonstrating stable learning and good generalization on the validation set.

The classification report confirms strong performance, with high precision and recall for both classes.

```
              precision    recall  f1-score   support

          no       0.91      1.00      0.95        10
         yes       1.00      0.93      0.97        16

    accuracy                           0.96        26
   macro avg       0.95      0.97      0.96        26
weighted avg       0.96      0.96      0.96        26

Confusion Matrix:
[[10  0]
 [ 1 15]]
```
Now, let’s find the overall accuracy of the model using the formula: (TP + TN) / (TP + FN + FN + TN)
```
total = sum(sum(cm))
accuracy = (cm[0, 0] + cm[1, 1]) / total
print("Accuracy: {:.4f}".format(accuracy))
```

## Summary
```
Brain tumor classification is a highly important healthcare project in machine learning. It helps doctors identify if a brain scan shows a tumor and what type it is—benign or malignant. The dataset usually contains MRI (Magnetic Resonance Imaging) scans of brains with labels. Using these images, a deep learning model can be trained to detect tumors, which helps in faster and more accurate diagnosis.

In brain tumor classification using machine learning, we built a binary classifier to detect brain tumors from MRI scan images. We built our classifier using transfer learning and obtained an accuracy of 96.5% and visualized our model’s overall performance.
```

