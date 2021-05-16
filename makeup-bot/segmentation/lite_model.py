import tensorflow

from file_manager.path_utilities import get_model_path


class LiteModel:
    def __init__(self, model_name):
        self.interpreter = tensorflow.lite.Interpreter(model_path=get_model_path(model_name))
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def predict(self, image):
        self.interpreter.set_tensor(self.input_details[0]['index'], image)
        self.interpreter.invoke()
        images_predicted = self.interpreter.get_tensor(self.output_details[0]['index'])
        return images_predicted
