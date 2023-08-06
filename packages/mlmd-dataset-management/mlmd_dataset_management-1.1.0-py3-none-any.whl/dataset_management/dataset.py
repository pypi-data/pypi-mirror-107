import os
import logging
import json
from mlmd.dataset_manager_scheme import ArtifactType, ExecutionType, ContextType
from mlmd.dataset_manager_dao import *
from dataset_management.utils import generate_version_id
from dataset_management.blob import _upload_blob, get_bucket_name, list_blob, _download_blob
import datetime
from multiprocessing import Array, cpu_count, Pool
from .triggers import ApiTrigger

class Dataset():
    def __init__(self, datasetname, version="latest", username="Anomymous") -> None:        
        dataset = get_artifact_by_type_and_name(ArtifactType.DATASET, datasetname)
        if dataset is None:
            raise Exception("Dataset {} not found".format(datasetname))
        self.metadata = dataset.properties
        self.datasetname = dataset.name
        self.created_at = datetime.datetime.fromtimestamp(dataset.create_time_since_epoch//1000.0)
        self.id = dataset.id
        self.username = username
        self.version = version
        if self.version == "latest":
            self.version = self.metadata["latest_version"].string_value
        self.uncommitted_version = self.metadata["uncommitted_version"].string_value
        self.filelist = self.get_filelist()
        self.trigger = ApiTrigger.from_json_string(self.metadata["trigger"].string_value)

    def __str__(self) -> str:
        return str({
            "name": self.datasetname,
            "version": self.version,
            "trigger": self.metadata["trigger"].string_value,
            "tags": self.metadata["tags"].string_value,
            "created_by": self.metadata["created_by"].string_value,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        })

    def list_staged_actions(self):
        tobe_committed_ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)
        return [{
            "action": get_type_name_from_id(exe.type_id),
            "filelist": exe.properties["filelist"].string_value,
            "executed_by": exe.properties["executed_by"].string_value
        } for exe in get_executions_by_context(tobe_committed_ctx.id)]


    def list_versions(self, short=False):
        if short:
            return [ctx.name for ctx in get_contexts_by_artifact(ContextType.COMMIT_DATASET_VERSION, self.id) if ctx.properties["committed_by"].string_value != ""]            
        return [
            {"version": ctx.name,
             "committed_by": ctx.properties["committed_by"].string_value,
             "prev_version": ctx.properties["prev_ref"].string_value,
             "created_at": datetime.datetime.fromtimestamp(ctx.create_time_since_epoch//1000.0).strftime("%Y-%m-%d %H:%M:%S")
            } for ctx in get_contexts_by_artifact(ContextType.COMMIT_DATASET_VERSION, self.id) if ctx.properties["committed_by"].string_value != ""]

    def add_files_from_dir(self, _dir, override=False):
        if _dir is None or os.path.isdir(_dir) == False:
            raise Exception("Data dir {} not valid".format(_dir))

        blobnamelist = [blob.name for blob in list_blob(get_bucket_name(self.datasetname))]

        filelist = [_file for _file in os.listdir(_dir) if os.path.isfile(os.path.join(_dir, _file)) 
            and (override == True or _file not in blobnamelist)]
        arglist = [(_file, self.datasetname, _dir) for _file in filelist]
        if len(arglist) <= 0:
            print("No file to upload. Override option is being set to {}".format(override))
            return

        print("Uploading {}...".format(filelist))
        proc_count = max(cpu_count(), len(arglist))
        p = Pool(proc_count)
        r = p.map(_upload_blob, arglist)
        p.close()
        p.join()
        success_list = []
        for i,_ in enumerate(r):
            if r[i] == False:
                logging.warning("Failed to update {} in changelist".format(self.changelist[i][0]))
            else:
                success_list.append(r[i])
        print("Successfully uploaded {}".format(success_list))
        exe_id = create_execution(ExecutionType.ADD_FILES_TO_DATASET, json.dumps(success_list), self.username, _dir)
        ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)
        return create_association_attribution(ctx.id, exe_id, None)

    def remove_files(self, filelist):
        if filelist is None or len(filelist) <= 0:
            return None
        exe_id = create_execution(ExecutionType.REMOVE_FILES_FROM_DATASET, json.dumps(filelist), self.username, None)
        ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)
        return create_association_attribution(ctx.id, exe_id, None)

    def commit_version(self, trigger=None, ref_version=None):
        tobe_committed_ctx = get_context(ContextType.COMMIT_DATASET_VERSION, self.uncommitted_version)

        if len(get_executions_by_context(tobe_committed_ctx.id)) <= 0:
            print("Nothing to commit")
            return False

        tobe_committed_ctx.properties["committed_by"].string_value = self.username
        tobe_committed_ctx.properties["prev_ref"].string_value = self.version if ref_version is None else ref_version
        update_context(tobe_committed_ctx)
        committed_version_id = tobe_committed_ctx.name
        # new uncommited version ref to committed version
        new_uncommitted_version_id = generate_version_id()
        context_id = create_context(ContextType.COMMIT_DATASET_VERSION, new_uncommitted_version_id, None, self.version)
        create_association_attribution(context_id, None, self.id)

        self.uncommitted_version = new_uncommitted_version_id
        self.version = committed_version_id
        self.filelist = self.get_filelist()
        update_artifact(ArtifactType.DATASET, self.datasetname, None, committed_version_id, new_uncommitted_version_id)
        if trigger is not None:
            trigger.execute()
        elif self.trigger is not None:
            self.trigger.execute()
        return committed_version_id

    def get_trigger(self):
        return ApiTrigger.from_json_string(self.metadata.get("trigger"))

    def set_trigger(self, trigger: ApiTrigger):
        self.metadata["trigger"].string_value = str(trigger)
        self.trigger = trigger
        return update_artifact(ArtifactType.DATASET, self.datasetname, None, None, None, self.metadata["trigger"].string_value)

    def get_tags(self):
        return self.metadata["tags"].string_value

    def add_tag(self, tag):
        tag_str = self.metadata["tags"].string_value
        if tag_str is None or tag_str == '':
            tag_arr = [tag]
        else:
            tag_arr = tag_str.split(",")
            if tag not in tag_arr:
                tag_arr.append(tag)
            else:
                print("Tag existed")
                return False
        tag_str = ",".join(tag_arr)
        self.metadata["tags"].string_value = tag_str
        return update_artifact(ArtifactType.DATASET, self.datasetname, None, None, None, None, tag_str)

    def set_tags(self, tags: Array):
        tags_str = ",".join(tags)
        self.metadata["tags"].string_value = tags_str
        return update_artifact(ArtifactType.DATASET, self.datasetname, None, None, None, None, tags_str)

    def __collect_changelist(self, version, global_changelist):
        ctx = get_context(ContextType.COMMIT_DATASET_VERSION, version)
        if ctx is None:
            raise Exception("Version {} not exists in this dataset".format(self.version))
        executions = get_executions_by_context(ctx.id)

        for execution in executions: 
            filelist = json.loads(execution.properties["filelist"].string_value)
            for _file in filelist:
                if global_changelist.get(_file) is None:
                    global_changelist[_file] = [execution.type_id]
                else:
                    global_changelist[_file].append(execution.type_id)
                
        prev_version = ctx.properties["prev_ref"].string_value
        if prev_version is not None and prev_version != '':
            return self.__collect_changelist(prev_version, global_changelist)
        return global_changelist

    def get_filelist(self):
        if self.version is None or self.version == "":
            return None
        addtype = get_execution_type_by_name(ExecutionType.ADD_FILES_TO_DATASET)
        filelist = []
        global_changelist = self.__collect_changelist(self.version, {})
        for key,value in global_changelist.items():
            if value[0] == addtype.id:
                filelist.append(key)
        return filelist

    def get_current_version(self):
        return self.version

    def checkout(self, version):
        if version == "latest":
            version = self.metadata["latest_version"].string_value
        if version not in self.list_versions(short=True):
            raise Exception("Version is not valid")
        self.version = version
        self.filelist = self.get_filelist()

    def download_to_dir(self, _dir):
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if self.filelist is None:
            self.filelist = self.get_filelist()        

        print("Downloading {}...".format(self.filelist))
        arglist = [(_f, self.datasetname, _dir) for _f in self.filelist]
        proc_count = max(cpu_count(), len(arglist))
        p = Pool(proc_count)
        r = p.map(_download_blob, arglist)
        p.close()
        p.join()
        success_list = []
        for i,_ in enumerate(r):
            if r[i] == False:
                logging.warning("Failed to update {} in changelist".format(self.changelist[i][0]))
            else:
                success_list.append(r[i])
        print("Successfully downloaded {}".format(success_list))
