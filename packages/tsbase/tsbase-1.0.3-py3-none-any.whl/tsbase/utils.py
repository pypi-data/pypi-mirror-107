

def set_seed_tf(seed_value=42, is_gpu=True, is_display=False):
    import os
    import random
    import numpy as np
    import tensorflow as tf

    os.environ['PYTHONHASHSEED'] = '0'
    if is_gpu:
        os.environ['CUDA_VISIBLE_DEVICES'] = ""
    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = "-1"

    np.random.seed(seed_value)
    random.seed(seed_value)
    tf.random.set_seed(seed_value)

    if is_display:
        print('设置随机种子: {}  是否启用GPU： {}' . format(seed_value, is_gpu))
    

def set_seed(seed_value, is_display=False):
    import random
    import numpy as np

    random.seed(seed_value)
    np.random.seed(seed_value)

    if is_display:
        print('设置随机种子: {}' . format(seed_value))
