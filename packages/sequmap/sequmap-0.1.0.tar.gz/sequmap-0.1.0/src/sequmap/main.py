import numpy as np
import umap
from sklearn.decomposition import PCA
from scipy.spatial.distance import sqeuclidean
from numba import jit

##############
# Encoding
##############

AA_DICT = {
    'A': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 
    'G': 6, 'H': 7, 'I': 8, 'K': 9, 'L': 10, 
    'M': 11, 'N': 12, 'P': 13, 'Q': 14, 'R': 15, 
    'S': 16, 'T': 17, 'V': 18, 'W': 19, 'Y': 20, 
    '*': 21, 'X': 22
}

#Nucleotide...
NT_DICT = {'A': 1, 'C': 2, 'G': 3, 'T': 4}

def string2encoding(seq, lookup_dic, missing_chars = set()):
    #np
    vec = np.empty(shape=(len(seq)),dtype="int64")
    #cython
    #cdef np.array[int, dim=1] vec = np.empty(shape=(len(seq)),dtype="int64")
    for i in range(len(seq)):
        if seq[i] not in lookup_dic:
            missing_chars.add(seq[i])
            vec[i] = 0
        else:
            vec[i] = lookup_dic[seq[i]]
    return vec, missing_chars

##############
# Embedding
##############
def collect_kmers(seq, k):
    return np.array([seq[i:k+i] for i in range(len(seq)-k+1)])

#weights vector length is the number of unique kmers
#each kmer is counted once, contributes to one pos
def kmer_count_with_index(kmer_counts, index, kmer):
    kmer_counts[int(index)] += 1
    
def batched_kmer_count_with_index(kmer_counts, indices, kmer_vec):
    kmer_counts[indices] += 1

#this function gets the index in lexicographic order...
#forget about 1-based indexing in Python... 
def get_kmer_index(kmer, n_chars):
    kmer_ix = 0
    for c in kmer:
        kmer_ix = kmer_ix * n_chars + (c - 1)
    print(kmer_ix)
    return kmer_ix

def get_all_kmer_indices(seqvec, n_chars, k):
    indices = np.zeros(seqvec.shape[0] - k + 1, dtype=int)
    for i in range(k):
        indices += (seqvec[i:len(seqvec)-k+i+1]-1) * n_chars**(k-i-1)
    return indices

def get_non_error_indices(seqvec, k):
    bit_arr = (seqvec == 0)
    final_bit_arr = np.zeros(bit_arr.shape[0] - k + 1, dtype="bool")
    for i in range(k):
        final_bit_arr |= bit_arr[i:len(bit_arr)-k+i+1]
    return ~final_bit_arr

#with a `kmer_contribution()` function... 
def kmer_embed(seq, k, kmer_contribution = None, batched_kmer_contribution = None, lookup_dic = AA_DICT, missing_chars = set()):
    n = len(set(lookup_dic.values()))
    kmer_counts = np.zeros(n**k, dtype="uint16")
    
    seqvec, missing_chars = string2encoding(seq, lookup_dic, missing_chars = missing_chars)
    kmers = collect_kmers(seqvec, k)
    
    indices = get_all_kmer_indices(seqvec, n, k)
    non_error_inds = get_non_error_indices(seqvec, k)
        
    if batched_kmer_contribution is None:
        for i in np.arange(len(kmers))[non_error_inds]:
            kmer, index = kmers[i], indices[i]
            kmer_contribution(kmer_counts, index, kmer)
    else:
        batched_kmer_contribution(kmer_counts, indices[non_error_inds], kmers[non_error_inds])
    
    return kmer_counts, missing_chars

##############
# Projection
##############
@jit(forceobj=True)
def sq_euclidean(x,y):
    return sqeuclidean(x,y)

def sequmap(seqs, ndim,
    k = 5,
    lookup_dic = NT_DICT,
    pca = True,
    pca_maxoutdim = 5,
    n_neighbors = 12, 
    min_dist = 0.7,
    repulsion_strength = 0.1,
    metric = sq_euclidean,
	metric_kwds = None, 
    **kwargs #can also put all umap args together
    ):
    vecs = []
    missing_chars = set() 
    for seq in seqs:
        vec, missing_chars = kmer_embed(seq, k, batched_kmer_contribution=batched_kmer_count_with_index, lookup_dic = lookup_dic, missing_chars = missing_chars);
        vecs.append(vec)
    if len(missing_chars) > 0:
        warn("Ignored the following characters missing from lookup: $(unique(missing_chars)). Check your sequence type!")
    X = np.array(vecs)
    if pca:
        pca_fit = PCA(n_components=pca_maxoutdim)
        PCAembedding = pca_fit.fit_transform(X);
        umap_fit = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=ndim, metric=metric, repulsion_strength=repulsion_strength, **kwargs)
        proj = umap_fit.fit_transform(PCAembedding);
    else:
        umap_fit = umap.UMAP(n_neighbors=n_neighbors, min_dist=min_dist, n_components=ndim, metric=metric, repulsion_strength=repulsion_strength, **kwargs)
        proj = umap_fit.fit_transform(X);
    return proj

def seqpca(seqs, ndim,
    k = 5,
    lookup_dic = NT_DICT
    ):
    vecs = []
    missing_chars = set() 
    for seq in seqs:
        vec, missing_chars = kmer_embed(seq, k, batched_kmer_contribution=batched_kmer_count_with_index, lookup_dic = lookup_dic, missing_chars = missing_chars);
        vecs.append(vec)
    if len(missing_chars) > 0:
        warn("Ignored the following characters missing from lookup: $(unique(missing_chars)). Check your sequence type!")
    X = np.array(vecs)
    pca_fit = PCA(n_components=ndim)
    return pca_fit.fit_transform(X);
