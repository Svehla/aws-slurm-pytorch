#!/usr/bin/env python3

# TODO: add multinode fine tuned llama
# TODO: run this file on single GPU/on local machine with mac chip
# TODO: rewrite model into jupyter + unable export it into DDP
# big inspiration taken from:
# https://github.com/pytorch/examples/blob/main/distributed/ddp-tutorial-series/multinode.py

# TODO: make this script available to run distributed and on local PC as well somehow
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
import torch.nn.functional as F
from torch.utils.data.distributed import DistributedSampler
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.distributed import init_process_group, destroy_process_group
import os
from torch.utils.tensorboard import SummaryWriter
from torchvision import datasets, transforms
from download_multinode_dataset import get_trainset
import torch
import numpy as np
import random
from model import ToyMnistModel


# ----------- setup logging ------------

# TODO: how to import shared.py with colorized func?
# import sys
# sys.path.append('/shared/{APP}/source_code/shared')
# from ..shared import colorize_red
# i should run source /shared/{APP}/my-venv/bin/activate 
# at the bagging before the script will start but it works for some reason... magic

def create_colorize_func(color_code: str):
    def colorize(input_string: str) -> str:
        return f"\033[{color_code}m{input_string}\033[0m"
    return colorize

colorize_blue = create_colorize_func("94")
# colorize_red = create_colorize_func("91")
# colorize_gray = create_colorize_func("90")
# colorize_yellow = create_colorize_func("93")
# colorize_green = create_colorize_func("92")


og_print = print
print = lambda *args, **kwargs: og_print(
    colorize_blue(f'[GR:{global_rank}LR:{local_rank}]'),
    *args,
    **kwargs
)

# from torch.profiler import profile, record_function, ProfilerActivity
# ----------- env variables ------------

# env parsing => TODO: add typed-env-parser ts alternative
local_rank = int(os.environ["LOCAL_RANK"])
global_rank = int(os.environ["RANK"])
IS_MAIN_NODE = global_rank == 0 and local_rank == 0

print('is_main_log_node', IS_MAIN_NODE)
# TODO: add pytorch writer
# writer = SummaryWriter(f'/shared/{APP}/tensor_board_logs/{experiment_name}')

# ----------- setup seeds ------------

def set_seeds(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

set_seeds(1234)

device = torch.device(local_rank if torch.cuda.is_available() else torch.device('cpu'))

print(f'device: {device}')

class Trainer:
    def __init__(
        self,
        model: torch.nn.Module,
        train_data: DataLoader,
        optimizer: torch.optim.Optimizer,
        save_every: int,
        snapshot_path: str,
    ) -> None:
        
        # local_rank = int(os.environ["LOCAL_RANK"])
        # global_rank = int(os.environ["RANK"])

        # TODO: is this .to() gpu assign correct?
        self.model = model.to(device)
        is_model_cuda = next(self.model.parameters()).is_cuda
        print(f'init trainer log: global_rank: {global_rank}, local_rank: {local_rank}, use cuda: {is_model_cuda}')
        self.train_data = train_data
        self.optimizer = optimizer
        self.save_every = save_every
        self.epochs_run = 0
        self.snapshot_path = snapshot_path
        if os.path.exists(snapshot_path):
            print("Loading snapshot")
            self._load_snapshot(snapshot_path)

        # register backward hooks for sharing gradients across ranks
        self.model = DDP(self.model, device_ids=[local_rank])

    def _load_snapshot(self, snapshot_path):
        loc = f"cuda:{local_rank}"
        snapshot = torch.load(snapshot_path, map_location=loc)
        self.model.load_state_dict(snapshot["MODEL_STATE"])
        self.epochs_run = snapshot["EPOCHS_RUN"] # this is last stored 
        print(f"Resuming training from snapshot at Epoch {self.epochs_run}")

    def _run_batch(self, source, targets):
        self.optimizer.zero_grad()
        output = self.model(source)
        loss = F.cross_entropy(output, targets) # cross_entropy returns scalar with averaged batches
        # loss for whole batch
        # print(loss)
        loss.backward()
        self.optimizer.step()
        return loss

    def _run_epoch(self, epoch):
        # pytorch profiler???
        # with profile(
        #     activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA],
        #     record_shapes=True,
        #     profile_memory=True,
        #     with_stack=True
        # ) as prof:
        #     with record_function("_run_batch"):
        """
        batch size should be computed by this:
        Start with a small batch size, such as 1 or 2.
        Increase the batch size until you encounter an Out of Memory (OOM) error.
        Once you hit an OOM error, reduce the batch size by one or two units.
        This value should be the maximum possible batch size that you can use without exhausting your GPU memory.
        """
        b_sz = len(next(iter(self.train_data))[0])
        self.train_data.sampler.set_epoch(epoch)
        loss = None
        for source, targets in self.train_data:
            source = source.to(device)
            targets = targets.to(device)
            loss = self._run_batch(source, targets)
            loss = loss.item()

            # prof.step()

        # should all processes have the same loss? if they share gradients via DDP?
        # avg_loss = sum(all_losses) / len(all_losses)
        # I think that this is working well, but dataset is shit => TODO: apply mnist 
        # print('batch loss', avg_loss, avg_loss + epoch)

        print(f"[GPU{global_rank}] Epoch {epoch} | Batchsize: {b_sz} | Steps: {len(self.train_data)} | Loss: {loss}")
        # write from 
        # this if is not working!!! why
        writer.add_scalar('Loss', loss, epoch)
        if global_rank == 0 and local_rank == 0:
            print(f"[GPU{global_rank}] Epoch {epoch} | Batchsize: {b_sz} | Steps: {len(self.train_data)} | Loss: {loss}")
            print('tb add_scalar is not working', loss, epoch)
            
            # print(global_rank, type(global_rank))


    def _save_snapshot(self, epoch):
        # if i Kil learning process and restore it from the state, tensorboard state will not be restored
        # so the overlaps (removed forwards) will be glitched in the UI
        snapshot = {
            "MODEL_STATE": self.model.module.state_dict(),
            "EPOCHS_RUN": epoch,
        }
        torch.save(snapshot, self.snapshot_path)
        """
        # TODO: upload snapshot into s3 bucket to AI store weights
        s3 = boto3.client('s3')
        # args are global for a whole script
        bucket_name = f'pravoai-public/{experiment_name}'
        s3.upload_file(self.snapshot_path, bucket_name, key)
        """

        print(f"Epoch {epoch} | Training snapshot saved at /shared file system {self.snapshot_path}")

    def train(self, max_epochs: int):
        for epoch in range(self.epochs_run, max_epochs):
            self._run_epoch(epoch)
            is_end_of_save_every_cycle = (epoch % self.save_every == (self.save_every -1))
            # every node stores snapshot into shared file system => only one should do it !
            if is_end_of_save_every_cycle and IS_MAIN_NODE:
                self._save_snapshot(epoch)


def load_train_objs():
    # train_set = MyTrainDataset(2048)  # load your dataset
    train_set = trainset # train_loader # 
    # print('train_set.shape')
    # print(train_set.shape)
    # model = torch.nn.Linear(20, 1)  # load your model
    model = ToyMnistModel()
    optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)
    return train_set, model, optimizer


