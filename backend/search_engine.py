import os
import numpy as np
import utils

class SearchEngine(object):
    def __init__(self, image_size, num_results):
      self.image_size = image_size
      self.num_results = num_results

    # Create image database.
    def create_database(self, encoder, corpus_dir):
      self.corpus_image_id_paths_map = utils.load_image_id_paths_map(corpus_dir)
      self.corpus_image_id_pil_map = utils.load_image_id_pil_map(self.corpus_image_id_paths_map, self.image_size)
      self.corpus_image_id_arr_map = utils.load_image_id_arr_map(self.corpus_image_id_pil_map)
      self.corpus_image_id_embedding_map = utils.load_image_id_embedding_map(encoder, self.corpus_image_id_arr_map)
      self.search_engine = utils.load_search_engine(self.corpus_image_id_embedding_map.values(), self.num_results)

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