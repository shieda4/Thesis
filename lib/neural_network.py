from tensorflow.keras.layers import Input, Conv2D, BatchNormalization, Activation, Add, Flatten, Dense, Reshape
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
import numpy as np


class Residual(object):
    def __init__(self):
        self.model = self.build()
        self.compile()
        pass

    def build(self):
        input_x = Input((8, 8))
        x = Reshape((8, 8, 1))(input_x)
        x = Conv2D(filters=256, kernel_size=[3, 3],
                   padding="same",
                   strides=1)(x)
        x = BatchNormalization()(x)
        x = Activation(activation='relu')(x)

        # Residual Block
        for i in range(5):
            x = self.build_residual_block(x)

        residual_out = x

        # Policy
        x = Conv2D(filters=2, kernel_size=1, padding="same", strides=1)(residual_out)
        x = BatchNormalization()(x)
        x = Activation(activation='relu')(x)
        x = Flatten()(x)
        policy = Dense(activation='softmax', units=280)(x)

        # Value
        x = Conv2D(filters=4, kernel_size=1, padding="same", strides=1)(residual_out)
        x = BatchNormalization()(x)
        x = Activation(activation='relu')(x)
        x = Flatten()(x)
        value = Dense(activation='tanh', units=1)(x)

        return Model(input_x, [policy, value], name="Residual_Network")

        pass

    def build_residual_block(self, x):
        input_x = x
        x = Conv2D(filters=256, kernel_size=[3, 3], padding="same", strides=1)(x)
        x = BatchNormalization()(x)
        x = Activation(activation='relu')(x)
        x = Conv2D(filters=256, kernel_size=[3, 3], padding="same", strides=1)(x)
        x = BatchNormalization()(x)
        x = Add()([input_x, x])
        x = Activation(activation='relu')(x)
        return x

    def compile(self):
        opt = Adam()
        losses = ['categorical_crossentropy', 'mean_squared_error']
        self.model.compile(optimizer=opt, loss=losses, metrics=['accuracy'])

    def predict(self, state):
        return self.model.predict(np.expand_dims(state, axis=0))

    def save_model(self, filename):
        self.model.save(filename)
        print('Model saved to models')
        pass

    def fit_model(self, data):
        data = data[0] + data[1]
        states = np.asanyarray([d[0] for d in data])
        policies = np.asanyarray([d[1] for d in data])
        values = np.asanyarray([d[2] for d in data])
        self.model.fit(states, [policies, values], batch_size=32, epochs=10)

        pass

    def load_model(self, filename):
        self.model = load_model(filename)
        pass

    def evaluate(self, data):
        data = data[0] + data[1]
        states = np.asanyarray([d[0] for d in data])
        policies = np.asanyarray([d[1] for d in data])
        values = np.asanyarray([d[2] for d in data])
        self.model.evaluate(states, [policies, values], batch_size=32)
