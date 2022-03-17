import matplotlib.pyplot as plt
import cv2
import os
import glob
import numpy as np

# Local
import token_manager
import utils

NUM_BINS = 256 # Each channel has range of [0, 255].

def compute_l2_distance(a, b):
  return np.linalg.norm(a-b)

def normalize_img(img):
  # Same preprocessing done: resize image, use bilinear interpolation.
  img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
  return img
  #return cv2.resize(img, token_manager.IMAGE_SIZE, interpolation=cv2.INTER_LINEAR)

def compute_histogram1(image_path):
  im = cv2.imread(image_path)
  im = normalize_img(im)
  vals = im.mean(axis=2).flatten()
  b, bins, patches = plt.hist(vals, NUM_BINS)

  return np.concatenate([b, bins])

def compute_histogram(image_path):
  im = cv2.imread(image_path)
  im = normalize_img(im)
  hist = cv2.calcHist([im], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
  return cv2.normalize(hist, hist).flatten()

def compute_histograms(corpus_dir):
    dir_prefix = os.path.join(os.getcwd(), corpus_dir)
    image_paths = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.JPEG', '*.PNG', '*.JPG']:
      image_paths.extend(glob.glob(os.path.join(dir_prefix, ext)))
    
    bstack = np.empty((0,  8 * 8 * 8))
    for image_path in image_paths:
      embedding = compute_histogram(image_path)
      bstack = np.vstack((bstack, embedding))

    return image_paths, bstack

class HistogramRetrieval(object):
  def __init__(self, corpus_dir, num_results):
    print("Computing histograms...")
    self.image_paths, self.histogram_embeddings = compute_histograms(corpus_dir)
    print("Histograms computed.")

    print("Indexing embeddings... ")
    self.search_engine = utils.load_search_engine(self.histogram_embeddings, num_results)
    print("Successfully indexed embeddings.")

  def search(self, img_to_search_path):
    histogram_embedding = compute_histogram(img_to_search_path)

    neighbors, distances = self.search_engine.search_batched([histogram_embedding])
    image_paths = []
    for idx, neighbor in enumerate(neighbors[0]):
      image_paths.append((self.image_paths[neighbor]))
    
    return neighbors, image_paths, distances[0]



def example_run():
  example_image_path = "example_image_corpus/fcat.jpg"
  retriever = HistogramRetrieval("example_image_corpus", 10)

  _, image_paths, distances = retriever.search(example_image_path)

  for image_path, distance in zip(image_paths, distances):
    print(f"Image {os.path.basename(image_path)} with distance {distance}")


# example_run()