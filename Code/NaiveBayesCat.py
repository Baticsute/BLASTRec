import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split ,KFold
from pandas import *



class NaiveBayesClassfier:

    def model_build(self,data,label="",lalapce_estimator=1):

        model = None
        data_col = data.columns[0:len(data.columns)-1] ## without label column

        class_unique = unique(data[label]) ## unique the class
        dic_att = {}
        for attribute in data_col:
            dic_class = {}
            for class_ in class_unique:

                dt = data[attribute][data[label]==class_]
                p = dict(dt.value_counts() / dt.count())

                if len(p) < len(unique(data[attribute])): ## compare and add lalapce estimator if keys p in dic difference with values of this attribute .

                    set_b = set(unique(data[attribute]))
                    set_a = set(p.keys())
                    values_difference = set_b.difference(set_a)

                    vl_counts = dt.value_counts() +  ( lalapce_estimator/len(unique(data[attribute]))) ## add more laplapce estimator
                    count_add = dt.count() + lalapce_estimator

                    p = dict(vl_counts/count_add) ## update p dict

                    for diff in values_difference:
                        value_estimator =  ( ( 0.0 + lalapce_estimator/len(unique(data[attribute]) ) ) / ( dt.count() + lalapce_estimator ) )
                        p_temp = {diff:value_estimator}
                        p.update(p_temp)

                dic_temp = {class_:p}
                dic_class.update(dic_temp)

            dic_att_temp = {attribute:dic_class}
            dic_att.update(dic_att_temp)

        model = dic_att

        return model

    def fit(self,data,label="",lalapce_estimator=1):

        sampling = self.model_build(data,label,lalapce_estimator)

        total_len = len(data[label])
        dict_ = {}
        for class_ in unique(data[label]):
            p = len(data[data[label]== class_ ]) / total_len
            dict_temp = {class_:p}
            dict_.update(dict_temp)

        model = NaiveBayesModel(sampling,dict_)

        return model


class NaiveBayesModel:

    def __init__(self,model,P_class):

        self.model = model
        self.P_class = P_class


    def predict(self, data_test):

        classes = list(self.P_class.keys())
        dictionary_of_P_class = dict()
        predict_targets = []
        data_col = data_test.columns ## without label column
        for i in data_test.index.values :

            fetch_data_index = data_test.ix[i]
            total = 0.0
            for class_ in classes:

                likeihood = self.P_class[class_]
   
                for attribute_ in data_col:
                    try:
                     likeihood = likeihood * (self.model[attribute_][class_][fetch_data_index[attribute_]])
                    except KeyError:
                        likeihood = likeihood * 1.0
                        erorr = True

                dict_temp = {class_:likeihood}
                dictionary_of_P_class.update(dict_temp)

            total = sum(list(dictionary_of_P_class.values()))
            max = 0
            final_label = None
            for key in dictionary_of_P_class:
                value =  dictionary_of_P_class[key]/total
                if(value > max ):
                    max = value
                    final_label = key
            predict_targets.append(final_label)
        return predict_targets


def determine_accuracy(test_target, targets_predicted):
    correct = 0
    total = len(test_target)
    for x in range(len(test_target)):

        if test_target[x] == targets_predicted[x]:
            correct = correct + 1
        else :
            if( test_target[x]==None or targets_predicted[x]==None):
                print(test_target[x], "-x-", targets_predicted[x])

    percent = (correct * 100) / total

    print("Total correct: (", correct, "/", total, "): ", float("{0:.2f}".format(percent)), "%")
    return percent

'''
--------------------------------------------------------
|                    VALIDATION                          |
--------------------------------------------------------
'''

def validation(data,label="",n_test=10):
    acc_score_MyHoldout = 0
    acc_score_MyKFold = 0

    for i in range(n_test):
        training, test = train_test_split(data, test_size=0.30,shuffle=True)
        test_data = test.loc[:, test.columns != label]
        test_targets = list(test[label])
        classifier = NaiveBayesClassfier()
        model = classifier.fit(training, label)
        predicted_targets = model.predict(test_data)

        print("My Hold Out : ")
        acc_score_MyHoldout = acc_score_MyHoldout + determine_accuracy(test_targets, predicted_targets)
    print("-------------------------------------------------------------------------")
    print("Total My Hold Out : ", acc_score_MyHoldout / n_test, " %")
    print("-------------------------------------------------------------------------")

    k = KFold(n_splits=n_test, shuffle=True)
    data_forme = data.iloc[:, :].values
    for train_index, test_index in k.split(data):
        training_data, test_data = data_forme[train_index], data_forme[test_index]
        classifier = NaiveBayesClassfier()
        training_dataframe = pandas.DataFrame(training_data[:, :],
                                              columns=["Giong_Lua", "Mat_Do_Sa", "Nhiet_Do", "Do_Am", "Mau_La",
                                                       "Tinh_Trang_Benh", "Phuong_Phap"]) ## convert numpy matrix to dataframe
        model = classifier.fit(training_dataframe, "Phuong_Phap")
        test_dataframe = pandas.DataFrame(test_data[:, :],
                                          columns=["Giong_Lua", "Mat_Do_Sa", "Nhiet_Do", "Do_Am", "Mau_La",
                                                   "Tinh_Trang_Benh", "Phuong_Phap"]) ## convert numpy matrix to dataframe
        test_targets = list(test_dataframe[label])
        test_data = test_dataframe.iloc[:, test_dataframe.columns != label]
        predicted_targets = model.predict(test_data)
        print("My K Fold : ")
        acc_score_MyKFold = acc_score_MyKFold + determine_accuracy(test_targets, predicted_targets)

    print("-------------------------------------------------------------------------")
    print("Total My K Fold : ", acc_score_MyKFold / n_test, " %")
    print("-------------------------------------------------------------------------")

#data = read_csv('data3.csv')
#validation(data,"Phuong_Phap")