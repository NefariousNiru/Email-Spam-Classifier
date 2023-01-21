import os
import io
from pandas import DataFrame
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from emailFetch import emailFetch

class emailClassifier:

    #initialize dataframe as class variable from various spam and ham emails.
    def __init__(self):
        self.data = DataFrame({'message': [], 'class': []})
        #Insert File location here
        self.data = self.data.append(self.dataFrameFromDirectory('emails/spam', 'spam'))
        self.data = self.data.append(self.dataFrameFromDirectory('emails/ham', 'ham'))

    #read ham and spam files in the directory
    def readFiles(self,path):
        for root, dirnames, filenames in os.walk(path):
            for filename in filenames:
                path = os.path.join(root, filename)
                inBody = False
                lines = []
                f = io.open(path, 'r', encoding='latin1')
                for line in f:
                    if inBody:
                        lines.append(line)
                    elif line == '\n':
                        inBody = True
                f.close()
                message = '\n'.join(lines)
                yield path, message

    #dataFrame from the the spam and ham sample emails
    def dataFrameFromDirectory(self, path, classification):
        rows = []
        index = []
        for filename, message in self.readFiles(path):
            #appending filenames and messages fethed by the readfile function
            rows.append({'message': message, 'class': classification})
            index.append(filename)
        return DataFrame(rows, index=index)

    #ML module to predict newer classes
    def classifier(self):
        vectorizer = CountVectorizer()
        counts = vectorizer.fit_transform(self.data['message'].values)
        classifier = MultinomialNB()
        targets = self.data['class'].values
        classifier.fit(counts, targets)
        ef = emailFetch()
        result = ef.imap()
        # result = [enter test value here]
        result_counts = vectorizer.transform(result)
        predictions = classifier.predict(result_counts)
        print(predictions)

if __name__ == '__main__':
    ec = emailClassifier()
    ec.classifier()