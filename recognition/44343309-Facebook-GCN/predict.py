"""
Author: Remington Greenhill-Brown
SN: 44343309
"""
from modules import *
from dataset import *
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
#from sklearn.metrics import classification_report

"""
PredictionFromModel: class to generate predictions based on the model created in modules.py
"""
class PredictionFromModel:
    """
    __init__(dataPath): initialises all variables used in classification/prediction
    params: dataPath - path to where data a user wants classified is stored.
    """
    def __init__(self, dataPath):
        self.dataset = DataProcess(dataPath)

        # pulls in data from dataset.py and assigns it to variables are used in classification
        (self.features, 
        self.labels, 
        self.adjacency, 
        self.trainMask, 
        self.validaMask, 
        self.testMask, 
        self.trainLabels, 
        self.validaLabels, 
        self.testLabels, 
        self.target, 
        self.numNodes, 
        self.numFeatures) = self.dataset.getData()

        self.classes = len(np.unique(self.target))

    """
    generateModel(): generates a model for classification using pretrained model weights 
    returns: a model for prediction/classification usage
    """
    def generateModel(self):
        self.model = GCN(self.numNodes, self.numFeatures, self.classes)
        self.model.load_weights("training/cp.ckpt")
        return self.model
    
    """
    predictResults(): generates predictions from the test set of data using keras's model prediction
    returns: classifications of the test set data using the trained model and labels/classes of the dataset
    """
    def predictResults(self):
        return self.model.predict([self.features, self.adjacency], batch_size=self.numNodes), self.labels

    """
    plotTSNE(labels, predictions): creates tsne plot given labels and predictions
    params: labels, predictions - labels/classes of the data; predictions generated by the predictResults function
    outputs: tsne plot of inputted data
    """
    def plotTSNE(self, labels, predictions):
        tsne = TSNE(n_components=2).fit_transform(predictions)
        colourMap = np.argmax(labels, axis=1)
        plt.figure(figsize=(15,15))
        for classes in range(self.classes):
            indices = np.where(colourMap == classes)
            indices = indices[0]
            plt.scatter(tsne[indices, 0], tsne[indices, 1], label=classes)

        plt.legend()
        plt.show()

def main():
 model = PredictionFromModel("facebook.npz") 
 model.generateModel()
 predictions, labels = model.predictResults()
 model.plotTSNE(labels, predictions)
 

if __name__ == '__main__':
    main()



