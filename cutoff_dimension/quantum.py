"""Hybrid Network Models 2022"""
from data import generate_synthetic_dataset
from keras import Model, layers, models, regularizers
from keras.callbacks import Callback
from sacred import Experiment
from sacred.observers import FileStorageObserver
from sacred.utils import apply_backspaces_and_linefeeds
from tensorflow.random import set_seed

from common_packages.CV_quantum_layers import (
    Activation_Layer,
    CV_Measurement,
    QuantumLayer_MultiQunode,
)
from common_packages.utilities import get_regularizer

EXPERIMENT_NAME = "cutoff_hybrid_with_trace"
ex = Experiment(EXPERIMENT_NAME)
ex.observers.append(FileStorageObserver(f"Experiment_{EXPERIMENT_NAME}"))
ex.captured_out_filter = apply_backspaces_and_linefeeds


@ex.capture
def log_performance(_run, logs, epoch, traces):
    """Logs performance with sacred framework"""
    _run.log_scalar("loss", float(logs.get("loss")), epoch)
    _run.log_scalar("accuracy", float(logs.get("accuracy")), epoch)
    _run.log_scalar("val_loss", float(logs.get("val_loss")), epoch)
    _run.log_scalar("val_accuracy", float(logs.get("val_accuracy")), epoch)
    _run.log_scalar("epoch", int(epoch), epoch)
    _run.log_scalar("traces", traces, epoch)


class LogPerformance(Callback):
    """Logs performance"""

    def on_epoch_end(self, epoch, logs=None):
        """Log key metrics on epoch end"""
        log_performance(logs=logs, epoch=epoch, traces=self.model.quantum_layer.traces)
        self.model.quantum_layer.traces = []


@ex.config
def confnet_config():
    """Default config"""
    quantum_preparation_layer = True
    regularizer_string = None
    scale_max = 6


@ex.automain
def define_and_train(quantum_preparation_layer, regularizer_string, scale_max):
    """Build and run the network"""

    set_seed(30)

    class Net(Model):
        """Neural network model to train on"""

        def __init__(self):
            super(Net, self).__init__()

            self.base_model = models.Sequential(
                [
                    layers.Dense(
                        10,
                        input_dim=10,
                        activation="relu",
                    ),
                    layers.Dense(
                        6,
                        activation=None,
                    ),
                ]
            )

            self.quantum_layer = QuantumLayer_MultiQunode(
                n_qumodes=3,
                n_circuits=1,
                n_layers=1,
                cutoff_dim=5,
                encoding_method="Amplitude_Phase",
                regularizer=get_regularizer(regularizer_string),
                max_initial_weight=None,
                measurement_object=CV_Measurement("X_quadrature"),
                trace_tracking=True,
                shots=None,
                scale_max=scale_max,
            )

            if quantum_preparation_layer:
                self.quantum_preparation_layer = Activation_Layer(
                    "Sigmoid", self.quantum_layer.encoding_object
                )

            self.final_layer = models.Sequential(
                [
                    layers.Dense(
                        3,
                        activation="softmax",
                    ),
                ]
            )

        def call(self, inputs, training=None, mask=None):
            """Call the network"""
            output = self.base_model(inputs)
            if quantum_preparation_layer:
                output = self.quantum_preparation_layer(output)
            output = self.quantum_layer(output)
            output = self.final_layer(output)
            return output

    train_data, validate_data, _ = generate_synthetic_dataset()
    model = Net()
    model.compile(
        optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"]
    )
    model.fit(
        *train_data,
        epochs=50,
        batch_size=36,
        validation_data=validate_data,
        callbacks=[LogPerformance()],
    )
