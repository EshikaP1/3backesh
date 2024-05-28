## Python Exercise Model
# Import the required libraries
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import seaborn as sns


# Define the ExerciseRegression global variable
exercise_regression = None


# Define the ExerciseRegression class
class ExerciseRegression:
    def __init__(self):
        self.ex = None
        self.linearregression = None
        self.X_train = None
        self.X_test = None
        self.Y_train = None
        self.Y_test = None
        self.exercise = None
        self.Weather_Conditions = None
        #self.encoder = None
        self.datacolumns = None




    def initExercise(self):
        exercise_data = pd.read_csv('/home/eneter/vscode/3backesh/exercise.csv')
        ex = exercise_data
        ex.drop(['ID'], axis=1, inplace=True)
        ex.dropna(inplace=True) # drop rows with at least one missing value, after dropping unuseful columns


        ex['Gender'] = ex['Gender'].apply(lambda x: 1 if x == 'male' else 0)
        # Encode categorical variables
        self.exercise = OneHotEncoder(handle_unknown='ignore')
        self.exercise.fit(ex[['Exercise']])
        e_hot = self.exercise.transform(ex[['Exercise']]).toarray()
        cols = ['Exercise_' + val for val in self.exercise.categories_[0]]
        ex[cols] = pd.DataFrame(e_hot)
        ex.drop(['Exercise'], axis=1, inplace=True)
        ex.dropna(inplace=True) # drop rows with at least one missing value, after preparing the data


        self.Weather_Conditions = OneHotEncoder(handle_unknown='ignore')
        self.Weather_Conditions.fit(ex[['Weather Conditions']])
        w_hot = self.Weather_Conditions.transform(ex[['Weather Conditions']]).toarray()
        cols = ['Weather Conditions_' + val for val in self.Weather_Conditions.categories_[0]]
        ex[cols] = pd.DataFrame(w_hot)
        ex.drop(['Weather Conditions'], axis=1, inplace=True)
        ex.dropna(inplace=True)


        X = ex.drop('Actual Weight',axis=1)
        Y = ex['Actual Weight']
        self.X_train,self.X_test,self.Y_train,self.Y_test = train_test_split(X,Y,test_size=0.2,random_state=11)
        self.datacolumns = self.X_train.columns
        self.linearregression = LinearRegression()
        self.linearregression.fit(self.X_train, self.Y_train)
       
    def runLinearRegression(self):
        if self.linearregression is None:
            print("Linear Regression model is not initialized. Please run initExercise() first.")
            return
        y_pred_logreg = self.linearregression.predict(self.X_test)
        # accuracy_logreg = accuracy_score(self.Y_test, y_pred_logreg)
        accuracy_logreg = self.linearregression.score(self.X_test,self.Y_test)
        print('Linear Regression Accuracy: {:.2%}'.format(accuracy_logreg))


def predictWeight(contestant):        
    #display(contestant)
    #pd.read_json(contestant)


    # contestant = pd.DataFrame({
    # 'Calories Burn': [237],
    # 'Dream Weight': [145],
    # 'Age': [17],
    # 'Gender': ['Female'],
    # 'Duration': [3],
    # 'Heart Rate': [140],
    # 'BMI': ['28.5'],
    # 'Exercise Intensity': [3],
    # 'Exercise': ['Exercise 1'],
    # 'Weather Conditions': ['Sunny']
    # })


    contestant = pd.DataFrame(contestant, index=[0])
    new_contestant = contestant.copy()
    print(contestant)


    # Preprocess the new passenger data
    new_contestant['Gender'] = new_contestant['Gender'].apply(lambda x: 1 if x == 'male' else 0)


    onehot = exercise_regression.exercise.transform(new_contestant[['Exercise']]).toarray()
    cols = ['Exercise_' + val for val in exercise_regression.exercise.categories_[0]]
    new_contestant[cols] = pd.DataFrame(onehot, index=new_contestant.index)


    onehot = exercise_regression.Weather_Conditions.transform(new_contestant[['Weather Conditions']]).toarray()
    cols = ['Weather Conditions_' + val for val in exercise_regression.Weather_Conditions.categories_[0]]
    new_contestant[cols] = pd.DataFrame(onehot, index=new_contestant.index)


    new_contestant.drop(['Exercise'], axis=1, inplace=True)
    new_contestant.drop(['Weather Conditions'], axis=1, inplace=True)


    new_contestant = new_contestant[exercise_regression.datacolumns]
   
    Actual_Weight = exercise_regression.linearregression.predict(new_contestant)
    print("******************************")
    print(Actual_Weight)
    return { 'actualWeight': Actual_Weight[0] }




def initExercise():
    global exercise_regression
    exercise_regression = ExerciseRegression()
    exercise_regression.initExercise()
    exercise_regression.runLinearRegression()

