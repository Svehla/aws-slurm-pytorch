#!/usr/bin/env python
from torchvision import datasets, transforms

# TODO: download and prepare dataset from AWS s3 to use custom data
def get_trainset(shouldDownload: bool):
    mean = (0.5,)
    std_dev = (0.5,)
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean, std_dev)])
    trainset = datasets.MNIST('/shared/ai_app/train_datasets/mnist', train=True, download=shouldDownload, transform=transform)
    return trainset

def download_dataset(print=print):
    # print('downloading multinode dataset into shared file system')
    # print('=====================================================')
    trainset = get_trainset(True)
    print(f'dataset is downloaded and has {len(trainset)} items')
    # print()

if __name__ == '__main__':
    download_dataset()