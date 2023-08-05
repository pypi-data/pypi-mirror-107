from nlpengine.cli import main
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import fasttext
import os

class FastTextClassifier:

    def __init__(self):
        self.texts, self.labels = None, None
        self.model, self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None, None

    def split_test_data(self):
        self.labels = [str(item).strip().replace(" ", "_") for item in self.labels]
        self.texts = [str(x) for x in self.texts]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.texts, self.labels)


    def preprocess_for_fasttext(self):
        X_train_fasttext, X_test_fasttext = [],[] 
        for i,j in zip(self.X_train, self.y_train):
            X_train_fasttext.append("__label__"+str(j) + " " + str(i))
        for i,j in zip(self.X_test, self.y_test):
            X_test_fasttext.append("__label__"+str(j) + " " + str(i))

        #saving the train and test data for fasttext
        with open('__temp__train.txt', 'w',encoding='utf8') as f:
            for item in X_train_fasttext:
                try:
                    f.write("%s\n" % item)
                except:
                    print("Error occured while writing the train.txt for fasttext ")
                    print(item)
        with open('__temp__test.txt', 'w',encoding='utf8') as f:
            for item in X_test_fasttext:
                try:
                    f.write("%s\n" % item)
                except:
                    print("Error occured while writing the test.txt for fasttext ")
                    print(item)
        

    def train(self):
        print("Fasttext Autotune Started for 10s.")
        self.model =  fasttext.train_supervised(input='__temp__train.txt', autotuneValidationFile='__temp__test.txt', autotuneDuration=10)
        print("Training complete.")

    def evaluate(self):
        results = self.model.test("__temp__test.txt")
        print("Model Evaluation complete. Samples: {}, precision: {}, recall: {}".format(results[0], results[1], results[2]))

    def get_model(self):
        return self.model
    
    def get_num_of_classes(self):
        return len(set(self.labels))

    def clean_temp_files(self):
        try:
            os.remove("__temp__train.txt")
            os.remove("__temp__test.txt")
            #print("temp files removed")
        except:
            print("no temp files to remove")

    def fit(self, texts, labels):
        ''' 
        Function which accepts a list of texts and labels and returns a fasttext classifier model
        '''
        
        assert len(texts) == len(labels), "Number of Texts and labels should be equal"
        self.texts = texts
        self.labels = labels
        self.split_test_data()
        self.preprocess_for_fasttext()
        self.train()
        #self.evaluate()
        self.get_classification_report()
        self.clean_temp_files()
        return self.get_model()

    def predict_proba(self, text):
        try:
            text = list(text)
            text = [str(x) for x in text]
        except:
            pass
        fasttext_predictions = self.get_model().predict(text, k=self.get_num_of_classes())
        return fasttext_predictions[1]

    def get_classification_report(self):
        try:
            y_pred_ = self.model.predict(list(self.X_test))
            y_pred = [y_pred_[0][i][0].replace("__label__", "") for i in range(len(self.X_test))]
            print(classification_report(self.y_test, y_pred))
        except Exception as error:
            print(error)

if __name__ == "__main__":
    FastTextClassifier()