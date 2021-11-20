Steps the code takes:
data_handler.py
model.py
train.py
predictor.py

Steps for the user:
-> predictor.py

More details in the notebook files and saved plots.

Introduction

Today deep learning is viral and applied to a variety of machine learning problems such as image recognition, speech 
recognition, machine translation, etc. There is a wide range of highly customizable neural network architectures, which 
can suit almost any problem when given enough data. Each neural network should be customized to suit the given problem 
well enough. You have to fine tune the hyperparameters for the network for each task (the learning rate, dropout 
coefficients, weight decay, etc.) as well as number of hidden layers, number of units in layers. Choosing the right 
activation function for each layer is also crucial and may have a significant impact on learning speed.


Activation Functions

The activation function is an essential building block for every neural network. We can choose from a huge list of 
popular activation functions, which are already implemented in Deep Learning frameworks, like ReLU, Sigmoid, Tanh and 
many others.
But to create a state of the art model, customized particularly for your task, you may need to use a custom activation 
function, which is not yet implemented in Deep Learning framework you are using. Activation functions can be roughly 
classified into the following groups by complexity:
1. Simple activation functions like SiLU, Inverse square root unit (ISRU). These functions can be easily implemented 
in any Deep Learning framework.
2. Activation functions with trainable parameters like SoftExponential or S-shaped rectified linear activation 
unit (SReLU).
3. Activation functions, which are not differentiable at some points and require custom implementation of backward 
step, for example Bipolar rectified linear unit (BReLU).

Context

Fashion-MNIST is a dataset of Zalando's article images—consisting of a training set of 60,000 examples and a test set 
of 10,000 examples. Each example is a 28x28 grayscale image, associated with a label from 10 classes. Zalando intends 
Fashion-MNIST to serve as a direct drop-in replacement for the original MNIST dataset for benchmarking machine learning 
algorithms. It shares the same image size and structure of training and testing splits.
The original MNIST dataset contains a lot of handwritten digits. Members of the AI/ML/Data Science community love this 
dataset and use it as a benchmark to validate their algorithms. In fact, MNIST is often the first dataset researchers 
try. "If it doesn't work on MNIST, it won't work at all", they said. "Well, if it does work on MNIST, it may still fail 
on others."
Zalando seeks to replace the original MNIST dataset

Content
Each image is 28 pixels in height and 28 pixels in width, for a total of 784 pixels in total. Each pixel has a single 
pixel-value associated with it, indicating the lightness or darkness of that pixel, with higher numbers meaning darker. 
This pixel-value is an integer between 0 and 255. The training and test data sets have 785 columns. The first column 
consists of the class labels (see above), and represents the article of clothing. The rest of the columns contain the 
pixel-values of the associated image.
To locate a pixel on the image, suppose that we have decomposed x as x = i * 28 + j, where i and j are integers between 
0 and 27. The pixel is located on row i and column j of a 28 x 28 matrix.
For example, pixel31 indicates the pixel that is in the fourth column from the left, and the second row from the top, 
as in the ascii-diagram below.

Labels
Each training and test example is assigned to one of the following labels:

0 T-shirt/top
1 Trouser
2 Pullover
3 Dress
4 Coat
5 Sandal
6 Shirt
7 Sneaker
8 Bag
9 Ankle boot


TL;DR

Each row is a separate image
Column 1 is the class label.
Remaining columns are pixel numbers (784 total).
Each value is the darkness of the pixel (1 to 255)
Acknowledgements
Original dataset was downloaded from https://github.com/zalandoresearch/fashion-mnist

Dataset was converted to CSV with this script: https://pjreddie.com/projects/mnist-in-csv/

