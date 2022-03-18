import os
import random
import numpy as np
import matplotlib.pyplot as plt

import ml_metrics as metrics
import recmetrics

# Local
import histogram
import model
import token_manager

def get_basenames(arr, d=2): # d=2 or d=1, anything else unsupported
    if d==2: 
        ret = []
        for subarr in arr:
            ret.append([os.path.basename(v) for v in subarr])
        return ret

    return [os.path.basename(v) for v in arr]

def slice_columns(arr, k=5):  # assumes 2d array
    return [v[:k] for v in arr]

def calc_mapk(actual, expected, k):
    mapk = metrics.mapk(expected, slice_columns(actual, k), k)
    return mapk

def calc_mark(actual, expected, k):
    mark = recmetrics.mark(expected, slice_columns(actual, k), k)
    return mark

# The first values' most similar image is the second value.
def extractSimilarImagesAnswers(filepath):
    similar_images = dict()
    with open(filepath) as f:
        for line in f.readlines():
            input_output = [v.strip() for v in line.split(' ')]
            rel_list = similar_images[input_output[0]] if input_output[0] in similar_images else []
            rel_list.append(input_output[1])
            similar_images.update({input_output[0]: rel_list})

    return similar_images

'''
  The cifar_dir structure BEFORE:
    -cifar_dir
      -test
        -class0
          -img001.png
          -img002.png
          -img950.png
        -class7
          -img001.png
          -img002.png
          -img950.png
  
  expected_paths is extracted as such:  # should align with actual_paths in terms of input to output
    [
      ['img103.png', ..., 'img481.png'], # retrieved images similar to dogs (a specific dog image)
      ['img937.png', ..., 'img168.png'], # retrieved images similar to cats (a specific cat image)
    ]

  AND the cifar_dir structure AFTER:
    -cifar_dir
      -index_corpus
        -img100001.png
        -img100002.png
        -img100950.png
      -test_corpus
        -img01.png
        -img02.png
        -img50.png

  Function also works with Imagenette, make sure to set original_dir_name
'''
def extractSimilarImagesAnswersCifarOrImagenette(cifar_dir, original_dir_name='test', per_class_num_index=95):
    # Need test_image_names (5 images in each class, total of 500 test imgs):
    # Make similar_images as mentioned above^
    # For each class dir, turn it's images into a list and shuffle
    # Turn entire test_corpus values into single list and shuffle (save into test_image_names).
    # While doing above step, generate expected_paths 
 
    # Also need to reorganize into new file structure
    os.mkdir(os.path.join(cifar_dir, "index_corpus"))
    os.mkdir(os.path.join(cifar_dir, "test_corpus"))

    test_image_paths = []
    expected_paths = []
    for dir in os.listdir(os.path.join(cifar_dir, original_dir_name)):
      class_img_names = os.listdir(os.path.join(cifar_dir, original_dir_name, dir))
      random.shuffle(class_img_names)

      sub_expected_paths = []
      for img_name in class_img_names[:per_class_num_index]:
        new_img_path = os.path.join(cifar_dir, "index_corpus", img_name)
        os.rename(os.path.join(cifar_dir, original_dir_name, dir, img_name), new_img_path)
        sub_expected_paths.append(new_img_path)
      
      for img_name in class_img_names[per_class_num_index:]:
        new_img_path = os.path.join(cifar_dir, "test_corpus", img_name)
        os.rename(os.path.join(cifar_dir, original_dir_name, dir, img_name), new_img_path)
        test_image_paths.append(new_img_path)
        expected_paths.append(sub_expected_paths)

    return test_image_paths, expected_paths

# count how many relevants images from top-k actual.
# assumes actuals and expecteds to align in input_outputs
# assumes actuals is ranked by most relevant in beginning
def topKPresent(k, actuals, expecteds, image_names):
    n = len(actuals) # num of images
    c_retrieved_relevant_counts = [0] * n
    e_retrieved_relevant_counts = [0] * n
    for i in range(n):
        e_retrieved_relevant_counts[i] = len(expecteds[i])

        #print(f"image name: {image_names[i]}")
        #print(f"actual: {actuals[i][:k]}")
        #print(f"expected: {expecteds[i]}")
        for actual in actuals[i][:k]:
            c_retrieved_relevant_counts[i] = c_retrieved_relevant_counts[i] + int(actual in expecteds[i])
        #print(f"relevant correct: {c_retrieved_relevant_counts[i]}")

    return c_retrieved_relevant_counts, e_retrieved_relevant_counts

'''
    actual_paths:   [[retrieved_img11, retrieved_img12, ..., retrieved_img1M],
                     [retrieved_img21, retrieved_img22, ..., retrieved_img2M],
                     ...
                     [retrieved_imgN1, retrieved_imgN2, ..., retrieved_imgNM]],
    expected_paths: [[relevant_img11, relevant_img12, ..., relevant_img1M],
                     [relevant_img21, relevant_img22, ..., relevant_img2M],
                     ...
                     [relevant_imgN1, relevant_imgN2, ..., relevant_imgNM]]                   
'''
def precision(actual_paths, expected_paths, k, image_names):
    n = len(image_names)
    correct_retrieved_relevant_counts, expected_retrieved_relevant_counts = topKPresent(k, actual_paths, expected_paths, image_names)
    actual_tp = np.sum(correct_retrieved_relevant_counts)
    possible_tp = np.sum([min(k, expected_rr_count) for expected_rr_count in expected_retrieved_relevant_counts])

    #print(f"actual_tp: {actual_tp}")
    #print(f"possible_tp: {possible_tp}")
    p = actual_tp / possible_tp     # We only care about the top-K results. FIX MAYBE?

    print(f"Precision@{k}: {p}")

