import tensorflow as tf
import numpy as np


def shape_list(x):
    static = x.shape.as_list()
    dynamic = tf.shape(x)
    return [dynamic[i] if s is None else s for i, s in enumerate(static)]


class MimicCnn(tf.keras.Model):
    def __init__(self, n_features=16, n_layers=18, **kwargs):
        super().__init__(**kwargs)
        self.n_features = n_features

        self.conv1d = tf.keras.layers.Conv1D(16, 3, activation='relu')
        self.attn = tf.keras.layers.Dense(16, activation='softmax')
        self.conv2ds = list(self.init_conv2ds(n_layers=n_layers))
        self.proj1 = tf.keras.layers.Dense(64, activation='relu')
        self.drop1 = tf.keras.layers.Dropout(0.5)
        self.proj2 = tf.keras.layers.Dense(16, activation='relu')
        self.proj3 = tf.keras.layers.Dense(1, activation='sigmoid')

    def init_conv2ds(self, n_layers=18):
        filters = 16
        for i in range(n_layers):
            if i != 0 and i % 4 == 0:
                filters = filters * 2

            yield tf.keras.layers.Conv2D(
                filters=filters,
                kernel_size=(3, 3),
                padding='same',
                activation='relu',
            )

    def call(self, x, training=False):
        # input shape sanity check
        # model expects an input of shape: (batch_size, n_features)
        batch_size, n_features = shape_list(x)
        assert n_features == self.n_features

        # get weights for embedding-level attention
        w = self.attn(x)
        x = x * w

        x = x[:, :, tf.newaxis]
        x = self.conv1d(x)
        x = x[:, :, :, tf.newaxis]

        # let x go through `n_layers` layers of Conv2D blocks
        for conv2d in self.conv2ds:
            x = conv2d(x)

        x = tf.reshape(x, (batch_size, -1))
        x = self.proj1(x)
        x = self.drop1(x, training=training)
        x = self.proj2(x)
        x = self.proj3(x)

        return x, w
