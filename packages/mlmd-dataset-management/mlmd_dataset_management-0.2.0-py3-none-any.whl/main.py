# from azure.storage.blob import __version__
# print("Azure Blob Storage v" + __version__)

# import os
# os.environ['AZURE_STORAGE_CONNECTION_STRING']="DefaultEndpointsProtocol=https;AccountName=mlops0115993429;AccountKey=UveujjrZ+nWQAOj25dFIvOP+UCQ4p4wJWRWUuAXTzk+pyNata5x5simtLLnNhakozMl+pYRiG2cjI7xg70qkFg==;EndpointSuffix=core.windows.net"
# os.environ['AZURE_STORAGE_ACCESS_KEY']= "UveujjrZ+nWQAOj25dFIvOP+UCQ4p4wJWRWUuAXTzk+pyNata5x5simtLLnNhakozMl+pYRiG2cjI7xg70qkFg=="

import dataset_manager as dm

# print(dm.list_datasets(tag="trainset"))

# dm.create_dataset("dataset1")
ds1 = dm.get_dataset("dataset1")
print(ds1)
#tagging
# print(ds1.get_tags())
# ds1.add_tag("selectnet")
# print(ds1.get_tags())
# ds1.add_tag("trainset")
# print(ds1.get_tags())

#get versions
# print(ds1.list_versions())
# print(ds1.get_current_version())
# print(ds1.filelist)

# checkout old version
# ds1.checkout("_33734cc89e7e494885d49dffa9120f2b")
# print(ds1.filelist)


# add file to dataset
# from triggers import ApiTrigger
# ds1.add_files_from_dir("dataset1")
# version = ds1.push(ApiTrigger("POST", "http://localhost/retrain", {"dataset":ds1.datasetname, "version": ds1.version}))

# for file in glob.glob("dataset1/*.jpeg"):
#     with open(file, "rb") as data:
#         filename = file.split("/").pop()
#         container.upload_blob(name=filename, data=data, timeout=-1)

# get file list in the dataset
# for f in container.list_blobs():
#     print(f)

# set metadata for a dataset
# container.set_container_metadata({'type':'dataset'})
# print(container.container_name)

# list all datasets
# containers = blob_service_client.list_containers(include_metadata=True)
# for c in containers:
#     print(c)