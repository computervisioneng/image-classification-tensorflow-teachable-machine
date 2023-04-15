import os

from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from sklearn.metrics import accuracy_score


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()
category_to_index = {}
for class_name in class_names:
    index, name = class_name.split(' ')
    name = name[:-1]
    category_to_index[name] = int(index)

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

predictions = []
labels = []
root_dir = '/media/veracrypt2/computer_vision/44_yolov8_image_classification_custom_data/code/data/weather_dataset/val'
for dir_ in os.listdir(root_dir):
    for j in os.listdir(os.path.join(root_dir, dir_)):
        image_path = os.path.join(root_dir, dir_, j)

        # Replace this with the path to your image
        image = Image.open(image_path).convert("RGB")

        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # Predicts the model
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        predictions.append(index)
        labels.append(category_to_index[dir_])

        # Print prediction and confidence score
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", confidence_score)

print(accuracy_score(predictions, labels))
