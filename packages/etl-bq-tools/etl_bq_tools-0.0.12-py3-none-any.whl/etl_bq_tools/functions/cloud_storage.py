from etl_bq_tools.utils import constants as cons
from etl_bq_tools.utils.memory import get_reduce_memory


def gs_bucket_list_patterns(project_id, bucket_name,
                            prefix_start=None, prefix_end=None,
                            logging=None, key_path=None):
    """
    :param project_id: String
    :param bucket_name: String
    :param prefix_start: String
    :param prefix_end: String
    :param logging: Object
    :param key_path: file.json
    :return: list_blobs
    """
    from color_tools import cprint
    from google.cloud import storage

    if not project_id:
        raise Exception('require var project_id:{project_id} ')
    if not bucket_name:
        raise Exception('require var bucket_name:{bucket_name} ')

    client = storage.Client(project=project_id)
    if project_id and key_path:
        client = storage.Client.from_service_account_json(key_path)

    try:
        bucket = client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()

        filenames = list()
        if prefix_start:
            filenames = list(sorted([str(blob.name) for blob in blobs
                                     if str(blob.name).startswith(prefix_start)]))

        elif prefix_end:
            filenames = list(sorted([str(blob.name) for blob in blobs
                                     if str(blob.name).endswith(prefix_end)]))

        elif prefix_start and prefix_start:
            filenames = list(sorted([str(blob.name) for blob in blobs
                                     if str(blob.name).startswith(prefix_start) and
                                     str(blob.name).endswith(prefix_end)]))

        elif not prefix_start and not prefix_start:
            filenames = list(sorted([str(blob.name) for blob in blobs]))

        if logging:
            logging.info(cons.txt_gs_bucket_list_patterns_success.format(bucket_name))
        else:
            cprint(cons.txt_gs_bucket_list_patterns_success.format(bucket_name))
        return filenames
    except Exception as e:
        if logging:
            logging.info(cons.txt_gs_bucket_list_patterns_errors.format(bucket_name))
        else:
            cprint(cons.txt_gs_bucket_list_patterns_errors.format(bucket_name))


def gs_bucket_list_to_df(project_id, bucket_name,
                         filename=None, filename_col=None,
                         logging=None, key_path=None):
    import pandas as pd
    import gc
    from color_tools import cprint
    import gcsfs

    if not project_id:
        raise Exception('require var project_id:{project_id} ')
    if not bucket_name:
        raise Exception('require var bucket_name:{bucket_name} ')
    if not filename:
        raise Exception('require var filename:{filename} ')
    if not filename_col:
        raise Exception('require var filename_col:{filename_col} ')
    if not key_path:
        raise Exception('require var key_path:{key_path} ')

    try:
        fs = gcsfs.GCSFileSystem(project=project_id,
                                 token=key_path)

        with fs.open(f"gs://{bucket_name}/{filename}") as f:
            frame = pd.read_csv(f)
            frame[f'{filename_col}'] = filename
            df_columns = frame.columns
            frame[df_columns] = frame[df_columns].astype(str)
            df2 = get_reduce_memory(frame, False)
            f.close()
        del frame
        gc.collect()

        if logging:
            logging.info(cons.txt_gs_bucket_list_to_df_success.format(bucket_name, filename))
        else:
            cprint(cons.txt_gs_bucket_list_to_df_success.format(bucket_name, filename))

        return df2
    except Exception as e:
        if logging:
            logging.info(cons.txt_gs_bucket_list_to_df_errors.format(bucket_name))
        else:
            cprint(cons.txt_gs_bucket_list_to_df_errors.format(bucket_name))
