import numpy
from keras.datasets import imdb
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence
# 加载数据集
numpy.random.seed(7)

(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=5000)
# print(X_train)
# 设置最大输出序列长度
outputlen = 500
X_train = sequence.pad_sequences(X_train, maxlen=outputlen)
X_test = sequence.pad_sequences(X_test, maxlen=outputlen)
# 设置模型参数并进行训练
embedding_vecor_length = 32
testmodel = Sequential()
testmodel.add(Embedding(5000,32, input_length=outputlen))
testmodel.add(LSTM(100))
testmodel.add(Dense(1, activation='sigmoid'))
testmodel.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(testmodel.summary())
testmodel.fit(X_train, y_train, epochs=3, batch_size=64)
# 用测试集测试得到结果并输出
scores = testmodel.evaluate(X_test, y_test, verbose=2)
print("准确度: %.2f%%" % (scores[1]*100))