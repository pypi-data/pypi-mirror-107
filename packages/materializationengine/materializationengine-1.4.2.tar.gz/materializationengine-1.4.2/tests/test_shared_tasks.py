import datetime
import logging
from materializationengine.models import AnalysisVersion
from materializationengine.shared_tasks import (chunk_annotation_ids,
                                                chunk_ids, collect_data, fin,
                                                get_materialization_info,
                                                query_id_range,
                                                add_index,
                                                update_metadata)
from materializationengine.index_manager import IndexCache
from emannotationschemas.models import make_annotation_model

index_client = IndexCache()

def test_chunk_annotation_ids(mat_metadata):
    anno_id_chunks = chunk_annotation_ids(mat_metadata)
    assert anno_id_chunks == [[1, 3], [3, None]]


def test_fin():
    result = fin.s().apply()
    assert result.get() == True


def test_get_materialization_info():
    datastack_info = {
        'datastack': 'test_datastack',
        'aligned_volume': {
            'name': 'test_aligned_volume'
        },
        'segmentation_source': 'graphene://https://fake-daf.com/segmentation/table/test_pcg'}
    analysis_version = 1
    materialization_time_stamp = datetime.datetime.utcnow()
    mat_info = get_materialization_info(
        datastack_info, analysis_version, materialization_time_stamp)
    assert mat_info == [
        {'datastack': 'test_datastack',
         'aligned_volume': 'test_aligned_volume',
         'schema': 'synapse',
         'create_segmentation_table': False,
         'max_id': 4,
         'min_id': 1,
         'row_count': 4,
         'add_indices': True,
         'segmentation_table_name': 'test_synapse_table__test_pcg',
         'annotation_table_name': 'test_synapse_table',
         'temp_mat_table_name': 'temp__test_synapse_table',
         'pcg_table_name': 'test_pcg',
         'segmentation_source': 'graphene://https://fake-daf.com/segmentation/table/test_pcg',
         'coord_resolution': [4, 4, 40],
         'materialization_time_stamp': str(materialization_time_stamp),
         'last_updated_time_stamp': None,
         'chunk_size': 100000,
         'table_count': 1,
         'find_all_expired_roots': False,
         'analysis_version': 1,
         'analysis_database': 'test_datastack__mat1'}]


def test_collect_data():
    task = collect_data.s('test', {'some': 'dict'}).apply()
    assert task.get() == (('test', {'some': 'dict'}), {})


def test_query_id_range():
    id_range = query_id_range(AnalysisVersion.id, 1, 3)
    assert str(
        id_range) == "analysisversion.id >= :id_1 AND analysisversion.id < :id_2"


def test_chunk_ids(mat_metadata):
    ids = chunk_ids(mat_metadata, AnalysisVersion.id, 2)
    assert [id for id in ids] == [[1, None]]


def test_update_metadata(mat_metadata):
    is_updated = update_metadata.s(mat_metadata).apply()
    mat_ts = mat_metadata['materialization_time_stamp']
    assert is_updated.get() == {
        "Table: test_synapse_table__test_pcg": f"Time stamp {mat_ts}"}


def test_add_index(mat_metadata, db_client):
    database_name = mat_metadata['aligned_volume']
    table_name = mat_metadata['annotation_table_name']
    schema = mat_metadata['schema_type']

    __, engine= db_client

    is_dropped = index_client.drop_table_indices(table_name, engine)
    assert is_dropped == True
    
    model = make_annotation_model(table_name, schema, with_crud_columns=False)

    indexs = index_client.add_indices_sql_commands(table_name, model, engine)
    for index in indexs:
        index = add_index.s(database_name, index).apply()
        assert "Index" or "Alter" in index.get() 
    