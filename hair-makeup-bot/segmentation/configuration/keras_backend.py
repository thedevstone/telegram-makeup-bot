import os


def set_keras_backend(tf=True) -> None:
    """ Set the keras backend

    :param tf: use tensorflow Keras
    """
    if tf:
        os.environ['SM_FRAMEWORK'] = 'tf.keras'
    else:
        os.environ['SM_FRAMEWORK'] = 'keras'
