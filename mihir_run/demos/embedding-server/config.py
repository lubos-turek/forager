GCP_PROJECT = "visualdb-1046"
GCP_ZONE = "us-central1-a"
GCP_MACHINE_TYPE = "n2-highcpu-4"

OUTPUT_FILENAME = "lvis-embeddings.npy"
MAPPER_CONTAINER = "gcr.io/visualdb-1046/mihir-full-image-embedding-spatial"

N_RETRIES = 1
CHUNK_SIZE = 1

EMBEDDING_LAYER = "res5"
EMBEDDING_DIM = 2048

QUERY_PATCHES_PER_IMAGE = 10
QUERY_NUM_RESULTS_MULTIPLE = 50

INDEX_NUM_CENTROIDS = 128
INDEX_SUBINDEX_SIZE = 25000
INDEX_NUM_QUERY_PROBES = 16
INDEX_USE_GPU = False
INDEX_TRAIN_MULTIPLE = 39

INDEX_TRANSFORM = None
INDEX_TRANSFORM_ARGS = None
INDEX_ENCODING = "SQ"
INDEX_ENCODING_ARGS = [8]

INDEX_FLUSH_SLEEP = 5  # seconds

CLEANUP_TIMEOUT = 30 * 60  # seconds
CLEANUP_INTERVAL = CLEANUP_TIMEOUT // 4
