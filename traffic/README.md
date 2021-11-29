## For all runs:
- Optimizer: "adam"
- Loss: "categorical_crossentropy"
- Metrics: "accuracy"

```
model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss=tf.keras.losses.CategoricalCrossentropy(),
    metrics=tf.keras.metrics.Accuracy(),
)
```

## Run 1:
- Input layer (32).
- 1 Conv2D layer (64).
- 1 MaxPooling2D layer.
- 1 Hidden layer (64).
- 1 Dropout.
- 1 Flatten.
- Output layer (NUM_CATEGORIES/43).

```
model = keras.Sequential(
    [
        layers.Dense(32, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), activation="relu", name="input"),

        layers.Conv2D(64, (2, 2), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dense(64, activation="relu"),

        layers.Dropout(0.5),
        layers.Flatten(),

        layers.Dense(NUM_CATEGORIES, activation="softmax", name="output")
    ]
)
```

```bash
Epoch 1/10
500/500 [==============================] - 41s 79ms/step - loss: 2.9817 - accuracy: 0.6217
Epoch 2/10
500/500 [==============================] - 33s 66ms/step - loss: 0.5533 - accuracy: 0.8474
Epoch 3/10
500/500 [==============================] - 35s 71ms/step - loss: 0.4153 - accuracy: 0.8867
Epoch 4/10
500/500 [==============================] - 35s 70ms/step - loss: 0.3346 - accuracy: 0.9088
Epoch 5/10
500/500 [==============================] - 43s 86ms/step - loss: 0.2652 - accuracy: 0.9274
Epoch 6/10
500/500 [==============================] - 37s 74ms/step - loss: 0.2731 - accuracy: 0.9290
Epoch 7/10
500/500 [==============================] - 35s 71ms/step - loss: 0.2400 - accuracy: 0.9376
Epoch 8/10
500/500 [==============================] - 36s 71ms/step - loss: 0.1711 - accuracy: 0.9519
Epoch 9/10
500/500 [==============================] - 49s 98ms/step - loss: 0.1775 - accuracy: 0.9532
Epoch 10/10
500/500 [==============================] - 35s 71ms/step - loss: 0.1423 - accuracy: 0.9618
333/333 - 4s - loss: 0.1818 - accuracy: 0.9604

```

## Run 2 (Implemented configuration):
- Input layer (16).
- 1 Conv2D layer (32).
- 1 MaxPooling2D layer.
- 1 Hidden layer (64).
- 1 Dropout.
- 1 Flatten.
- Output layer (NUM_CATEGORIES/43).

```
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
```

```bash
Epoch 1/10
500/500 [==============================] - 17s 32ms/step - loss: 3.5232 - accuracy: 0.6554
Epoch 2/10
500/500 [==============================] - 18s 37ms/step - loss: 0.4019 - accuracy: 0.8913
Epoch 3/10
500/500 [==============================] - 22s 44ms/step - loss: 0.2576 - accuracy: 0.9288
Epoch 4/10
500/500 [==============================] - 22s 43ms/step - loss: 0.2464 - accuracy: 0.9355
Epoch 5/10
500/500 [==============================] - 20s 40ms/step - loss: 0.1815 - accuracy: 0.9480
Epoch 6/10
500/500 [==============================] - 17s 35ms/step - loss: 0.1876 - accuracy: 0.9496
Epoch 7/10
500/500 [==============================] - 21s 41ms/step - loss: 0.1698 - accuracy: 0.9549
Epoch 8/10
500/500 [==============================] - 20s 40ms/step - loss: 0.1547 - accuracy: 0.9601
Epoch 9/10
500/500 [==============================] - 17s 34ms/step - loss: 0.1519 - accuracy: 0.9601
Epoch 10/10
500/500 [==============================] - 16s 32ms/step - loss: 0.1547 - accuracy: 0.9606
333/333 - 2s - loss: 0.1588 - accuracy: 0.9633
```

Considerations: 
- Similar accuracy compared with the first run but considerably faster (doubles as fast) in the execution.

