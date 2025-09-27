# Brain-Tumor-Classification-With-using-Machine-Learning-
In this machine learning project, we build a classifier to detect the brain tumor (if any) from the MRI scan images. By now it is evident that this is a binary classification problem. Examples of such binary classification problems are Spam or Not spam, Credit card fraud (Fraud or Not fraud).

## Dataset

import kagglehub

# Download latest version
path = kagglehub.dataset_download("navoneel/brain-mri-images-for-brain-tumor-detection")

print("Path to dataset files:", path)

The images are split into two folders yes and no each containing images with and without brain tumors respectively. There are a total of 253 images.
