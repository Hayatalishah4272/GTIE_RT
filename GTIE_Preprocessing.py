# -*- coding: utf-8 -*-
"""GTIE_Prprocessing.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cSicimcX-K8Zzu5sImfEOJp7VOU59Qxa

### Package installation
"""

# Commented out IPython magic to ensure Python compatibility.
# # Install RDKit.
# %%capture
# !pip install rdkit-pypi

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

"""### Check if GPU is available"""

if torch.cuda.is_available():
    device = torch.device('cuda')
else:
    device = torch.device('cpu')

"""### Helper functions"""

# dictionary of atoms where a new element gets a new index
def create_atoms(mol):
    atoms = [atom_dict[a.GetSymbol()] for a in mol.GetAtoms()]
    return np.array(atoms)

# format from_atomIDx : [to_atomIDx, bondDict]
def create_ijbonddict(mol):
    i_jbond_dict = defaultdict(lambda: [])
    for b in mol.GetBonds():
        i, j = b.GetBeginAtomIdx(), b.GetEndAtomIdx()
        bond = bond_dict[str(b.GetBondType())]
        i_jbond_dict[i].append((j, bond))
        i_jbond_dict[j].append((i, bond))
    return i_jbond_dict


def create_fingerprints(atoms, i_jbond_dict, radius):
    """Extract the r-radius subgraphs (i.e., fingerprints)
    from a molecular graph using WeisfeilerLehman-like algorithm."""

    if (len(atoms) == 1) or (radius == 0):
        fingerprints = [fingerprint_dict[a] for a in atoms]

    else:
        vertices = atoms
        for _ in range(radius):
            fingerprints = []
            for i, j_bond in i_jbond_dict.items():
                neighbors = [(vertices[j], bond) for j, bond in j_bond]
                fingerprint = (vertices[i], tuple(sorted(neighbors)))
                fingerprints.append(fingerprint_dict[fingerprint])
            vertices = fingerprints

    return np.array(fingerprints)


def create_adjacency(mol):
    adjacency  = Chem.GetAdjacencyMatrix(mol)
    n          = adjacency.shape[0]
    
    adjacency  = adjacency + np.eye(n)
    degree     = sum(adjacency)
    d_half     = np.sqrt(np.diag(degree))
    d_half_inv = np.linalg.inv(d_half)
    adjacency  = np.matmul(d_half_inv,np.matmul(adjacency,d_half_inv))
    return np.array(adjacency)


def dump_dictionary(dictionary, file_name):
    with open(file_name, 'wb') as f:
        pickle.dump(dict(dictionary), f)
        

def load_tensor(file_name, dtype):
    return [dtype(d).to(device) for d in np.load(file_name + '.npy', allow_pickle=True)]


def load_numpy(file_name):
    return np.load(file_name + '.npy', allow_pickle=True)


def load_pickle(file_name):
    with open(file_name, 'rb') as f:
        return pickle.load(f)


def shuffle_dataset(dataset, seed):
    np.random.seed(seed)
    np.random.shuffle(dataset)
    return dataset


def split_dataset(dataset, ratio):
    n = int(ratio * len(dataset))
    dataset_1, dataset_2 = dataset[:n], dataset[n:]
    return dataset_1, dataset_2



radius = 3

with open('Drugs.txt', 'r') as f:
    data_list = f.read().strip().split('\n')
    
"""Exclude the data contains "." in the smiles, which correspond to non-bonds"""
data_list = list(filter(lambda x: '.' not in x.strip().split()[0], data_list))
N = len(data_list)

print('Total number of Drugs : %d' %(N))

atom_dict = defaultdict(lambda: len(atom_dict))
bond_dict = defaultdict(lambda: len(bond_dict))
fingerprint_dict = defaultdict(lambda: len(fingerprint_dict))

Molecules, Adjacencies, Properties, MACCS_list = [], [], [], []

max_MolMR, min_MolMR     = -1000, 1000
max_MolLogP, min_MolLogP = -1000, 1000
max_MolWt, min_MolWt     = -1000, 1000
max_NumRotatableBonds, min_NumRotatableBonds = -1000, 1000
max_NumAliphaticRings, min_NumAliphaticRings = -1000, 1000
max_NumAromaticRings, min_NumAromaticRings   = -1000, 1000
max_NumSaturatedRings, min_NumSaturatedRings = -1000, 1000

