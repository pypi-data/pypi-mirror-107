import numpy as np
import tensorflow as tf
from tensorflow.keras import datasets
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras.applications import MobileNet
from aibro.train import fit
from aibro.train import retrain
from aibro.train import retrain_with_new_data
from aibro.train import retrain_with_new_model
# GPU_type = "K80"
# num_GPU = 1
# batch_size = 1
# epochs = 1
# job_id = "312b4f46-e78f-420a-9cd3-13de319ab1ed"
# retrain(job_id, GPU_type, num_GPU, batch_size, epochs, resume=True)
# (train_images, train_labels), (test_images, test_labels) = datasets.cifar10.load_data()
# # Normalize pixel values to be between 0 and 1
# train_images, test_images = train_images / 255.0, test_images / 255.0
# model = models.Sequential()
# model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(32, 32, 3)))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation="relu"))
# model.add(layers.MaxPooling2D((2, 2)))
# model.add(layers.Conv2D(64, (3, 3), activation="relu"))
# model.add(layers.Flatten())
# model.add(layers.Dense(64, activation="relu"))
# model.add(layers.Dense(10))
# model.compile(
#     optimizer="adam",
#     loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
#     metrics=["accuracy"],
# )
# fit(
#     model,
#     train_X=train_images,
#     train_Y=train_labels,
#     validation_X=test_images,
#     validation_Y=test_labels,
#     GPU_type="K80",
#     num_GPU=1,
#     batch_size=1,
#     epochs=3,
# )
TRAINING_SIZE = 10
def _get_random_train_data(h, w, c):
    # Generate some random training data that match the input shape
    random_x_train = np.random.rand(TRAINING_SIZE, h, w, c)
    random_y_train = tf.one_hot([i for i in range(0, TRAINING_SIZE)], 100)
    return random_x_train, random_y_train
model = MobileNet(weights=None, classes=100)
model.compile(loss="categorical_crossentropy", optimizer="sgd", metrics=["accuracy"])
train_X, train_Y = _get_random_train_data(224, 224, 3)
validation_X, validation_Y = _get_random_train_data(224, 224, 3)
fit(
    model=model,
    train_X=train_X,
    train_Y=train_Y,
    validation_X=validation_X,
    validation_Y=validation_Y,
    machine_id='g4dn.4xlarge',
    batch_size=1,
    epochs=3,
)
from aibro.train import get_tensorboard_logs

# get_tensorboard_logs()
# # retrain_with_new_model(
# #     job_id="312b4f46-e78f-420a-9cd3-13de319ab1ed",
# #     GPU_type="K80",
# #     num_GPU=1,
# #     batch_size=1,
# #     epochs=3,
# #     model=model,
# # )
# # retrain_with_new_data(
# #     job_id="312b4f46-e78f-420a-9cd3-13de319ab1ed",
# #     GPU_type="K80",
# #     num_GPU=1,
# #     batch_size=1,
# #     epochs=3,
# #     train_X=train_X,
# #     train_Y=train_Y,
# #     validation_X=validation_X,
# #     validation_Y=validation_Y,
# #     description="retraining model with new data",
# # )

