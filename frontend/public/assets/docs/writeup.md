## Author
Engineered by Abduselam Shaltu. Fulfillment for the final project of [cse-455](https://courses.cs.washington.edu/courses/cse455/22wi/) taught by Joseph Redmon at the University of Washington.

## Published on March 18, 2022
Source code for the [backend](https://github.com/ashaltu/crier/tree/master/backend) and for the [frontend](https://github.com/ashaltu/crier/tree/master/frontend). Here is a [Jupyter Notebook](https://github.com/ashaltu/crier/blob/master/backend/original_crier.ipynb) to quickly demo CRIER and also made available in [Google Colab](https://colab.research.google.com/github/ashaltu/crier/blob/master/crier.ipynb).

# Abstract
In this project, I develop a reverse image search engine that is easily customizable. I open-source a backend built-in Python that allows indexing of custom image corpora, a separation between corpora, easy search functionality, endpoints with an easy one-command server spin up, token-management so users retrieve images from their own custom corpus, evaluation using mAP@k and mAR@k metrics, comparing against different retrieval implementations(histogram-based image retrieval implementation provided), and Jupyter notebooks to demo and experiment. I also open-source a frontend interface built-in React that easily connects to the aforementioned backend server that allows the following functionality: searching through a provided example image database, indexing a new image corpus, searching through the indexed image corpora, and deleting the indexed image corpora. I compare CRIER with a histogram-based image retrieval model across three datasets. I also discuss the challenges and takeaways of the project. A video summary of CRIER can be found [here](youtube.com).

# Problem and Motivation
For the average consumer, searching consists of typing keywords or in some advanced systems, phrases to retrieve relevant documents, images, tables, and other kinds of data. When it comes to searching for images, the average consumer can search with keywords/phrases on their own phones and computers, and search with keywords/phrases and images on large-scale systems like Google Search and Google Images. For this project, I intend to build an easily customizable system to retrieve relevant images from a custom database by searching with an image. For these individuals, systems like Google Images are unhelpful since they reverse image search through a web-indexed image corpus. Additionally, the barrier of entry can be quite costly and tedious for consumers/industry workers trying to test out the usefulness of custom reverse image engines on cloud services like Google Cloud, Microsoft Azure, and Amazon Web Services. This project proposes CRIER, a Custom Reverse Image Extractions Ranked system. By building this system, the entry point for consumers and industry workers across different sectors can easily build their own reverse image search engine.

# Previous work
For this project, I relied on [extracted feature vectors](https://tfhub.dev/google/imagenet/efficientnet_v2_imagenet1k_s/feature_vector/2) from [EfficientNetV2](https://arxiv.org/abs/2104.00298). EfficientNetV2, released by Google, performs expectionally well for tasks that may require a CNN. It outperforms other SOTA models and trains 5-10x faster on image datasets like CIFAR and ImageNet. Below is a plot comparing it's accuracy against other SOTA models on ImageNet for top-1 accuracy.
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/plots/efficientnetv2_is_a_boss.png" width="60%" alt="Comparison showing EfficientNetV2 outperforming other SOTA on the ImageNet dataset"/>
</div>

I use [ScaNN](https://ai.googleblog.com/2020/07/announcing-scann-efficient-vector.html), also released by Google, as my Approximate Nearest Neighbor search library. ScaNN is a SOTA ANN library through the development of a new technique called "Anisotropic Vector Quantization". Below is a plot demonstrating its high QPS and accuracy in comparison to other popular ANN libraries.
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/plots/scann.png" width="60%" alt="Comparison showing high accuracy and queries per second where the scann library is dominating"/>
</div>

# Approach

The backend and frontend servers are running on a Microsoft Azure VM, with a size of Standard B2s.

## Backend (Python)
The core of my approach is to use EfficientNetV2's feature extractor as an image encoder to create 1280 fixed-size embeddings for each image. Images are resized to 384x384 with Bilinear Interpolation to fit the model. Pixel values are also normalized in the range of [0, 1]. Then, I "index" the images by passing in all the embeddings into a ScaNN search model. When we want to actually reverse image search, we will follow the same steps by encoding the query image and getting a 1280 fixed-size embedding, then searching with the ScaNN index.

There are many variants of EfficientNetV2, I use EfficientNetV2-S due to it having a relatively small number of parameters(~20M) and high accuracy. I set up a ScaNN index with DotProduct as the similarity function.

I created REST APIs to allow easy interactions with CRIER: CreateToken, RemoveImages, AddImages, SearchDatabase, and RetrieveImages. To do this, I used Flask to create and manage my backend server. To allow multiple users to create their own databases, I built a token manager to ensure users retrieve images from their own image database by token authentication. A scheduler is also created to erase any image corpora and ScaNN index models since this is a demo.

## Frontend (React)
The frontend is built in React JS. There isn't anything too special about the frontend besides creating an actual interface for users to interact with CRIER. I use [`react-markdown`](https://github.com/remarkjs/react-markdown) to render this project info page from a markdown file.

## Evaluation
I built a Histogram based image retrieval model to compare against CRIER using OpenCV. A histogram-based embedding is made of two parts: histograms of an image across all RGB channels flattened, and means of RGB values. I do this to increase the number of features for an image embedding for the Histogram image retrieval model.

To calculate mAP@k and mAR@k metric values, I use the `recmetrics` and `ml_metrics` modules.

# Datasets and Data Augmentation
I don't do any finetuning or transfer learning with the EfficientNetV2 model since I use the pre-trained feature extract as an image encoder. In theory, developers wanting to finetune the EfficientNetV2 model on a certain domain of images (like a medical doctor finetuning on chest x-rays to diagnose lung disease) is certainly possible. Although no methods are provided to do finetuning for this project.

For evaluation, I use three datasets: 
- [CIFAR-100-128](https://www.kaggle.com/joaopauloschuler/cifar100-128x128-resized-via-cai-super-resolution): Regulary CIFAR-100 but resized with the CAI Neural API to 128x128 for increased pixel information.
- [Imagenette](https://github.com/fastai/imagenette) sized at 320-320 also for more pixel information.
- [A custom dataset](https://github.com/ashaltu/crier/tree/master/backend/example_image_corpus): contains pictures of cats, sunflowers, trees, and houses developed by myself.

# Demo
Here is the provided example image corpus that users can search through.

<div style="display:flex;justify-content:space-evenly;flex-wrap:wrap;">
    <img style="margin:5px;border-radius:10px;" src="assets/example_image_corpus/catt.jpg" width="21%" alt="Cat"/>
    <img style="margin:5px;border-radius:10px;" src="assets/example_image_corpus/fcat.jpg" width="21%" alt="Friends cat"/>
    <img style="margin:5px;border-radius:10px;" src="assets/example_image_corpus/house.jpg" width="21%" alt="House 1"/>
    <img style="margin:5px;border-radius:10px;" src="assets/example_image_corpus/house2.jpg" width="21%" alt="House 2"/>
    <img style="margin:5px;border-radius:10px;" src="assets/example_image_corpus/sunflower.jpg" width="21%" alt="Sunflower 1"/>
    <img style="margin:5px;border-radius:10px;" src="assets/example_image_corpus/sunflower2.jpg" width="21%" alt="Sunflower 2"/>
    <img style="margin:5px;border-radius:10px;" src="assets/example_image_corpus/dog_sunflower.jpg" width="21%" alt="Sunflower dog"/>
    <img style="margin:5px;" src="assets/example_image_corpus/tree.jpg" width="21%" alt="Tree"/>
</div>

Briefly what it looks to upload an image database. Notice I am are using the example image corpus shown above as my database.
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/demos/uploading_images.png" width="100%" alt="Demo of uploading images"/>
</div>

My first query will be with this white cat (notice how it is not an image from my database).
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/demos/white_cat.png" width="40%" alt="Demo of search results of white"/>
</div>

And results after querying (in this image I query for a sunflower).
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/demos/white_cat_results.png" width="100%" alt="Demo of search results"/>
</div>

Another query this time with a blue house (also not in my database).
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/demos/blue_house.png" width="40%" alt="Demo of search results"/>
</div>

And results from searching for the blue house.
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/demos/blue_house_results.png" width="100%" alt="Demo of search results"/>
</div>

In both search results, it is clear that the model is performing well in returning relevant search results.

# Model Evaluation
I measured mAP@k and mAR@k across my custom dataset, CIFAR-100-128, Imagenette between the CRIER and the Histogram-based image retrieval models. [mAP@k](http://sdsawtelle.github.io/blog/output/mean-average-precision-MAP-for-recommender-systems.html#MAP-for-Recommender-Algorithms), and [mAR@k](http://sdsawtelle.github.io/blog/output/mean-average-precision-MAP-for-recommender-systems.html#MAP-for-Recommender-Algorithms) is the mean Average Precision and mean Average Recall for the top-k retrievals. These metrics are typically used in evaluating the performance of recommendation systems. mAP@k evaluates the relevancy of retrieved items(images in our case) whereas mAR@k evaluates how well the recommender(the CRIER model) is able to recall all the items the user has rated positively in the test set.

To evaluate the datasets, I first split each dataset into an `index` and `test` portion. The splits are percentage-based with ~95% of the dataset going into the `index` corpus and the rest going into the `test` portion. The number of results to be outputted by the ScaNN model for the CIFAR-100-128 and Imagenette datasets are set to 25, whereas the custom dataset is set to 10 since the dataset is so small.

The plots below were created by the `recmetrics` module. In all three instances, it is clear that CRIER outperforms a Histogram based image retrieval model (higher means better).

### Evaluation on CIFAR-100-128
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/plots/mapk_cifar100-128.png" width="45%" alt="Mean Average Precision at K plot showing CRIER outperforming the Histogram based image retrieval on CIFAR 100 128"/>
    <img src="assets/plots/mark_cifar100-128.png" width="45%" alt="Mean Average Recall at K plot showing CRIER outperforming the Histogram based image retrieval on CIFAR 100 128"/>
</div>

### Evaluation on Imagenette
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/plots/mapk_imagenette.png" width="45%" alt="Mean Average Precision at K plot showing CRIER outperforming the Histogram based image retrieval on Imagenette 320"/>
    <img src="assets/plots/mark_imagenette.png" width="45%" alt="Mean Average Recall at K plot showing CRIER outperforming the Histogram based image retrieval on Imagenette 320"/>
</div>

### Evaluation on custom dataset
<div style="display:flex;justify-content:space-evenly;">
    <img src="assets/plots/mapk_custom.png" width="45%" alt="Mean Average Precision at K plot showing CRIER outperforming the Histogram based image retrieval on the custom dataset"/>
    <img src="assets/plots/mark_custom.png" width="45%" alt="Mean Average Recall at K plot showing CRIER outperforming the Histogram based image retrieval on the custom dataset"/>
</div>

# Discussion

## What problems did you encounter?
Honestly, too many that I've lost track. 

## Are there next steps you would take if you kept working on the project?
Find and fix bugs, keep it open-source, and encourage people to find benefits in custom reverse image search. I would also make it more customizable to provide metadata about the image retrieved so the user can do more. Oh, also make this website way more user-friendly and accessible.

## How does your approach differ from others? Was that beneficial?
This is essentially a playground customizable reverse image search engine tool, something that hasn't been done before. CRIER seems like a very beneficial tool in many fields. As a consumer, it would be nice to search through my own phone's images with an image. It would be nice to do that with an album on my phone. As a student, this is a fun tool that a potential entry point to study Computer Science as a major, and specialize in Machine Learning and Computer Vision. After discussing with some of my peers studying medicine, they see it as useful for quickly diagnosing images of injured patient body parts to retrieve past diagnoses of other patients to help determine the best diagnosis. There are also many medical-related image datasets that a student studying medicine could drag into the CRIER frontend interface and use a new image to search and find the most similar image to understand how to make a correct diagnosis. 