for no, data in enumerate(data_list):
    
    print('/'.join(map(str, [no+1, N])))
    
    smiles, property_indices = data.strip().split('\t')
    property_s = property_indices.strip().split(',')
    
    property = np.zeros((1,7))
    for prop in property_s:
        property[0,int(prop)] = 1
        
    Properties.append(property)
    
    mol = Chem.MolFromSmiles(smiles)
    atoms = create_atoms(mol)
    i_jbond_dict = create_ijbonddict(mol)

    fingerprints = create_fingerprints(atoms, i_jbond_dict, radius)
    Molecules.append(fingerprints)
    
    adjacency = create_adjacency(mol)
    Adjacencies.append(adjacency)
    
    MACCS         = MACCSkeys.GenMACCSKeys(Chem.MolFromSmiles(smiles))
    MACCS_ids     = np.zeros((20,))
    MACCS_ids[0]  = Descriptors.MolMR(mol)
    MACCS_ids[1]  = Descriptors.MolLogP(mol)
    MACCS_ids[2]  = Descriptors.MolWt(mol)
    MACCS_ids[3]  = Descriptors.NumRotatableBonds(mol)
    MACCS_ids[4]  = Descriptors.NumAliphaticRings(mol)
    MACCS_ids[5]  = MACCS[108]
    MACCS_ids[6]  = Descriptors.NumAromaticRings(mol)
    MACCS_ids[7]  = MACCS[98]
    MACCS_ids[8]  = Descriptors.NumSaturatedRings(mol)
    MACCS_ids[9]  = MACCS[137]
    MACCS_ids[10] = MACCS[136]
    MACCS_ids[11] = MACCS[145]
    MACCS_ids[12] = MACCS[116]
    MACCS_ids[13] = MACCS[141]
    MACCS_ids[14] = MACCS[89]
    MACCS_ids[15] = MACCS[50]
    MACCS_ids[16] = MACCS[160]
    MACCS_ids[17] = MACCS[121]
    MACCS_ids[18] = MACCS[149]
    MACCS_ids[19] = MACCS[161]
    
    if max_MolMR < MACCS_ids[0]:
        max_MolMR = MACCS_ids[0]
    if min_MolMR > MACCS_ids[0]:
        min_MolMR = MACCS_ids[0]
        
    if max_MolLogP < MACCS_ids[1]:
        max_MolLogP = MACCS_ids[1]
    if min_MolLogP > MACCS_ids[1]:
        min_MolLogP = MACCS_ids[1]
        
    if max_MolWt < MACCS_ids[2]:
        max_MolWt = MACCS_ids[2]
    if min_MolWt > MACCS_ids[2]:
        min_MolWt = MACCS_ids[2]
        
    if max_NumRotatableBonds < MACCS_ids[3]:
        max_NumRotatableBonds = MACCS_ids[3]
    if min_NumRotatableBonds > MACCS_ids[3]:
        min_NumRotatableBonds = MACCS_ids[3]
        
    if max_NumAliphaticRings < MACCS_ids[4]:
        max_NumAliphaticRings = MACCS_ids[4]
    if min_NumAliphaticRings > MACCS_ids[4]:
        min_NumAliphaticRings = MACCS_ids[4]
        
    if max_NumAromaticRings < MACCS_ids[6]:
        max_NumAromaticRings = MACCS_ids[6]
    if min_NumAromaticRings > MACCS_ids[6]:
        min_NumAromaticRings = MACCS_ids[6]
    
    if max_NumSaturatedRings < MACCS_ids[8]:
        max_NumSaturatedRings = MACCS_ids[8]
    if min_NumSaturatedRings > MACCS_ids[8]:
        min_NumSaturatedRings = MACCS_ids[8]
    
    MACCS_list.append(MACCS_ids)

dir_input = ('Drug pathway/input'+str(radius)+'/')
os.makedirs(dir_input, exist_ok=True)

for n in range(N):
    for b in range(20):
        if b==0:
            MACCS_list[n][b] = (MACCS_list[n][b]-min_MolMR)/(max_MolMR-min_MolMR)
        elif b==1:
            MACCS_list[n][b] = (MACCS_list[n][b]-min_MolLogP)/(max_MolMR-min_MolLogP)
        elif b==2:
            MACCS_list[n][b] = (MACCS_list[n][b]-min_MolWt)/(max_MolMR-min_MolWt)
        elif b==3:
            MACCS_list[n][b] = (MACCS_list[n][b]-min_NumRotatableBonds)/(max_MolMR-min_NumRotatableBonds)
        elif b==4:
            MACCS_list[n][b] = (MACCS_list[n][b]-min_NumAliphaticRings)/(max_MolMR-min_NumAliphaticRings)
        elif b==6:
            MACCS_list[n][b] = (MACCS_list[n][b]-min_NumAromaticRings)/(max_MolMR-min_NumAromaticRings)
        elif b==8:
            MACCS_list[n][b] = (MACCS_list[n][b]-min_NumSaturatedRings)/(max_NumSaturatedRings-min_NumSaturatedRings)

np.save(dir_input + 'molecules', Molecules)
np.save(dir_input + 'adjacencies', Adjacencies)
np.save(dir_input + 'properties', Properties)
np.save(dir_input + 'maccs', np.asarray(MACCS_list))

dump_dictionary(fingerprint_dict, dir_input + 'fingerprint_dict.pickle')

print('End!')