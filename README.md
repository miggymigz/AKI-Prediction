# AKI-Prediction
Deep Learning Models for AKI Prediction on MIMIC-III and eICU database

if you use this code, please cite the following paper:
```
Wang Y, Bao J P, Du J Q, et al. Precisely Predicting Acute Kidney Injury with Convolutional Neural Network Based on Electronic Health Record Data. arXiv preprint arXiv:2005.13171, 2020.
```

## Data Access
The propsed models were tested on [MIMIC-III database](https://mimic.physionet.org/) and [eICU database](https://eicu-crd.mit.edu/). This study uses blood gas features and fundamental demographics to make the input vector. The data sets used for the proposed models can be found in [data](https://github.com/Sophiaaaaaa/AKI-Prediction/tree/master/data) folder.

## How to run these model?
```
python main.py --data_base [mimic|eicu] --model_name [MLP|CNN|Resnet] --nb_layer 18
```
* data_base: the name of database you used. In this work, you can choose `mimic` or `eicu`.
* nb_layer: the number of layers of the network you used.
* model_name: the name of the neural network you used.

## Files contained in this repository
* main.py: main function.
* data_process.py: to copy the data from the database to an .npz file.
* train.py: to train the model using 5-fold cross-validation.
* model.py: to build the `MLP`, `VGG` and `Resnet` model.
* utils.py: some common funtions.