def run(use_cifar=False, use_imagenette=False):
    # Set load evaluation dataset.
    print(f"Using cifar: {use_cifar}")
    print(f"Using imagenette: {use_imagenette}")
    if use_cifar: 
      # Should run on Google Colab. Change cifar_dir, index_image_corpus, and test_image_corpus to wherever your data is.
      # Dataset available at: https://drive.google.com/file/d/1Zivf7cXpXAHPoVii0Mp3hecWJJx4ZBY_/view?usp=sharing
      # The used dataset is only the test dataset of https://www.kaggle.com/joaopauloschuler/cifar100-128x128-resized-via-cai-super-resolution.
      cifar_dir = "/content/crier/backend/cifar100-128"                        # Should exist already.
      index_image_corpus = "/content/crier/backend/cifar100-128/index_corpus"  # Will create this dir. 950 images per class to index.
      test_image_corpus = "/content/crier/backend/cifar100-128/test_corpus"    # Will create this dir. 50 images per class to test           
      test_image_names, expected_paths = extractSimilarImagesAnswersCifarOrImagenette(cifar_dir)
    elif use_imagenette:
      # Should run on Google Colab. Change imagenette_dir, index_image_corpus, and test_image_corpus to wherever your data is.
      # Dataset available at: https://github.com/fastai/imagenette
      # The used dataset is only the test dataset of https://github.com/fastai/imagenette
      imagenette_dir = "/content/crier/backend/imagenette2-320"                        # Should exist already.
      index_image_corpus = "/content/crier/backend/imagenette2-320/index_corpus"  # Will create this dir. 950 images per class to index.
      test_image_corpus = "/content/crier/backend/imagenette2-320/test_corpus"    # Will create this dir. 50 images per class to test           
      test_image_names, expected_paths = extractSimilarImagesAnswersCifarOrImagenette(imagenette_dir, 'train', 880)  
    else:
      index_image_corpus = "example_image_corpus"
      test_image_corpus = "example_image_corpus"
      similarity_path = "test_image_corpus/similarity.txt"
      similar_images = extractSimilarImagesAnswers(similarity_path)
      test_image_names = os.listdir(test_image_corpus)
      expected_paths = [similar_images[img_name] for img_name in test_image_names]

    num_results = 25 if use_cifar or use_imagenette else 10
    k_range = range(1, 26) if use_cifar or use_imagenette else range(1, 11)
    output_mapk = "mapk_cifar.png" if use_cifar or use_imagenette else "mapk_custom.png"
    output_mark = "mark_cifar.png" if use_cifar or use_imagenette else "mark_custom.png"

    if use_imagenette:
      output_mapk = "mapk_imagenette.png"
      output_mark = "mark_imagenette.png"
    # Build Retrieval models.
    hist_retriever = histogram.HistogramRetrieval(index_image_corpus, num_results)
    crier_retriever = model.CRIER(token_manager.MODEL_NAME, token_manager.IMAGE_SIZE, num_results)
    crier_retriever.create_engine(index_image_corpus)
    crier_retriever.create_database(index_image_corpus)

    if use_cifar or use_imagenette: expected_paths = get_basenames(expected_paths)

    # Run Hisogram-Retrieval on dataset, retrieve top-k images, and save total time.
    hist_actual_paths = []
    for test_image_name in test_image_names:
        test_image_path = os.path.join(test_image_corpus, test_image_name)
        _, image_paths, distances = hist_retriever.search(test_image_path)
        hist_actual_paths.append(image_paths)
    hist_actual_paths = get_basenames(hist_actual_paths)

    # Run CRIER on dataset, retrieve top-k images, and save total time.
    crier_actual_paths = []
    for test_image_name in test_image_names:
        _, image_paths, distances = crier_retriever.search(index_image_corpus, test_image_name)
        crier_actual_paths.append(image_paths)
    crier_actual_paths = get_basenames(crier_actual_paths)

    # Evaluate Histogram and CRIER retrievers. Need to compare total times taken.
    hist_mapks = []
    hist_marks = []

    crier_mapks = []
    crier_marks = []

    print(f"\nCalculating MAP@k and MAR@k values for HistogramRetrieval and CRIER.")
    for k in k_range:
        hist_mapks.append(calc_mapk(hist_actual_paths, expected_paths, k))
        hist_marks.append(calc_mark(hist_actual_paths, expected_paths, k))
        
        crier_mapks.append(calc_mapk(crier_actual_paths, expected_paths, k))
        crier_marks.append(calc_mark(crier_actual_paths, expected_paths, k))
    print(f"\nMetrics calculated.")

    recmetrics.mapk_plot([hist_mapks, crier_mapks], ['HistogramRetrieval', 'CRIER'], k_range)
    plt.savefig(output_mapk)

    recmetrics.mark_plot([hist_marks, crier_marks], ['HistogramRetrieval', 'CRIER'], k_range)
    plt.savefig(output_mark)

    print(f"Saved MAP@k and MAP@k plots.")

    
# run() # Can run locally without any additional setup(besides installing from requirements.txt)
# run(use_cifar=True)  # Preferable to use Google Colab for higher memory bandwith(suggested is 12gb RAM). Feel free to experiment with
#                      # changing BATCH_SIZE in model_defs.
# run(use_imagenette=True) # Same as use_cifar but for the Imagenette2-320 dataset.