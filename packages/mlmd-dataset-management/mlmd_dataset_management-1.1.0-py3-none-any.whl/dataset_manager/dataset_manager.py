from multiprocessing import Array
from dataset_management.blob import get_bucket_name
from mlmd.dataset_manager_dao import create_artifact, create_context, get_artifacts_by_type, create_association_attribution
from mlmd.dataset_manager_scheme import ContextType, ArtifactType
from dataset_management.dataset import Dataset
from dataset_management.utils import generate_version_id
from google.cloud import storage
import datetime

def _is_tag_hit(requested_tags, tags):
    if requested_tags is None or requested_tags == '':
        return True
    if tags is None or tags == '':
        return False
    for tag in requested_tags:
        if tag in tags:
            return True
    return False

def list_datasets(tags:Array=None):
    return [{
        "name": dataset.name,
        "created_at": datetime.datetime.fromtimestamp(dataset.create_time_since_epoch//1000.0).strftime("%Y-%m-%d %H:%M:%S"),
        "created_by": dataset.properties["created_by"].string_value,
        "latest_version": dataset.properties["latest_version"].string_value,
        "tags": dataset.properties["tags"].string_value,
        "trigger": dataset.properties["trigger"].string_value
        } for dataset in get_artifacts_by_type(ArtifactType.DATASET) if _is_tag_hit(tags, dataset.properties["tags"].string_value.split(","))]

def get_dataset(name, version="latest", get_by="Anomymous"):
    ds = Dataset(name, version, get_by)
    return ds

def create_dataset(name, created_by="Anonymous"):
    storage_client = storage.Client()
    bucket = storage_client.bucket(get_bucket_name(name))
    if bucket.exists():
        raise Exception("Bucket {} existed".format(name))
    bucket.storage_class = "STANDARD"
    storage_client.create_bucket(bucket, location="eu")
    uncommitted_version_id = generate_version_id()
    context_id = create_context(ContextType.COMMIT_DATASET_VERSION, uncommitted_version_id, None, None)
    artifact_id = create_artifact(ArtifactType.DATASET, name, created_by, None, uncommitted_version_id)
    create_association_attribution(context_id, None, artifact_id)
    return Dataset(name)

def delete_dataset(name):
    print("Not yet implemeted")
    pass
