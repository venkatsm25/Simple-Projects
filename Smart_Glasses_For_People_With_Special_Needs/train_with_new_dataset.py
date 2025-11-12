# Mook Mitra - New Model Training Script
# This script is designed to train a new, more accurate model using the Kaggle ISL dataset (A-Z, 0-9).
# RUN THIS SCRIPT WHENEVER YOU ARE READY TO TRAIN.

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
import os

def train_new_model():
    """
    Defines, compiles, and trains a new CNN model based on the Kaggle dataset structure.
    """
    print("Starting the training process for the new, enhanced model...")

    # --- 1. Data Augmentation and Loading ---
    # This creates more varied training data from your existing images to make the model more robust.
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2  # Use 20% of the data for validation
    )

    # The directory where you have placed the Kaggle dataset (e.g., SIH25/data/)
    DATA_DIR = 'data'
    IMAGE_SIZE = (64, 64) # The new dataset uses a more efficient 64x64 size
    BATCH_SIZE = 32
    
    # Check if the data directory exists
    if not os.path.exists(DATA_DIR):
        print(f"[ERROR] Data directory not found at '{DATA_DIR}'.")
        print("Please create a 'data' folder and organize your Kaggle images into subfolders (e.g., 'A', 'B', '0', '1').")
        return

    print(f"Loading training data from '{DATA_DIR}'...")
    train_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training' # Set as training data
    )

    print(f"Loading validation data from '{DATA_DIR}'...")
    validation_generator = datagen.flow_from_directory(
        DATA_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation' # Set as validation data
    )

    # The number of classes (A-Z, 0-9) is automatically detected from the number of subfolders.
    num_classes = train_generator.num_classes
    print(f"Detected {num_classes} classes (signs) in the dataset.")

    # --- 2. Model Architecture ---
    # A robust CNN architecture suitable for this task.
    model = Sequential([
        # The model expects color images, so the input shape has 3 channels.
        Conv2D(32, (3, 3), activation='relu', input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3)),
        MaxPooling2D(2, 2),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5), # Dropout helps prevent overfitting
        Dense(num_classes, activation='softmax') # The final layer has an output for each class
    ])

    model.summary()

    # --- 3. Compile the Model ---
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # --- 4. Train the Model ---
    print("\nStarting model training... This will take some time.")
    EPOCHS = 25 # You can increase this for better accuracy if you have time
    model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator
    )

    # --- 5. Save the Final Model ---
    # The trained model will be saved and ready to use in your application.
    if not os.path.exists('model'):
        os.makedirs('model')
    model.save('model/new_kaggle_model.h5')
    print("\nTraining complete! The new model has been saved to 'model/new_kaggle_model.h5'")


if __name__ == '__main__':
    train_new_model()
