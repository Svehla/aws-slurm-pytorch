#!/usr/bin/env python
from torchvision import datasets, transforms

# TODO: download and prepare dataset from AWS s3 to use custom data
def get_trainset(path, shouldDownload: bool):
    mean = (0.5,)
    std_dev = (0.5,)
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean, std_dev)])
    # TODO: add test set for over-fitting check
    trainset = datasets.MNIST(path, train=True, download=shouldDownload, transform=transform)
    return trainset

def download_dataset(path, print=print):
    trainset = get_trainset(path=path, shouldDownload=True)
    print(f'dataset is downloaded and has {len(trainset)} items')
