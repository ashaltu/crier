import os
import numpy as np
import utils
from itertools import islice


# Local
import model_defs

class SearchEngine(object):
    def __init__(self, image_size, num_results):
      self.image_size = image_size
      self.num_results = num_results

    # Create image database.
    def create_database(self, encoder, corpus_dir):
      self.corpus_image_id_paths_map = utils.load_image_id_paths_map(corpus_dir)
      corpus_image_id_pil_map = utils.load_image_id_pil_map(self.corpus_image_id_paths_map, self.image_size)

      # Encode batched since load_image_id_arr_map eats memory.
      corpus_image_id_embedding_map = dict()
      pil_list = list(corpus_image_id_pil_map.items())
      num_batches = (len(self.corpus_image_id_paths_map) // model_defs.BATCH_SIZE) + 1
      for i in range(num_batches):
        pil_sub_list = pil_list[i*model_defs.BATCH_SIZE : (i+1)*model_defs.BATCH_SIZE]
        corpus_image_id_arr_map = utils.load_image_id_arr_map(dict(pil_sub_list))

        embedding_sub_map = utils.load_image_id_embedding_map(encoder, corpus_image_id_arr_map)
        print(f"LEN of old_embedding_map = {len(corpus_image_id_embedding_map)}")
        print(f"LEN of sub_map = {len(embedding_sub_map)}")
        print(f"LEN of unpack = {len({**embedding_sub_map,**corpus_image_id_embedding_map})}")
        corpus_image_id_embedding_map.update(embedding_sub_map)
        print(f"LEN of embedding_map = {len(corpus_image_id_embedding_map)}")

      assert(len(self.corpus_image_id_paths_map) == len(corpus_image_id_embedding_map))
      self.search_engine = utils.load_search_engine(corpus_image_id_embedding_map.values(), self.num_results)

    # Update image database.
    # Expects new images in the corpus or a different corpus.
    def update_database(self, encoder, corpus_dir):
      self.create_database(encoder, corpus_dir)

    # Search image database and return image index, images themselves, and the distances ranked.
    def search_database(self, encoder, image_path):
      img_arr = utils.image_path_to_arr(image_path, self.image_size)
      image_embedding = encoder.predict(np.array([img_arr]))

      neighbors, distances = self.search_engine.search_batched(image_embedding)
      #images = []   # Uncomment if wanting to send images back to client.
      image_paths = []
      for idx, neighbor in enumerate(neighbors[0]):
        #images.append(self.corpus_image_id_pil_map[neighbor]) # Neighbor = id # Uncomment if wanting to send images back to client.
        image_paths.append((self.corpus_image_id_paths_map[neighbor]))

        # print(f"Image {neighbor} distance: {distances[0][idx]}")
        # display(self.corpus_image_id_pil_map[neighbor]) # Jupyter/Colab notebook only.
      
      #return neighbors, images, image_paths, distances
      return neighbors, image_paths, distances
    
    # Search image database and return image index, images themselves, and the distances ranked.
    def search(self, encoder, image_path):
      return self.search_database(encoder, image_path)
