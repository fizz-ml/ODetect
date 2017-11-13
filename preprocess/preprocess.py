import os
import glob
import argparse

from features import calc_co2_troughs

def main(input_path, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    preprocess_data_set(input_path, output_path)

def preprocess_data_set(input_path, output_path):
    """Preprocesses files from dat"""
    if not os.path.exists(output_path):
        raise IOError("Specified output path {} does not exist.".format(output_path))

    for file_path in glob.glob(os.path.join(input_path, '*.mat')):

        print(file_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('dataset_name', type=str, help='Name of the dataset under raw containing the data folder of h5 files to be processed.')
    args = parser.parse_args()

    dataset_name = args.dataset_name
    input_path = os.path.join('data', dataset_name, 'raw')
    output_path = os.path.join('data', dataset_name, 'preprocess')

    main(input_path, output_path)