## Run 3:
- Input layer (16).
- 1 Conv2D layer (32).
- 1 MaxPooling2D layer.
- 1 Hidden layer (64).
- Second Conv2D layer (64).
- Second MaxPooling2D layer.
- Second Hidden layer (128).
- Dropout.
- Flatten.
- Output layer (NUM_CATEGORIES/43).

```
model = keras.Sequential(
    [
        layers.Dense(16, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), activation="relu", name="input"),

        layers.Conv2D(32, (2, 2), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dense(64, activation="relu"),

        layers.Conv2D(64, (2, 2), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dense(128, activation="relu"),

        layers.Dropout(0.5),
        layers.Flatten(),

        layers.Dense(NUM_CATEGORIES, activation="softmax", name="output")
    ]
)
```

```bash
Epoch 1/10
500/500 [==============================] - 29s 56ms/step - loss: 1.6202 - accuracy: 0.6415  
Epoch 2/10
500/500 [==============================] - 36s 72ms/step - loss: 0.3609 - accuracy: 0.8928
Epoch 3/10
500/500 [==============================] - 36s 71ms/step - loss: 0.2106 - accuracy: 0.9383
Epoch 4/10
500/500 [==============================] - 38s 75ms/step - loss: 0.1759 - accuracy: 0.9489
Epoch 5/10
500/500 [==============================] - 37s 73ms/step - loss: 0.1350 - accuracy: 0.9599
Epoch 6/10
500/500 [==============================] - 29s 58ms/step - loss: 0.1088 - accuracy: 0.9662
Epoch 7/10
500/500 [==============================] - 29s 58ms/step - loss: 0.1152 - accuracy: 0.9674
Epoch 8/10
500/500 [==============================] - 28s 55ms/step - loss: 0.0893 - accuracy: 0.9737
Epoch 9/10
500/500 [==============================] - 28s 56ms/step - loss: 0.1029 - accuracy: 0.9703
Epoch 10/10
500/500 [==============================] - 24s 49ms/step - loss: 0.0888 - accuracy: 0.9743
333/333 - 2s - loss: 0.1113 - accuracy: 0.9788
```

Considerations: 
- Higher accuracy compared with the previous 2 runs, with execution time somewhere in between.


## Run 4:
- Input layer (16).
- 1 Conv2D layer (32).
- 1 MaxPooling2D layer.
- 1 Hidden layer (64).
- Second Conv2D layer (128).
- Second MaxPooling2D layer.
- Second Hidden layer (256).
- Dropout.
- Flatten.
- Output layer (NUM_CATEGORIES/43).

```
model = keras.Sequential(
    [
        layers.Dense(16, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), activation="relu", name="input"),

        layers.Conv2D(32, (2, 2), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dense(64, activation="relu"),

        layers.Conv2D(128, (2, 2), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dense(256, activation="relu"),

        layers.Dropout(0.5),
        layers.Flatten(),

        layers.Dense(NUM_CATEGORIES, activation="softmax", name="output")
    ]
)
```

```bash
Epoch 1/10
500/500 [==============================] - 56s 109ms/step - loss: 1.6184 - accuracy: 0.6727
Epoch 2/10
500/500 [==============================] - 44s 88ms/step - loss: 0.3211 - accuracy: 0.9067
Epoch 3/10
500/500 [==============================] - 40s 79ms/step - loss: 0.1845 - accuracy: 0.9476
Epoch 4/10
500/500 [==============================] - 24s 49ms/step - loss: 0.1533 - accuracy: 0.9555
Epoch 5/10
500/500 [==============================] - 23s 46ms/step - loss: 0.1189 - accuracy: 0.9654
Epoch 6/10
500/500 [==============================] - 23s 45ms/step - loss: 0.1104 - accuracy: 0.9681
Epoch 7/10
500/500 [==============================] - 23s 45ms/step - loss: 0.0924 - accuracy: 0.9743
Epoch 8/10
500/500 [==============================] - 26s 52ms/step - loss: 0.0868 - accuracy: 0.9760
Epoch 9/10
500/500 [==============================] - 31s 62ms/step - loss: 0.0710 - accuracy: 0.9797
Epoch 10/10
500/500 [==============================] - 30s 59ms/step - loss: 0.0854 - accuracy: 0.9767
333/333 - 4s - loss: 0.0808 - accuracy: 0.9820
```

