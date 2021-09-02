import jenkspy
import numpy as np
from .support import str_to_num


class Classification:
    '''
    There are following type of classification methods,
        1. Natural break: 
            The jenkspy library is used for this classification method. 
            With natural breaks classification (Jenks) Natural Breaks Jenks, classes are based on natural groupings inherent in the data. 
            Class breaks are created in a way that best groups similar values together and maximizes the differences between classes. 
            The features are divided into classes whose boundaries are set where there are relatively big differences in the data values.

        2. Equal Interval:
        3. Defined Interval: 
            This method ignore the number of classes. 
            Based on the given interval, it will automatically classify the given data.

        4. Quantile (Equal count):

        5. Standard Deviation:
            I have to check this method again

        6. Geometrical Interval:

    '''

    def __init__(self, values, number_of_class=5, classification_method='natural_break'):
        self.values = values
        self.number_of_class = number_of_class
        self.classification_method = classification_method

        # The following values will be generated based on values
        if self.values:
            self.max_value = max(self.values)
            self.min_value = min(self.values)

        else:
            self.max_value = None
            self.min_value = None
            self.classes = None

    def jenks_breaks(self):
        return jenkspy.jenks_breaks(self.values, self.number_of_class)

    def equal_interval(self):
        interval = (self.max_value - self.min_value)/self.number_of_class

        output = []
        for i in range(self.number_of_class):
            val = self.min_value + interval * i
            output.append(val)

        output.append(self.max_value)

        return output

    def defined_interval(self, interval):

        output = []
        while self.min_value < self.max_value:
            val = self.min_value + interval
            output.append(val)

        return output

    def quantile(self):
        interval = 1/self.number_of_class

        output = []
        for i in range(self.number_of_class):
            val = interval * i
            quantile = np.quantile(self.values, val)
            output.append(quantile)

        output.append(self.max_value)

        return output

    def standard_deviation(self):
        '''
        I have to come back here. 
        For now, I don't know the algorithm how to classify it.
        '''
        std = np.std(self.values)
        mean = np.mean(self.values)

        return self.equal_interval()

    def geometrical_interval(self):
        return np.geomspace(self.min_value, self.max_value, num=self.number_of_class+1)

    def choose_classification_method(self):

        for i, v in enumerate(self.values):
            if type(v) is str:
                val = str_to_num(v)
                self.values[i] = val

        try:
            self.max_value = max(self.values)
            self.min_value = min(self.values)

        except TypeError as te:
            return ('The values column must be a list of numeric values. ', te)

        if self.classification_method == 'equal_interval':
            self.classes = self.equal_interval()

        if self.classification_method == 'natural_break':
            self.classes = self.jenks_breaks()

        if self.classification_method == 'quantile':
            self.classes = self.quantile()

        if self.classification_method == 'standard_deviation':
            self.classes = self.standard_deviation()

        if self.classification_method == 'geometrical_interval':
            self.classes = self.geometrical_interval()
