from tpdataset import RawDataSet, DataDownloader
from torchvision import datasets
from torchvision import transforms
from torch.utils.data import DataLoader
from pyctlib import vector, path, fuzzy_obj
import math
import torch

class CelebA(fuzzy_obj):

    def __init__(self, root="", transform="defalut"):

        self.root = root
        if isinstance(transform, str) and transform == "default":
            self.trans = transforms.ToTensor()
        else:
            self.trans = transform

        self.__train_set = datasets.CelebA(root=str(root), split="train", transform=self.trans, download=True)
        self.__test_set = datasets.CelebA(root=str(root), split="test", transform=self.trans, download=False)

    @property
    def train_set(self):
        if hasattr(self, "_CelebA__train_set_vector"):
            return self.__train_set_vector
        self.__train_set_vector = vector(self.__train_set, str_function=lambda x: "\n".join(["Dataset CelebA", "    Number of datapoints: {}".format(x.length), "    Split: Train"]))
        return self.__train_set_vector

    @property
    def test_set(self):
        if hasattr(self, "_CelebA__test_set_vector"):
            return self.__test_set_vector
        self.__test_set_vector = vector(self.__test_set, str_function=lambda x: "\n".join(["Dataset CelebA", "    Number of datapoints: {}".format(x.length), "    Split: Test"]))
        return self.__test_set_vector

    def train_dataloader(self, batch_size=1, shuffle=True, num_workers=0, pin_memory=True):
        return DataLoader(self.__train_set, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers, pin_memory=pin_memory)

    def train_val_dataloader(self, batch_size=1, shuffle=True, num_workers=0, pin_memory=True, split=[50000, 10000]):
        train, val = torch.utils.data.random_split(self.__train_set, lengths=split)
        return DataLoader(train, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers, pin_memory=pin_memory), DataLoader(val, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=pin_memory)

    def test_dataloader(self, batch_size=1, shuffle=False, num_workers=0, pin_memory=True):
        return DataLoader(self.__test_set, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers, pin_memory=pin_memory)
