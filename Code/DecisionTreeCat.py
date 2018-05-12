from sklearn.model_selection import train_test_split, KFold
from pandas import *
from numpy import *

class Node:

    def __init__(self, attribute):
        self.attribute = attribute
        self.branches = {}

    def isLeaf(self):
        if self.branches:
            return False
        else:
            return True

def entropy(data_subset, label=""): ## Calculate entropy

    class_count = data_subset[label].value_counts()
    total_len = len(data_subset[label])
    e = 0
    for i in class_count:
        e = e + ((-i / total_len) * np.log2(i / total_len))
    return e

def information_bits_of_column(data, column="", label=""): ## Information Gain of a column ( feature )

    data_unique = unique(data[column]) ## distinct value
    data_len = len(data[label])  ## lenght of column label
    information_gain = 0
    for i in data_unique: ## entropy for each value in a feature , sum that
        attribute_label_len = len(data[data[column] == i])
        information_gain = information_gain + (
                    (attribute_label_len / data_len) * entropy(data[data[column] == i], label))

    return information_gain


class MyDescisionTreeClassifier:
    def tree(self, data, label=""):
        total_entropy = entropy(data, label)  ## Step 1
        if total_entropy == 0: ## previous entropy = 0 , data completely homogeneous , return first index of label column
            target = unique(data[label])
            node = Node(target[0])
            return node

        if len(data.columns) == 1:
            node = Node(data[label].value_counts().idxmax()) ## Have not any Attribute to split , choose the most class appear in label column
            return node

        gain_inf = 0  ## Step 2
        previous_gain_inf = 0
        best_attribute = None
        for col in data.columns: ## information gain for each attribute
            if col == label:  ## ignore the label columns
                break
            gain_inf = total_entropy - information_bits_of_column(data, col, label)
            if gain_inf > previous_gain_inf: ## choose the most information gain
                previous_gain_inf = gain_inf
                best_attribute = col

        if (best_attribute == None):
            node = Node(data[label].value_counts().idxmax())  ## So If it don't find any best Attribute because Entropy not change for this stage .
            return node


        current_node = Node(best_attribute)  ## step 3

        data_unique = unique(data[best_attribute])  ## values in best current attribue
        for attribute_value in data_unique:
            data_subset = data[data[best_attribute] == attribute_value]
            reduced_subset = data_subset.drop(best_attribute, axis=1)  ## removed
            node = self.tree(reduced_subset, label)  ## loop
            current_node.branches[attribute_value] = node

        return current_node  # step 4

    def fit(self, data, label=""):
        Root = self.tree(data, label) ## Rules of the tree
        model = MyDescisionTreeModel(Root) ## Ready to predict

        return model ## Rules of the tree

class MyDescisionTreeModel:
    def __init__(self, treenode):
        self.treenode = treenode

    def predict(self, test_data):
        columns = ["Giong_Lua", "Mat_Do_Sa", "Nhiet_Do", "Do_Am", "Mau_La", "Tinh_Trang_Benh"] ## vietnamese attribute
        predicted_targets = []

        for i in range(len(test_data)):
            node = self.treenode
            while node.isLeaf() != True:

                if test_data.iloc[i, columns.index(node.attribute)] in node.branches:
                    node = node.branches[test_data.iloc[i, columns.index(node.attribute)]]
                else:
                    keys = list(node.branches.keys())
                    node = node.branches[keys[0]]

            predicted_targets.append(node.attribute)  ## list of targets predicted .
        return predicted_targets





def determine_accuracy(test_target, targets_predicted):
    correct = 0
    total = len(test_target)
    for x in range(len(test_target)):
        if test_target[x] == targets_predicted[x]:
            correct = correct + 1
    percent = (correct * 100) / total
    print("Total correct: (", correct, "/", total, "): ", float("{0:.2f}".format(percent)), "%")
    return percent


def validation(data, label="", n_test=10):
    acc_score_MyHoldout = 0
    acc_score_MyKFold = 0

    for i in range(n_test):
        training, test = train_test_split(data, test_size=0.30, shuffle=True)
        test_data = test.loc[:, test.columns != label]
        test_targets = list(test[label])

        classifier = MyDescisionTreeClassifier()
        model = classifier.fit(training, label)
        predicted_targets = model.predict(test_data)
        print("My Hold Out : ")
        acc_score_MyHoldout = acc_score_MyHoldout + determine_accuracy(test_targets, predicted_targets)
    print("-------------------------------------------------------------------------")
    print("Total My Hold Out : ", acc_score_MyHoldout / n_test, " %")
    print("-------------------------------------------------------------------------")

    k = KFold(n_splits=n_test, shuffle=True, random_state=True)
    data_forme = data.iloc[:, :].values
    for train_index, test_index in k.split(data):
        training_data, test_data = data_forme[train_index], data_forme[test_index]
        classifier = MyDescisionTreeClassifier()
        training_dataframe = pandas.DataFrame(training_data[:, :],
                                              columns=["Giong_Lua", "Mat_Do_Sa", "Nhiet_Do", "Do_Am", "Mau_La",
                                                       "Tinh_Trang_Benh", "Phuong_Phap"])
        model = classifier.fit(training_dataframe, "Phuong_Phap")
        test_dataframe = pandas.DataFrame(test_data[:, :],
                                          columns=["Giong_Lua", "Mat_Do_Sa", "Nhiet_Do", "Do_Am", "Mau_La",
                                                   "Tinh_Trang_Benh", "Phuong_Phap"])
        test_targets = list(test_dataframe[label])
        test_data = test_dataframe.iloc[:, test_dataframe.columns != label]
        predicted_targets = model.predict(test_data)
        print("My K Fold : ")
        acc_score_MyKFold = acc_score_MyKFold + determine_accuracy(test_targets, predicted_targets)

    print("-------------------------------------------------------------------------")
    print("Total My K Fold : ", acc_score_MyKFold / n_test, " %")
    print("-------------------------------------------------------------------------")



'''
##uncomment this to see my model validation accuracy 
'''
##data = read_csv('data3.csv')
##validation(data,"Phuong_Phap")