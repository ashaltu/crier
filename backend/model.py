import os
import numpy as np

import tensorflow as tf
import tensorflow_hub as tfhub

# Local
import utils
import search_engine
import model_defs

class CRIER(object):
    def __init__(self, model_dir, image_size, num_results=10, batch_size=model_defs.BATCH_SIZE):
      self.num_results = num_results
      self.image_size = image_size
      self.batch_size = batch_size

      self.encoder = tf.keras.Sequential(
          [
            tf.keras.layers.InputLayer(input_shape=self.image_size + (3,)),
            tfhub.KerasLayer(model_dir, trainable=False),  # Can be True, see below.
          ])
      self.encoder.build((None,)+self.image_size+(3,))        # Batch input shape.
      self.encoder.summary()  

      self.token_threads = set()
      self.engines = dict()
    
    # Creates a new search engine mapped from its corpus directory. If corpus directory already exists, does nothing.
    def create_engine(self, corpus_dir):
      if corpus_dir in self.engines: return

      self.engines.update({corpus_dir: search_engine.SearchEngine(self.image_size, self.num_results)})

    # Deletes a search engine mapped from its corpus directory. If corpus directory doesn't exist, does nothing.
    def delete_engine(self, corpus_dir):
      if corpus_dir not in self.engines or not self.engine_available(os.path.basename(corpus_dir)): return

      self.engines.pop(corpus_dir, None)

    # See SearchEngine.create_database.
    def create_database(self, corpus_dir):
      if corpus_dir not in self.engines or not self.engine_available(os.path.basename(corpus_dir)): return

      self.engines[corpus_dir].create_database(self.encoder, corpus_dir)
      if not self.engine_available(corpus_dir): self.token_threads.remove(corpus_dir)
      print(f"Finished indexing job on token: {corpus_dir}")

    # See SearchEngine.update_database.
    def update_database(self, corpus_dir):
      if corpus_dir not in self.engines or not self.engine_available(os.path.basename(corpus_dir)): return

      self.engines[corpus_dir].update_database(self.encoder, corpus_dir)
      if not self.engine_available(corpus_dir): self.token_threads.remove(corpus_dir)
      print(f"Finished indexing job on token: {corpus_dir}")

    # See SearchEngine.search_database.
    def search_database(self, corpus_dir, image_filename):
      if corpus_dir not in self.engines or not self.engine_available(os.path.basename(corpus_dir)): return None

      image_path = os.path.join(corpus_dir, image_filename)
      return self.engines[corpus_dir].search_database(self.encoder, image_path)
    
    # See SearchEngine.search.
    def search(self, corpus_dir, image_filename):
      if corpus_dir not in self.engines or not self.engine_available(os.path.basename(corpus_dir)): return None

      image_path = os.path.join(corpus_dir, image_filename)
      return self.engines[corpus_dir].search(self.encoder, image_path)

    def engine_available(self, token):
      return os.path.basename(token) not in self.token_threads
