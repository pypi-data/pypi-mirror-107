from unittest.mock import MagicMock
import sys
sys.modules['materializationengine.chunkedgraph_gateway'] = MagicMock()
from materializationengine.workflows.update_root_ids import get_expired_root_ids, get_new_roots, get_supervoxel_ids
import logging


mocked_expired_root_id_data = [
    [20000000, 20000001],
    [20000002, 20000003],
    [20000004, 20000005],
    [20000006, 20000007],
    [20000008, 20000009],
]

mocked_supervoxel_chunks = [{'post_pt_supervoxel_id': 10000000,
                             'pre_pt_supervoxel_id': 10000000,
                             'id': 1,
                             'post_pt_root_id': 20000000,
                             'pre_pt_root_id': 20000000},
                            {'post_pt_supervoxel_id': 10000000,
                             'pre_pt_supervoxel_id': 10000000,
                             'id': 2,
                             'post_pt_root_id': 20000000,
                             'pre_pt_root_id': 20000000},
                            {'post_pt_supervoxel_id': 10000000,
                             'pre_pt_supervoxel_id': 10000000,
                             'id': 3,
                             'post_pt_root_id': 20000000,
                             'pre_pt_root_id': 20000000}]

def test_get_expired_root_ids(monkeypatch, mat_metadata):
    def mock_lookup_expire_root_ids(*args, **kwargs):
        return list(range(20000000, 20000010))
    monkeypatch.setattr(
        "materializationengine.workflows.update_root_ids.lookup_expired_root_ids", mock_lookup_expire_root_ids)
    expired_root_ids = get_expired_root_ids(mat_metadata, 2)
    index = 0
    for root_id in expired_root_ids:
        logging.info(root_id)
        assert root_id == mocked_expired_root_id_data[index]
        index += 1


def test_get_supervoxel_ids(annotation_data, mat_metadata):
    expired_roots = annotation_data['expired_root_ids']

    supervoxel_ids = get_supervoxel_ids(expired_roots, mat_metadata)
    assert supervoxel_ids == {
        'post_pt_root_id': [
            {'id': 2,
             'post_pt_root_id': 40000000000000000,
             'post_pt_supervoxel_id': 40000000}],
        'pre_pt_root_id': [
            {'id': 1,
             'pre_pt_root_id': 10000000000000000,
             'pre_pt_supervoxel_id': 10000000},
            {'id': 3,
             'pre_pt_root_id': 50000000000000000,
             'pre_pt_supervoxel_id': 50000000},
            {'id': 4,
             'pre_pt_root_id': 10000000000000000,
             'pre_pt_supervoxel_id': 10000000}]}


def test_get_new_roots(monkeypatch, mat_metadata, annotation_data):
    
    def mock_lookup_new_root_ids(*args, **kwargs):
        return annotation_data['new_root_ids']
    
    monkeypatch.setattr(
        "materializationengine.workflows.update_root_ids.lookup_new_root_ids", mock_lookup_new_root_ids)
    
    supervoxel_chunk = annotation_data["segmentation_data"]
    new_roots = get_new_roots.s(supervoxel_chunk, mat_metadata).apply()
    assert new_roots.get() == 'Number of rows updated: 3'


