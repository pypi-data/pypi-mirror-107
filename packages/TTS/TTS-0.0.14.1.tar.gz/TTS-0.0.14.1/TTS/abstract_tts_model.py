class TTSModel(nn.Module):
    def __init__(self,):
    """initialize layers, variables and model parameter."""
        ...

    def forward(self):
    """Forward pass for training."""
        ...
        return outputs_dict

    def inference(self):
    """Forward pass for inference."""
        ...
        return outputs_dict

    def train_step(self, batch, criterion):
    """A Single training pass for the model. It takes a batch of instances and
    computes the loss and returns loss_dict and the model outputs.
    """
        ...
        return outputs_dict, loss_dict

    def train_log(self, ap, batch, outputs):
    """Visualizations and special logs to be projected to the Logger in use."""
        ...
        return figures_dict, train_audios

    def eval_step(self, batch, critetion):
    """A single evaluation pass for the model. It takes a batch of instances and
    computed the loss and returns loss_dict and the model outputs.

    It is in general very similar to the `train_step`.
    """
        ...
        return outputs_dict, loss_dict

    def eval_log(self, ap, batch, outputs):
    """Similar to the `train_log` but for evaluation."""
        ...
        return figures_dict, eval_audios

    def load_checkpoint(self, config, checkpoint_path, eval=False):
    """Load a pretrained model and make it ready for inference"""
        ...