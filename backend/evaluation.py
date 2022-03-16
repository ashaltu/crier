import os
import numpy as np

# Local
import histogram
import model
import token_manager

# Local only

# from tensorflow.python.compiler.mlcompute import mlcompute
# tf.compat.v1.disable_eager_execution()
# mlcompute.set_mlc_device(device_name='gpu')
# print("is_apple_mlc_enabled %s" % mlcompute.is_apple_mlc_enabled())
# print("is_tf_compiled_with_apple_mlc %s" % mlcompute.is_tf_compiled_with_apple_mlc())
# print(f"eagerly? {tf.executing_eagerly()}")
# print(tf.config.list_logical_devices())

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

    print(f"Precision for top-{k}: {p}")

def recall(actual_paths, expected_paths, k):
    correct_retrieved_relevant_counts, expected_retrieved_relevant_counts = topKPresent(k, actual_paths, expected_paths)

    actual_tp = np.sum(correct_retrieved_relevant_counts)
    possible_tp = np.sum(expected_retrieved_relevant_counts)

    print(f"actual_tp: {actual_tp}")
    print(f"possible_tp: {possible_tp}")
    p = actual_tp / possible_tp      # We only care about the top-K results. FIX MAYBE?

    print(f"Precision@{k}: {p}")


def f1(k):
    pass

def accuracy(k):
    pass

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
    hist_actual_paths.append([os.path.basename(image_path) for image_path in image_paths])

# Run Hisogram-Retrieval on dataset, retrieve top-k images, and save total time.
crier_actual_paths = []
for test_image_name in test_image_names:
    _, image_paths, distances = crier_retriever.search(test_image_corpus, test_image_name)
    crier_actual_paths.append([os.path.basename(image_path) for image_path in image_paths])

# Evaluate SIFT, SURF, and CRIER. Compare total times taken 
print(f"\nCalculating precision values for HistogramRetrieval")
precision(hist_actual_paths, expected_paths, 1, test_image_names) # Should be 1.0
precision(hist_actual_paths, expected_paths, 2, test_image_names)
precision(hist_actual_paths, expected_paths, 3, test_image_names)
precision(hist_actual_paths, expected_paths, 5, test_image_names)
precision(hist_actual_paths, expected_paths, 10, test_image_names)

print(f"\nCalculating precision values for CRIER")
precision(crier_actual_paths, expected_paths, 1, test_image_names) # Should be 1.0
precision(crier_actual_paths, expected_paths, 2, test_image_names)
precision(crier_actual_paths, expected_paths, 3, test_image_names)
precision(crier_actual_paths, expected_paths, 5, test_image_names)
precision(crier_actual_paths, expected_paths, 10, test_image_names)
