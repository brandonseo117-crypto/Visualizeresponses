import numpy as np
import os
import numpy as np
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
import zipfile
import scipy.ndimage as ndimage
import io
import glob
import sys
import re
from scipy import stats
import pickle
import torch
import re
import gc
import time
import imageio
gpu_number = str(sys.argv[1])
gpu_device = gpu_number
print('using gpu ' + gpu_device)
os.environ["CUDA_VISIBLE_DEVICES"] = gpu_device


def predict_compact(image_data_orig, all_compact_models):
    batch_size = 100
    image_data = np.copy(image_data_orig).astype(np.float32)
    compact_model_response_list = torch.zeros(
        (image_data.shape[0], 1), dtype=torch.float32)
    print('Starting . . . ')
    mean_rgb = np.array([121.965696, 114.91127158, 105.86463286])
    model = tf.keras.models.load_model(f"{folder_path}{all_compact_models}")
    start_time = time.time()

    for i in range(0, len(image_data), batch_size):
        one_batch = image_data[i:i+batch_size]
        batch_chunked = one_batch

        batch_chunked[:, :, :, 0] = (batch_chunked[:, :, :, 0]) - mean_rgb[0]
        batch_chunked[:, :, :, 1] = batch_chunked[:, :, :, 1] - mean_rgb[1]
        batch_chunked[:, :, :, 2] = batch_chunked[:, :, :, 2] - mean_rgb[2]

        batch_predictions = model.predict(batch_chunked)
        batch_predictions = torch.tensor(
            batch_predictions, dtype=torch.float32)

        print(
            f'Doing these indexes {i}:{i+batch_size} | prediction shape {batch_predictions.shape}')
        compact_model_response_list[i:i +
                                    batch_size] = batch_predictions.view(-1, 1)
        print(compact_model_response_list.shape)
    del image_data
    del model
    del batch_chunked
    del one_batch
    tf.keras.backend.clear_session()
    return compact_model_response_list


def filename_to_int(filename):
    match = re.search(r'session(\d+)_neuron(\d+)', filename)
    if match:
        session, neuron = match.groups()
        return session, neuron
    return None


folder_path = '/DATA/cowley_lab/compact_models/compact_models_final/saved_models/'
all_compact_models_list = sorted(
    [f for f in os.listdir(folder_path) if f.endswith('.keras')])

dif_compact_models = []
for compact_model in all_compact_models_list:

    session, neuron = filename_to_int(compact_model)

    version_number = f'session_{session}_neuron_{neuron}'
    names = f'/DATA/scratch/gondur/models/{version_number}'
    # print(names)

    dif_compact_models.append(version_number)

dif_compact_models = dif_compact_models

for x in dif_compact_models:
    version_num = x  # 'version_plots'
    compact_model = 0
    folder_path = '/DATA/cowley_lab/compact_models/compact_models_final/saved_models/'
    all_compact_models = sorted(
        [f for f in os.listdir(folder_path) if f.endswith('.keras')])
    all_compact_models = all_compact_models[int(compact_model)]
    random_index_path = f'./random_idx_to_use_{all_compact_models[0][:-6]}.npy'
    image_dir = '/DATA/scratch/gondur/500k_natural_images/'
    response_dir = f'/DATA/scratch/gondur/models/{version_num}/'


def sort_images_responses(response_dir):

    response_files = sorted(glob.glob(os.path.join(
        response_dir, '500k_responses_batch_*.npy')))

    responses = []
    for resp_file in response_files:
        responses.append(np.load(resp_file, mmap_mode='r'))
    responses = np.concatenate(responses, axis=0)

    sorted_indices = np.argsort(responses.squeeze())
    min_resp = np.min(responses)
    max_resp = np.max(responses)
    del responses

    return sorted_indices, min_resp, max_resp


def sequential_search_random(indices, image_direct, batch_size=20000):
    if image_direct == image_dir:
        image_files = sorted(
            glob.glob(os.path.join(image_direct, 'batch_*.npy')))
    else:
        image_files = sorted(glob.glob(os.path.join(
            image_direct, '500k_responses_batch_*.npy')))

    first_image = np.load(image_files[0], mmap_mode='r')
    # indices_size, 112, 112, 3
    result = np.zeros((len(indices),) +
                      first_image[0].shape, dtype=first_image.dtype)

    found_indices = set()
    index_map = {idx: i for i, idx in enumerate(indices)}

    for file_idx, file_path in enumerate(image_files):

        start_idx = file_idx * batch_size
        end_idx = start_idx + batch_size
        relevant_indices = [
            idx for idx in indices if start_idx <= idx < end_idx]

        if relevant_indices:
            data = np.load(file_path, mmap_mode='r')

            for idx in relevant_indices:
                local_idx = idx - start_idx
                result_idx = index_map[idx]
                result[result_idx] = data[local_idx]
                found_indices.add(idx)

        if len(found_indices) == len(indices):
            break
    return result


# for 'idx_i_want' enter a number between 0 and 219 to get a compact model
# if you print 'modified ' you can see the name of the compact model
idx_i_want = 132
number_of_imgs = 8  # this will give you the top or bottom 20, you can change to any number!
max_mode = True  # False if you want anti-pref images, True for pref.
modified = [all_compact_models_list[idx_i_want]]

for x in modified:
    start = time.time()
    all_values = []
    results = {}
    session, neuron = filename_to_int(x)

    version_number = f'session_{session}_neuron_{neuron}'

    image_dir = '/DATA/scratch/gondur/500k_natural_images/'
    response_dir = f'/DATA/scratch/gondur/models/{version_number}/'

    sorted_indices, responses_avg_min, responses_avg_max = sort_images_responses(
        response_dir)

    print('$$$$$$$')
    if max_mode:
        max_indices = sorted_indices[-number_of_imgs:]
    else:
        max_indices = sorted_indices[:number_of_imgs]

    max_images = sequential_search_random(
        indices=max_indices, image_direct=image_dir)
    max_responses = sequential_search_random(
        indices=max_indices, image_direct=response_dir)
    fig, axes = plt.subplots(10, 2, figsize=(20, 20))

    # save images in a grid
    for idx, ax in enumerate(axes.flat):
        ax.imshow(max_images[idx])
        ax.axis('off')
    plt.subplots_adjust(wspace=0.01, hspace=0.01)
    if max_mode:
        plt.savefig(f"{idx_i_want}_max{x}image_grid.pdf",
                    bbox_inches='tight', pad_inches=0)
    else:
        plt.savefig(f"{idx_i_want}_min{x}image_grid.pdf",
                    bbox_inches='tight', pad_inches=0)
    plt.close()
    ######

    frames = []

    # below we make a gif with all the pref. or anti-pref images
    for img in max_images:
        frames.append(img)

    if max_mode:
        imageio.mimsave(f"max_{idx_i_want}_{x}_images.gif", frames, fps=5)

    else:
        imageio.mimsave(f"min_{idx_i_want}_{x}_images.gif", frames, fps=5)
