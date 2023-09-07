GTIE-RT: Graph based framework for prediction of target metabolic pathways 
This repository contains the code for the GTIE_RT model. GTIE is a deep learning
model designed for predicting target metabolic pathways of chemical
compounds based on their molecular structures and additional features. 
This README will guide you through installing the necessary dependencies,
using the code, and understanding its components.
 
 INSTALLATION

Before using the GTIE code, you need to install the required dependencies,
including RDKit. RDKit is used for processing chemical structures. You can 
install the necessary libraries by running the following command:
 
 
!pip install rdkit-pypi

Ensure you have Python 3.x installed, as well as the libraries mentioned in the code.

Usage 

To use the GTIE code for target metabolic pathways prediction, follow these steps:
Clone this repository to your local machine.
Install the required dependencies as mentioned in the Installation section.
Used the dataset used in this work or pepare your own molecular dataset for target some
metabolic pathways. The dataset should include molecular structures, target pathways, 
and additional features (MACCS keys).
Modify the code to load and preprocess your dataset. You may need to adjust the code 
to match the format of your dataset.
Train the GTIE-RT model on your dataset by specifying the model's hyperparameters, such 
as dimensionality, number of layers, batch size, learning rate, and more.
Evaluate the model's performance on a validation dataset and a test dataset using various
 metrics like AUC, precision, and recall.

Data 

The GTIE model expects input data in the following format:

Molecular structures represented as fingerprints (obtained from RDKit).
Adjacency matrices for the molecular structures.
Target metabolic pathways.
Additional molecular features (MACCS keys).
You should prepare your dataset in this format and modify the code accordingly to
 load and preprocess your data.

Model Architecture

The GTIE-RT model is a graph-based deep learning model that leverages GCN and Transformer
architecture for target metabolic pathways prediction. It embeds atoms, processes them through
multiple deep model layers, and combines them with additional features (MACCS keys) to make predictions.
The model's hyperparameters, such as dimensionality, number of layers, and learning rate, can be adjusted 
to suit your specific task.

Training 

To train the GTIE model on your dataset, you need to specify the model's hyperparameters and train it
using your training data. The code includes a training loop that handles the optimization process using
the Adam optimizer.

Training can be customized by adjusting the number of training iterations, batch size, learning rate, and
learning rate decay.

Testing and Evaluation 
After training the GTIE-RT model, you can evaluate its performance on a validation dataset and a test dataset.
The code calculates metrics such as AUC, precision, and recall to assess the model's predictive accuracy.

Contact Information
For any questions or inquiries related to GTIE-RT, please contact the authors at:
Hayat Ali Shah (hayatali@whu.edu.cn)