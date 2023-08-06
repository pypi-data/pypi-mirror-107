
import tqdm
import torch


def set_seed_torch(seed_value=42):
    import os
    import random
    import numpy as np

    seed_value = int(seed_value)
    random.seed(seed_value)
    np.random.seed(seed_value)
    os.environ['PYTHONHASHSEED'] = str(seed_value)
    torch.manual_seed(seed_value)                    # 为CPU设置随机种子
    torch.cuda.manual_seed(seed_value)               # 为当前GPU设置随机种子
    torch.cuda.manual_seed_all(seed_value)           # 为所有GPU设置随机种子
    # CUDNN
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.enabled = False

    print('[Torch]  Random seed: {}' . format(seed_value))


def fit(x, y, validation_data=None,
        epochs=30, batch_size=16,
        model=None, optimizer=None, criterion=None,
        verbose=True, is_gpu=False, lr=0.001):
    """
    Train neural network
    Args:
        x (numpy.ndarray):                        X
        y (numpy.ndarray):                        y
        validation_data (tuple, list or None):    (val_x, val_y) or [val_x, val_y]
        epochs (int):                             Epochs
        batch_size (int):                         Number of samples of each batch
        model (torch.nn.Module):                  Neural network based on torch framework
        optimizer (torch optim, str):             Optimizer in torch framework
        lr (float):                               Learning rate for optimizer
        criterion (torch loss, str):              Loss function in torch framework
        verbose (bool):                           Whether to display information about the training
        is_gpu (bool):                            Whether to train neural network on GPU
    Returns:
        model (torch model):                      Trained model
    """

    # Numpy array converts to torch tensor
    _x, _y = torch.from_numpy(x), torch.from_numpy(y)
    # Move model to GPU
    if is_gpu:
        model.cuda()
    # Optimizer
    if isinstance(optimizer, str):
        if optimizer in ['SGD', 'sgd']:
            optimizer = torch.optim.SGD(model.parameters(), lr=lr)
        elif optimizer in ['adam', 'Adam']:
            optimizer = torch.optim.Adam(model.parameters(), lr=lr)
        elif optimizer in ['RMSprop']:
            optimizer = torch.optim.RMSprop(model.parameters(), lr=lr)
    # Loss function
    if isinstance(criterion, str):
        if criterion in ['mse', 'MSE', 'mean_squared_error']:
            criterion = torch.nn.MSELoss()
        elif criterion in ['mae', 'MAE', 'mean_absolute_error']:
            criterion = torch.nn.L1Loss()
    # Train model
    n_samples = _x.shape[0]
    n_batch = n_samples // batch_size
    info = dict()
    history = {'loss': [], 'val_loss': []}
    for ep in range(epochs):
        # Progress bar
        if verbose:
            progress_bar = tqdm.tqdm(range(n_batch+1), disable=False)
            progress_bar.set_description(f'[Train {ep+1:4d}/{epochs}]')
        else:
            progress_bar = tqdm.tqdm(range(n_batch+1), disable=True)

        # Train
        tr_loss_per_ep = 0
        for k in progress_bar:
            if k != n_batch:
                if is_gpu:
                    x_batch = _x[k * batch_size:].cuda()
                    y_true = _y[k * batch_size:].cuda()
                else:
                    x_batch = _x[k * batch_size:]
                    y_true = _y[k * batch_size:]
            else:
                if is_gpu:
                    x_batch = _x[k * batch_size: (k + 1) * batch_size].cuda()
                    y_true = _y[k * batch_size: (k + 1) * batch_size].cuda()
                else:
                    x_batch = _x[k * batch_size: (k + 1) * batch_size]
                    y_true = _y[k * batch_size: (k + 1) * batch_size]

            # Zero the parameter gradients
            optimizer.zero_grad()
            # Forward
            y_pred = model(x_batch)
            loss = criterion(y_pred, y_true)
            # Backward
            loss.backward()
            # Optimize
            optimizer.step()
            # Loss value of each epoch
            tr_loss_per_ep += loss.item()
            info['loss'] = tr_loss_per_ep

            # Validate
            if validation_data is not None:
                val_x, val_y_true = torch.from_numpy(validation_data[0]), torch.from_numpy(validation_data[1])
                if is_gpu:
                    val_x, val_y_true = val_x.cuda(), val_y_true.cuda()
                with torch.no_grad():
                    val_y_pred = model(val_x)
                val_loss = criterion(val_y_pred, val_y_true)
                info['val_loss'] = val_loss.item()

            # Display info
            if verbose:
                progress_bar.set_postfix(info)
        progress_bar.close()

        # History
        for key in info.keys():
            history[key].append(round(info[key], 6))

    return model, history


def predict(x, model, is_gpu):
    """
    Predict by using trained model
    Args:
        x (numpy.ndarray):         X
        model (torch.nn.Module):   Neural network based on torch framework
        is_gpu (bool):             Whether to train neural network on GPU
    Returns:
        y_pred (numpy array):      Predicted results, shape=(len(x), n_outputs)
    """

    # Numpy array converts to torch tensor
    _x = torch.from_numpy(x)
    with torch.no_grad():
        if is_gpu:
            y_pred = model(_x.cuda())
            y_pred = y_pred.cpu()
        else:
            y_pred = model(_x)
    y_pred = y_pred.detach().numpy()
    return y_pred
