from notebookutils import mssparkutils


class Util:

    def __init__(self):
        pass

    def list_folder_delta_lake(self, dir):
        return mssparkutils.fs.ls(dir)

    def delete_file_delta_lake(self, path):
        mssparkutils.fs.rm(path, True)
