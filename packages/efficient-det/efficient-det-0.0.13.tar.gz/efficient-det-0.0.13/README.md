## EfficientDet

Start with following command:

```python
export PYTHONPATH="$PWD/src"
```

All commands should be executed in **efficientdet/**.

#### To test trained model on validation dataset you can use the jupyter notebook or python script in examples/.
```python
For your own implementation set the dataset path and path to the trained model. Default paths are set to efficient/dataset.
```

#### To run all tests:
```python
python3 -m unittest
```

#### To train neural network
```python
python3 src/efficient_det/train.py --dataset_path /path/to/dataset/
```


When using Ray Tune verbose is default set to False. Use W&B for visualization.

#### Pip
```python
python3 -m efficient_det.run_training --dataset_path ~/efficientdet/voc_data --use_wandb
```

Imports with pip needs to be like
```python
from efficient_det.models.efficient_net import create_efficientnet
```




