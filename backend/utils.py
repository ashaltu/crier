import os
import glob
import math
import random

import numpy as np

import scann
import tensorflow as tf

# Build dict mapping image ids to their paths.
def load_image_id_paths_map(images_dir):
  dir_prefix = os.path.join(os.getcwd(), images_dir)
  image_paths = []
  for ext in ['*.png', '*.jpg', '*.jpeg', '*.JPEG', '*.PNG', '*.JPG']:
    image_paths.extend(glob.glob(os.path.join(dir_prefix, ext)))
  return {idx: path for idx, path in enumerate(image_paths)}

# Build dict mapping image ids to PIL image instances.
def load_image_id_pil_map(image_id_paths_map, image_size):
  map = dict()

  for k in sorted(image_id_paths_map.keys()):
    map.update({idx: tf.keras.preprocessing.image.load_img(
                        path=image_id_paths_map[k],
                        target_size=image_size,
                        interpolation='bilinear'
                     )
               })
    
  return map

# Normalize an image array to the following range: [0, 1].
def normalize_img_arr(arr):
  return tf.keras.utils.normalize(arr, axis=-1, order=2)

# Build dict mapping image ids to image arrays.
def load_image_id_arr_map(image_id_pil_map):
  map = dict()

  for k in sorted(image_id_pil_map.keys()):
    img_arr = tf.keras.preprocessing.image.img_to_array(image_id_pil_map[k])
    norm_img_arr = normalize_img_arr(img_arr)
    map.update({idx: norm_img_arr})
    
  return map

# Build dict mapping image ids to embeddings.
def load_image_id_embedding_map(model, image_id_arr_map):
  map = dict()
  inputs = []
  for k in sorted(image_id_arr_map.keys()):
    inputs.append(image_id_arr_map[k])
  
  batched_img_arrs = np.array(inputs)
  predictions = model.predict(batched_img_arrs)
  print(len(predictions))
  for idx, embedding in enumerate(predictions):
    map.update({idx: embedding})

  return map

# Build a ScaNN index for later ANN lookups.
def load_search_engine(corpus_image_embeddings, num_results, similarity_function="dot_product"):
  dataset = np.array(list(corpus_image_embeddings))
  num_leaves = int(math.sqrt(len(corpus_image_embeddings)))

  search_engine = scann.scann_ops_pybind.builder(dataset, num_results, similarity_function).score_brute_force().build()
  return search_engine

def image_path_to_arr(image_path, image_size):
  pil_image = tf.keras.preprocessing.image.load_img(
                    path=image_path,
                    target_size=image_size,
                    interpolation='bilinear'
                  )
  img_arr = tf.keras.preprocessing.image.img_to_array(pil_image)
  norm_img_arr = normalize_img_arr(img_arr)

  return norm_img_arr

def rand():
  return np.base_repr(int(str(random.random())[2:]), 36).lower()

def generate_token():
  return rand()+rand()