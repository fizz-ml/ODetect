import torch.nn as nn
from torch.autograd import Variable

def CausalConv1d(in_channel, out_channel, kernel_size, dilation=1, **kwargs):
    """
    Performs a causal convolution by padding the input.
    # Padding needs to account for dilation*kernelsize
    # out ----------->0
    #     |     |     |
    # in  p p p p p p 0 1 2 3 4
    """
    padding = (kernel_size-1)*dilation
    return nn.Conv1d(in_channel, out_channel, kernel_size, padding=padding, dilation=dilation, **kwargs)


class CausalCNN(nn.Module):
    def __init__(self):
        super().__init__()
        h1 = 8
        self.conv1 = CausalConv1d(1, h1, kernel_size=3, dilation=3, stride=4)
        self.conv2 = CausalConv1d(h1, h1, kernel_size=3, dilation=3, stride=4)
        self.conv3 = CausalConv1d(h1, h1, kernel_size=2, dilation=2)
        self.conv4 = CausalConv1d(h1, h1, kernel_size=2, dilation=4)
        self.conv5 = CausalConv1d(h1, 1, kernel_size=2, dilation=8)
        self.nl = nn.ReLU()

    def forward(self, x):
        in_length = 1600 #len(x)
        print(in_length)
        x = self.conv1(x)
        x = x[:,:,:in_length//4] # remove trailing padding
        x = self.nl(x)

        x = self.conv2(x)
        x = x[:,:,:in_length//4//4] # remove trailing padding
        x = self.nl(x)

        x = self.conv3(x)
        x = x[:,:,:in_length//4//4] # remove trailing padding
        x = self.nl(x)

        x = self.conv4(x)
        x = x[:,:,:in_length//4//4] # remove trailing padding
        x = self.nl(x)

        x = self.conv5(x)
        x = x[:,:,:in_length//4//4] # remove trailing padding
        print(x.size())

        return x

