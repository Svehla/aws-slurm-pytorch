import torch.nn as nn
import torch.nn.functional as F

# model.py ------------------------- MNIST
# TODO: make some better source code file system abstraction
class ToyMnistModel(nn.Module):
    """ Network architecture. """
    def __init__(self):
        super(ToyMnistModel, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)


    # DDP connects into pytorch autograd_hook
    # autograd_hooks are passes in forward function and waiting till backward is computed to distribute gradients over nodes
    # remove: rewrite forward and when it's called it sends gradients to other nodes + aggregate results
    def forward(self, x):
        x = F.relu(F.max_pool2d(self.conv1(x), 2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x, training=self.training)
        x = self.fc2(x)
        # print(x.shape)
        # log softmax is applied into the last layer => not to the batches

        # log_softmax === log(softmax)
        # log_softmax + NLLLoss == CrossEntropyLoss => https://www.youtube.com/watch?v=6ArSys5qHAU&ab_channel=StatQuestwithJoshStarmer
        # return F.log_softmax(x, dim=-1)
        return x

# ----------------------------------