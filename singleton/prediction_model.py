from tensorflow.keras.models import Model, load_model

class PredictionModel(object):
    def __new__(self):
        if not hasattr(self, 'model'):
            self.model = load_model('models/model_v1.h5')
            self.feature_model = Model(self.model.input,self.model.layers[-7].output)
        return self
