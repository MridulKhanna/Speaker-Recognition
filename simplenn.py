import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.optimizers import Adagrad
import csv

reader = csv.reader(open("datarand.csv", "rb"), delimiter=",")
x = list(reader)
result = np.array(x).astype("float")

x_train = result[:,0:25]
#print(result[:,25].shape)
#print(np.random.randint(10, size=(1000, 1)).shape)

result[:,25] = result[:,25] - 1
three_classes_x = np.concatenate((result[np.where(result[:,25] == 0)], result[np.where(result[:,25] == 1)]), axis=0)
three_classes_x = np.concatenate((three_classes_x,result[np.where(result[:,25] == 2)]),axis=0)
three_classes_y = three_classes_x[:,25]
three_classes_x = three_classes_x[:,0:25]
x_train = three_classes_x
print(three_classes_x.shape)
print(three_classes_y.shape)

#reshaped = np.reshape(result[:,25],(result[:,25].shape[0],1))
#print(reshaped.shape)
print(result[:,25].shape)
#y_train = keras.utils.to_categorical(result[:,25],num_classes=2)
y_train = keras.utils.to_categorical(three_classes_y,num_classes=3)
x_test = three_classes_x
y_test = y_train

model = Sequential()
# Dense(64) is a fully-connected layer with 64 hidden units.
# in the first layer, you must specify the expected input data shape:
# here, 20-dimensional vectors.
model.add(Dense(50, activation='relu', input_dim=25))
#model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
#model.add(Dense(128, activation='relu'))
#model.add(Dense(64, activation='relu'))
#model.add(Dropout(0.5))
model.add(Dense(3, activation='softmax'))

sgd = SGD(lr=0.008, decay=1e-6, momentum=0.9, nesterov=True)
adagrad =Adagrad()
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(x_train, y_train,
          epochs=40,
          batch_size=150)
score = model.evaluate(x_test, y_test, batch_size=128)
print(score)
