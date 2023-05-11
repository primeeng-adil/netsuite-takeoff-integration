from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext


class DirHandler:

    def __init__(self, root_url, creds):
        self.client = ClientContext(root_url).with_credentials(UserCredential(*creds))

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def __del__(self):
        pass

    @staticmethod
    def get_proj_dir_name(proj_num, proj_title, proj_loc):
        """
        Return the directory name of the project.

        :param proj_num: project ID of the current project
        :param proj_title: project name of the current project
        :param proj_loc: project location of the current project
        :return: appended string with '_' separators
        """
        return (proj_num + '_' + proj_title + '_' + proj_loc).strip()

    def make_proj_dir(self, rel_url):
        """
        Create the project directory in SharePoint.

        :param rel_url: relative url where the directory is to be created
        :return: absolute url of the created directory
        """
        target_folder = self.client.web.ensure_folder_path(rel_url).execute_query()
        return target_folder.serverRelativeUrl

    def make_proj_subdir(self, dir_names, rel_root_url):
        """
        Create subdirectories in the project directory.

        :param dir_names: names of the subdirectories to be created
        :param rel_root_url: relative url of the root folder
        """
        for dir_name in dir_names:
            rel_path = rel_root_url + f'/{dir_name}'
            self.client.web.ensure_folder_path(rel_path).execute_query()

    def copy_file(self, rel_src_url, rel_dest_url):
        """
        Copy a file from one location to another in SharePoint.

        :param rel_src_url: relative source url of the source file
        :param rel_dest_url: relative destination url of the copied file
        """
        file = self.client.web.get_file_by_url(rel_src_url)
        file.copyto(rel_dest_url, False).execute_query()

    def rename_file(self, new_name, rel_server_url):
        """
        Rename a file in SharePoint.

        :param new_name: new name for a file in SharePoint
        :param rel_server_url: relative url of the current sharepoint server
        """
        file = self.client.web.get_file_by_server_relative_url(rel_server_url)
        file.rename(new_name).execute_query()
