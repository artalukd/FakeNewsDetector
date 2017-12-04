import re
from keras.models import Sequential
from keras.layers import Activation, Dropout, Flatten, Dense, BatchNormalization, LSTM, Embedding, Reshape
from keras.models import load_model, model_from_json
import pickle
from keras.engine.topology import Layer
import keras.backend as K
from keras import initializers
import numpy as np


def predict(title,text):
	

	class Embedding2(Layer):

	    def __init__(self, input_dim, output_dim, fixed_weights, embeddings_initializer='uniform', 
	                 input_length=None, **kwargs):
	        kwargs['dtype'] = 'int32'
	        if 'input_shape' not in kwargs:
	            if input_length:
	                kwargs['input_shape'] = (input_length,)
	            else:
	                kwargs['input_shape'] = (None,)
	        super(Embedding2, self).__init__(**kwargs)
	    
	        self.input_dim = input_dim
	        self.output_dim = output_dim
	        self.embeddings_initializer = embeddings_initializer
	        self.fixed_weights = fixed_weights
	        self.num_trainable = input_dim - len(fixed_weights)
	        self.input_length = input_length
	        
	        w_mean = fixed_weights.mean(axis=0)
	        w_std = fixed_weights.std(axis=0)
	        self.variable_weights = w_mean + w_std*np.random.randn(self.num_trainable, output_dim)

	    def build(self, input_shape, name='embeddings'):        
	        fixed_weight = K.variable(self.fixed_weights, name=name+'_fixed')
	        variable_weight = K.variable(self.variable_weights, name=name+'_var')
	        
	        self._trainable_weights.append(variable_weight)
	        self._non_trainable_weights.append(fixed_weight)
	        
	        self.embeddings = K.concatenate([fixed_weight, variable_weight], axis=0)
	        
	        self.built = True

	    def call(self, inputs):
	        if K.dtype(inputs) != 'int32':
	            inputs = K.cast(inputs, 'int32')
	        out = K.gather(self.embeddings, inputs)
	        return out

	    def compute_output_shape(self, input_shape):
	        if not self.input_length:
	            input_length = input_shape[1]
	        else:
	            input_length = self.input_length
	        return (input_shape[0], input_length, self.output_dim)

	title = title.lower()
	text = text.lower()

	title = title.replace(r'http[\w:/\.]+','<URL>') # remove urls
	text = text.replace(r'http[\w:/\.]+','<URL>') # remove urls
	title = title.replace(r'[^\.\w\s]','') #remove everything but characters and punctuation
	text = text.replace(r'[^\.\w\s]','') #remove everything but characters and punctuation
	title = title.replace(r'\.\.+','.') #replace multple periods with a single one
	text = text.replace(r'\.\.+','.') #replace multple periods with a single one
	title = title.replace(r'\.',' . ') #replace periods with a single one
	text = text.replace(r'\.',' . ') #replace multple periods with a single one
	title = title.replace(r'\s\s+',' ') #replace multple white space with a single one
	text = text.replace(r'\s\s+',' ') #replace multple white space with a single one
	title = title.strip() 
	text = text.strip() 

	# getting word2num
	fp = open("demo/word2num_processed.pkl")
	word2num = pickle.load(fp)
	fp.close()

	# getting words_in_glove
	fp = open("demo/words_in_glove_processed.pkl")
	words_in_glove = pickle.load(fp)
	fp.close()

	# getting word2glove
	fp = open("demo/word2glove_processed.pkl")
	word2glove = pickle.load(fp)
	fp.close()

	model = Sequential()
	model.add(Embedding2(len(word2num), 50,
	                    fixed_weights=np.array([word2glove[w] for w in words_in_glove]))) # , batch_size=batch_size
	model.add(LSTM(64))
	model.add(Dense(1, activation='sigmoid'))

	model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
	model.summary()

	model.load_weights("demo/rmsprop_guardian_kaggle_data_trained_model.h5")
	

	sentence = text.lower()
	sentence_num = [word2num[w] if w in word2num else word2num['<Other>'] for w in sentence.split()]
	sentence_num = [word2num['<PAD>']]*(0) + sentence_num
	sentence_num = np.array(sentence_num)
	new_obj = model.predict(sentence_num[None,:])
	return new_obj[0][0].item()
