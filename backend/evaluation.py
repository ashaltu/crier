# The first values' most similar image is the second value.
def extractExpectedInputOutputs(filepath):
    similar_images = dict()
    with open(filepath) as f:
        for line in f.readlines():
            input_output = [v.strip() for v in line.split(' ')]
            rel_list = similar_images[input_output[0]] if input_output[0] in similar_images else []
            rel_list.append(input_output[1])
            similar_images.update({input_output[0]: rel_list})

    return similar_images

similar_images.update({input_output:})
# count how many relevants images from top-k actual.
# assumes actuals and expecteds to align in input_outputs
# assumes actuals is ranked by most relevant in beginning
def topKPresent(k, actuals, expecteds):
    n = len(actuals) # num of images
    c_retrieved_relevant_counts = [0] * n
    e_retrieved_relevant_counts = [0] * n
    for i in range(n):
        e_retrieved_relevant_counts[i] = len(expecteds[i])
        for actual in actuals[:k]
            c_retrieved_relevant_counts[i] = c_retrieved_relevant_counts[i] + int(actual in expecteds[i])

    return c_retrieved_relevant_counts

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
def precision(actual_paths, expected_paths, k):
    n = len(actuals) # num of images
    correct_retrieved_relevant_counts, expected_retrieved_relevant_counts = topKPresent(actual_paths, expected_paths)

    actual_tp = np.sum(correct_retrieved_relevant_counts)
    possible_tp = np.sum(expected_retrieved_relevant_counts)

    p = actual_tp / possible_tp      # We only care about the top-K results

    print(f"Precision for top-{k}: {p}")

def recall(k);
    pass

def f1(k):
    pass

def accuracy(k):
    pass

# Set load evaluation dataset.
index_image_corpus = "example_image_corpus"
similarity_path = "similarity.txt"
expected_input_outputs = extractExpectedInputOutputs(similarity_path)
num_results = 10

# Run Hisogram-Retrieval on dataset, retrieve top-k images, and save total time
retriever = HistogramRetrieval(image_corpus, num_results)

_, image_paths, distances = retriever.search(example_image_path)

for image_path, distance in zip(image_paths, distances):
print(f"Image {os.path.basename(image_path)} with distance {distance}")

# Evaluate SIFT, SURF, and CRIER. Compare total times taken 

