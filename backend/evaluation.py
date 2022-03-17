import os
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

# Set load evaluation dataset.
index_image_corpus = "example_image_corpus"
test_image_corpus = "example_image_corpus"
similarity_path = "test_image_corpus/similarity.txt"
similar_images = extractSimilarImagesAnswers(similarity_path)
num_results = 10

test_image_names = os.listdir(test_image_corpus)
expected_paths = [similar_images[img_name] for img_name in test_image_names]

# Build Retrieval models.
hist_retriever = histogram.HistogramRetrieval(index_image_corpus, num_results)
crier_retriever = model.CRIER(token_manager.MODEL_NAME, token_manager.IMAGE_SIZE, num_results)
crier_retriever.create_engine(index_image_corpus)
crier_retriever.create_database(index_image_corpus)

# Run Hisogram-Retrieval on dataset, retrieve top-k images, and save total time.
hist_actual_paths = []
for test_image_name in test_image_names:
    test_image_path = os.path.join(test_image_corpus, test_image_name)
    _, image_paths, distances = hist_retriever.search(test_image_path)
    hist_actual_paths.append(image_paths)
hist_actual_paths = get_basenames(hist_actual_paths)

# Run Hisogram-Retrieval on dataset, retrieve top-k images, and save total time.
crier_actual_paths = []
for test_image_name in test_image_names:
    _, image_paths, distances = crier_retriever.search(test_image_corpus, test_image_name)
    crier_actual_paths.append(image_paths)
crier_actual_paths = get_basenames(crier_actual_paths)

def calc_mapk(actual, expected, k):
    mapk = metrics.mapk(slice_columns(actual, k), slice_columns(expected, k))
    return mapk

def calc_mark(actual, expected, k):
    mark = recmetrics.mark(slice_columns(actual, k), slice_columns(expected, k))
    return mark

# Evaluate Histogram and CRIER retrievers. Need to compare total times taken.
hist_mapks = []
hist_marks = []

crier_mapks = []
crier_marks = []

k_range = range(1, 11)
print(f"\nCalculating MAP@k and MAR@k values for HistogramRetrieval and CRIER.")
for k in k_range:
    hist_mapks.append(calc_mapk(hist_actual_paths, expected_paths, k))
    hist_marks.append(calc_mark(hist_actual_paths, expected_paths, k))
    
    crier_mapks.append(calc_mapk(crier_actual_paths, expected_paths, k))
    crier_marks.append(calc_mark(crier_actual_paths, expected_paths, k))
print(f"\nMetrics calculated.")

recmetrics.mapk_plot([hist_mapks, crier_mapks], ['HistogramRetrieval', 'CRIER'], k_range)
plt.savefig('mapks.png')

recmetrics.mark_plot([hist_marks, crier_marks], ['HistogramRetrieval', 'CRIER'], k_range)
plt.savefig('marks.png')

print(f"Saved MAP@k and MAP@k plots.")