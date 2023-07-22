GTIE-RT: A Comprehensive Graph Learning Model for Predicting Drugs Target Metabolic Pathways in Homosapiens.

The GTIE-RT is a deep learning tool designed to predict target metabolic pathways of drugs. This repository contains the code for the GTIE-RT model, which utilizes a Transformer-based architecture for target metabolic pathway prediction.

Installation
To run GTIE-RT, need to install RDKit and the required Python libraries. Use the following command to install the dependencies:


pip install rdkit-pypi

The installation of the RDKit library is essential for the GTIE-RT model because it provides the necessary tools and functionalities to work with chemical structures and molecules.
After the installation of RDKit all the given packages need to import to provide essential functionalities and tools required for various tasks involved in the development and execution
of the model.

from collections import defaultdict
import os
import pickle
import sys
import timeit

import numpy as np

from rdkit import Chem
from rdkit.Chem import rdDepictor, Descriptors
from rdkit.Chem import MACCSkeys

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.metrics import matthews_corrcoef 

Data
The data required to run GTIE-RT is included in this repository with the file name of Drugs.txt.
Please refer to the corresponding paper or contact the authors for information on how to obtain the necessary datasets.

Usage
Ensure that you have obtained the required datasets and placed them in the appropriate directories.

Modify the code to specify the correct data paths, such as 'Drugs.txt', and update any other data-specific configurations as needed.

Run the code in an appropriate Python environment i.e Google coalb, Jupiter notebook, to process the data, create features, and train the GTIE-RT model.

Please note that this README provides only a brief overview of GTIE-RT and its usage. For more detailed instructions and explanations,
refer to the paper associated with this code.

Contact Information
For any questions or inquiries related to GTIE-RT, please contact the authors at:

Hayat Ali Shah (hayatali@whu.edu.cn)








