from visualize import *
from vectorize import *

def load_topic_modeling(saved_model):
    # Import Libraries
    import pandas as pd
    import numpy as np
    import pyLDAvis
    import pyLDAvis.gensim as genldavis

    import sklearn.cluster.k_means_
    from sklearn.preprocessing import normalize
    from sklearn.feature_extraction.text import CountVectorizer

    # Load Data & Preprocessing
    documents = saved_model['documents']
    processed_docs = saved_model['processed_docs']
    processed_docs = processed_docs.apply(lambda x: x[1:-1].replace("'", "").split(', '))

    vect = CountVectorizer()
    tsne_data = get_countvector(processed_docs)

    # LDA
    lda_result = saved_model['lda_result']
    if len(lda_result) == 3:
        # lda_result = {'topic_model': gensim.models.ldamodel.LdaModel, 
        #               'corpus': list, 
        #               'dictionary': gensim.corpora.dictionary.Dictionary
        # }
        lda_vis_data = genldavis.prepare(**lda_result)
        lda_labels = []
        for i in range(len(documents)):
            lda_labels.append(np.argmax([p for t, p in lda_result['topic_model'][lda_result['corpus'][i]]]))
    elif len(lda_result) == 5:
        # lda_result = {'document_topic_counts': list,
        #               'topic_word_counts': list,
        #               'topic_counts': list,
        #               'document_lengths': list,
        #               'distinct_words': set
        # }
        document_topic_counts = lda_result['document_topic_counts']
        topic_word_counts = lda_result['topic_word_counts']
        topic_counts = lda_result['topic_counts']
        document_lengths = lda_result['document_lengths']
        distinct_words = lda_result['distinct_words']
        n_clusters = len(topic_counts)

        topic_term_dists = np.array([topic_word_counts[i][k] for i in range(n_clusters) for k in list(distinct_words)]).reshape((n_clusters, len(distinct_words)))
        doc_topic_dists = pd.DataFrame([d.values() for d in document_topic_counts]).fillna(0).values
        doc_lengths = np.array(document_lengths)
        vocab = list(distinct_words)
        term_frequency = np.array([topic_word_counts[i][k] for i in range(n_clusters) for k in list(distinct_words)]).reshape((n_clusters, len(distinct_words))).sum(axis=0)

        lda_data = {
            'topic_term_dists':topic_term_dists,
            'doc_topic_dists':doc_topic_dists,
            'doc_lengths':doc_lengths,
            'vocab':vocab,
            'term_frequency':term_frequency
        }

        lda_vis_data = pyLDAvis.prepare(**lda_data)
        lda_labels = []
        for i in range(len(documents)):
            lda_labels.append(np.argmax(doc_topic_dists[i]))

    # K-Means
    kmeans_result = saved_model['kmeans_result']
    if type(kmeans_result) == sklearn.cluster.k_means_.KMeans:
        kmeans_centers = kmeans_result.cluster_centers_
        kmeans_labels = kmeans_result.labels_
    else:
        kmeans_centers = kmeans_result['cluster_centers']
        kmeans_labels = kmeans_result['labels']

    km_vis_data = get_vis_data(normalize(tsne_data, norm='l2'), processed_docs, kmeans_centers, kmeans_labels)


    # DEC
    dec_labels = saved_model['dec_result']

    x_data = pd.DataFrame(tsne_data)
    x_data['y'] = dec_labels
    dec_vis_data = get_vis_data(tsne_data, processed_docs, x_data.groupby('y').mean().reset_index().values[:, 1:], dec_labels)

    ## Visualization
    umap_data = run_umap(tsne_data)

    ## Visualization
    return get_visualization_json(len(np.unique(lda_labels)), documents, umap_data, lda_vis_data, lda_labels, km_vis_data, kmeans_labels, dec_vis_data, dec_labels)
