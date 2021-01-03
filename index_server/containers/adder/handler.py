import asyncio
from collections import ChainMap, defaultdict
import concurrent
from queue import SimpleQueue

import numpy as np

from typing import Dict, List, Optional, Tuple

from interactive_index import InteractiveIndex

from knn import utils
from knn.mappers import Mapper
from knn.utils import JSONType

import config


class Index:
    def __init__(self, index_dir: str, worker_id: str):
        self.indexes: SimpleQueue[InteractiveIndex] = SimpleQueue()
        for i in range(config.NPROC):
            index = InteractiveIndex.load(index_dir)
            index.SHARD_INDEX_NAME_TMPL = config.SHARD_INDEX_NAME_TMPL.format(
                worker_id, i
            )
            self.indexes.put(index)

    def add(self, embedding_dict: Dict[int, np.ndarray]) -> int:
        ids = [
            int(id)
            for id, embeddings in embedding_dict.items()
            for _ in range(embeddings.shape[0])
        ]
        index = self.indexes.get()  # get an index no other thread is adding to
        index.add(
            np.concatenate(list(embedding_dict.values())), ids, update_metadata=False
        )
        self.indexes.put(index)
        return len(ids)


class IndexBuildingMapper(Mapper):
    def initialize_container(self):
        self.shard_pattern_for_glob = config.SHARD_INDEX_NAME_TMPL.format(
            self.worker_id, "*"
        ).format("*")

    def register_executor(self):
        return concurrent.futures.ThreadPoolExecutor() if config.NPROC > 1 else None

    async def initialize_job(self, job_args) -> InteractiveIndex:
        index_dicts = job_args["indexes"]

        job_args["indexes_by_reduction"] = defaultdict(dict)
        for index_name, index_dict in index_dicts.items():
            reduction = index_dict["reduction"]
            index_dir = index_dict["index_dir"]

            job_args["indexes_by_reduction"][reduction][index_name] = Index(
                index_dir, self.worker_id
            )

        return job_args

    # input = path to a np.save'd Dict[int, np.ndarray] where each value is N x D
    @utils.log_exception_from_coro_but_return_none
    async def process_element(
        self, input, job_id, job_args, request_id, element_index
    ) -> Dict[str, int]:
        indexes_by_reduction = job_args["indexes_by_reduction"]
        path_tmpl = input

        num_added_dicts = await asyncio.gather(
            *[
                self.build_indexes_for_reduction(
                    reduction, path_tmpl, indexes, request_id
                )
                for reduction, indexes in indexes_by_reduction.items()
            ]
        )
        return dict(ChainMap(*num_added_dicts))  # merge the dicts

    async def build_indexes_for_reduction(
        self,
        reduction: Optional[str],
        path_tmpl: str,
        indexes: Dict[str, Index],
        request_id: str,
    ) -> Dict[str, int]:
        # Step 1: Load saved embeddings into memory
        embedding_dict = await self.apply_in_executor(
            lambda p: np.load(p, allow_pickle=True).item(),
            path_tmpl.format(reduction),
            request_id=request_id,
            profiler_name=f"{reduction}_load_time",
        )  # type: Dict[int, np.ndarray]

        # Step 2: Add to applicable on-disk indexes
        num_added = await asyncio.gather(
            *[
                self.apply_in_executor(
                    index.add,
                    embedding_dict,
                    request_id=request_id,
                    profiler_name=f"{index_name}_add_time",
                )
                for index_name, index in indexes.items()
            ]
        )

        return dict(zip(indexes.keys(), num_added))

    async def postprocess_chunk(
        self,
        inputs,
        outputs,
        job_id,
        job_args,
        request_id,
    ) -> Tuple[str, List[JSONType]]:
        return self.shard_pattern_for_glob, outputs


mapper = IndexBuildingMapper()
server = mapper.server
