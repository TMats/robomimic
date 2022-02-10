"""
Script for splitting a dataset hdf5 file into training and validation trajectories.

Args:
    dataset (str): path to hdf5 dataset

    filter_key (str): if provided, split the subset of trajectories
        in the file that correspond to this filter key into a training
        and validation set of trajectories, instead of splitting the
        full set of trajectories

    ratio (float): validation ratio, in (0, 1). Defaults to 0.1, which is 10%.

Example usage:
    python split_train_val.py --dataset /path/to/demo.hdf5 --ratio 0.1
"""

import argparse
import json
import numpy as np
from sklearn.model_selection import train_test_split
import os

def split_config_from_json(source_json_path, test_ratio=0.1):
    """
    Splits view config into training set and test set from json file.

    Args:
        source_json_path (str): path to the json file

        test_ratio (float): ratio of test views to all available views

    """

    with open(source_json_path, 'r') as f:
        views = json.load(f)
    root_json_path, source_json_name = os.path.split(source_json_path)
    source_json_name = os.path.splitext(source_json_name)[0]
    train_json_path = os.path.join(root_json_path, source_json_name + '-train.json')
    test_json_path = os.path.join(root_json_path, source_json_name + '-test.json')

    train_views, test_views = train_test_split(views, test_size=test_ratio)
    print("{} test views out of {} total demonstrations.".format(len(test_views), len(views)))

    with open(train_json_path, "w") as f:
        json.dump(train_views, f, indent=2) 
    with open(test_json_path, "w") as f:
        json.dump(test_views, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="path to source view json config file",
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=0.1,
        help="validation ratio, in (0, 1)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=0,
        help="random seed for spliting into train/test"
    )
    args = parser.parse_args()

    assert args.source is not None, "Please provide source json file"
    # seed to make sure results are consistent
    np.random.seed(args.seed)

    split_config_from_json(args.source, test_ratio=args.ratio)
