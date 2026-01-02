from keras_facenet import FaceNet

class FaceNetModel:
    def __init__(self):
        self.model = FaceNet()

    def get_embedding(self, face_img):
        face_img = face_img.astype('float32')
        embedding = self.model.embeddings([face_img])
        return embedding[0]