Considerations: 
- Merely doubling the units of the second Conv2D and Dense layers didn't seem to have significantly affected the outcome.

## Run 5:
- Input layer (16).
- 1 Conv2D layer (32).
- 1 MaxPooling2D layer.
- 1 Hidden layer (64).
- Second Hidden layer (128).
- 1 Dropout.
- 1 Flatten.
- Output layer (NUM_CATEGORIES/43).

```
model = keras.Sequential(
    [
        layers.Dense(16, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), activation="relu", name="input"),

        layers.Conv2D(32, (2, 2), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dense(64, activation="relu"),
        layers.Dense(126, activation="relu"),

        layers.Dropout(0.5),
        layers.Flatten(),

        layers.Dense(NUM_CATEGORIES, activation="softmax", name="output")
    ]
)
```

```bash
Epoch 1/10
500/500 [==============================] - 29s 56ms/step - loss: 2.7225 - accuracy: 0.7196 
Epoch 2/10
500/500 [==============================] - 27s 55ms/step - loss: 0.2532 - accuracy: 0.9311
Epoch 3/10
500/500 [==============================] - 31s 63ms/step - loss: 0.1619 - accuracy: 0.9531
Epoch 4/10
500/500 [==============================] - 31s 62ms/step - loss: 0.1520 - accuracy: 0.9573
Epoch 5/10
500/500 [==============================] - 23s 46ms/step - loss: 0.1194 - accuracy: 0.9657
Epoch 6/10
500/500 [==============================] - 23s 46ms/step - loss: 0.0969 - accuracy: 0.9720
Epoch 7/10
500/500 [==============================] - 21s 42ms/step - loss: 0.0877 - accuracy: 0.9758
Epoch 8/10
500/500 [==============================] - 26s 52ms/step - loss: 0.0997 - accuracy: 0.9723
Epoch 9/10
500/500 [==============================] - 23s 46ms/step - loss: 0.0805 - accuracy: 0.9763
Epoch 10/10
500/500 [==============================] - 22s 44ms/step - loss: 0.0590 - accuracy: 0.9833
333/333 - 2s - loss: 0.1404 - accuracy: 0.9703
```

Considerations: 
- Accuracy is very high and higher than the test accuracy (possible over-fitting?).

## Run 6:
- Same as run 2 but with sigmoid activation for the output layer.

```
model = keras.Sequential(
    [
        layers.Dense(16, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3), activation="relu", name="input"),

        layers.Conv2D(32, (2, 2), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Dense(64, activation="relu"),

        layers.Dropout(0.5),
        layers.Flatten(),

        layers.Dense(NUM_CATEGORIES, activation="sigmoid", name="output")
    ]
)
```

```bash
Epoch 1/10
500/500 [==============================] - 16s 30ms/step - loss: 2.0685 - accuracy: 0.6954 
Epoch 2/10
500/500 [==============================] - 16s 32ms/step - loss: 0.2885 - accuracy: 0.9193
Epoch 3/10
500/500 [==============================] - 14s 29ms/step - loss: 0.2042 - accuracy: 0.9433
Epoch 4/10
500/500 [==============================] - 17s 33ms/step - loss: 0.1412 - accuracy: 0.9608
Epoch 5/10
500/500 [==============================] - 19s 38ms/step - loss: 0.1451 - accuracy: 0.9607
Epoch 6/10
500/500 [==============================] - 17s 35ms/step - loss: 0.1238 - accuracy: 0.9673
Epoch 7/10
500/500 [==============================] - 16s 31ms/step - loss: 0.0939 - accuracy: 0.9736
Epoch 8/10
500/500 [==============================] - 15s 30ms/step - loss: 0.1262 - accuracy: 0.9675
Epoch 9/10
500/500 [==============================] - 19s 38ms/step - loss: 0.1126 - accuracy: 0.9703
Epoch 10/10
500/500 [==============================] - 16s 31ms/step - loss: 0.0768 - accuracy: 0.9793
333/333 - 2s - loss: 0.1610 - accuracy: 0.9696
```

Considerations:
- The outcome is not too dissimilar from run 2 (softmax activation for output layer).