def prepare_dataloader(dataset: Dataset, batch_size: int):
    return DataLoader(
        dataset,
        batch_size=batch_size,
        pin_memory=True,
        shuffle=False,
        sampler=DistributedSampler(dataset)
    )

def ddp_setup():
    init_process_group(backend="gloo")
    # init_process_group(backend="nccl")
    torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))

def main(save_every: int, total_epochs: int, batch_size: int, snapshot_path: str):
    ddp_setup()
    dataset, model, optimizer = load_train_objs()
    train_data = prepare_dataloader(dataset, batch_size)
    trainer = Trainer(model, train_data, optimizer, save_every, snapshot_path)
    trainer.train(total_epochs)
    destroy_process_group()
    writer.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='simple distributed training job')
    parser.add_argument('--total_epochs', type=int, help='Total epochs to train the model')
    parser.add_argument('--save_every', type=int, help='How often to save a snapshot')
    parser.add_argument('--batch_size', default=32, type=int, help='Input batch size on each device (default: 32)')
    parser.add_argument('--experiment_name', type=str, help='ID for Tensorboard + checkpoint file')
    parser.add_argument('--dataset_path', type=str, help='')
    parser.add_argument('--snapshots_dir', type=str, help='')
    # put writer into constructor of trainer, or keep it global?
    args = parser.parse_args()
    
    experiment_name = args.experiment_name
    # TODO: extract paths to run it from different envs as well
    # summary writer should be initialized only on the one node
    # use: f"{tempfile.gettempdir()}/{experiment_name}"


    # ----------- getting datasets ------------

    trainset = get_trainset(path=args.dataset_path, shouldDownload=False)

    # -----------------------------------------

    if IS_MAIN_NODE:
        # TODO: extract paths to run it from different envs as well
        if not os.path.exists(args.snapshots_dir):
            os.makedirs(args.snapshots_dir)


    writer = SummaryWriter(f'../tensor_board_logs/{args.experiment_name}')
    snapshot_path = f"{args.snapshots_dir}/{args.experiment_name}.pt"

    main(args.save_every, args.total_epochs, args.batch_size, snapshot_path)


    print('multinode_torchrun ended successfully! bye bye :wave:')
    # TODO: put checkpoints into s3
    # TODO: show loss in tensorboard
