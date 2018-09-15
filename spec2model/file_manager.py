from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import spec2model.config_manager as yml_manager

config_file_path = 'spec2model/configuration.yml'

class FolderDigger:

    gauth = "This variable will have the Google Authorization file"
    specs_id = '0Bw_p-HKWUjHoNThZOWNKbGhOODg'
    drive = "This variable will be the Google drive's object"
    yml_config = ''

    def __init__(self):
        creds_path="spec2model/mycreds.txt"
        self.gauth = GoogleAuth()
        # Try to load saved client credentials
        self.gauth.LoadCredentialsFile(creds_path)
        if self.gauth.credentials is None:
            # Authenticate if they're not there
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialize the saved creds
            self.gauth.Authorize()
            # Save the current credentials to a file
            self.gauth.SaveCredentialsFile(creds_path)
        # Save the current credentials to a file
        self.gauth.SaveCredentialsFile(creds_path)

        self.drive = GoogleDrive(self.gauth)
        #This is the id of the folder Specification
        self.specs_id = '0Bw_p-HKWUjHoNThZOWNKbGhOODg'
        self.specs_list = {}
        self.yml_config = yml_manager.YamlIO()

    def set_spec_file_id(self, file_id):
        self.specs_id=file_id

    def __get_spec_folder_files(self):
        file_list = self.drive.ListFile({'q':"'"+self.specs_id+"' in parents and trashed =false"}).GetList()
        return file_list

    def __get_spec_folder_files_by_id(self, folder_id):
        file_list = self.drive.ListFile({'q':"'"+folder_id+"' in parents and trashed =false"}).GetList()
        return file_list

    def __get_gfolder_id(self, current_cfg_yml, spec_folder_files):
        current_spec_g_folder = current_cfg_yml['g_folder']
        for folder_file in spec_folder_files:
            if folder_file['title']==current_spec_g_folder:
                return folder_file['id']
        return ''

    def __get_gfile_dic(self, current_cfg_yml, folder_id):
        folder_files=self.__get_spec_folder_files_by_id(folder_id)
        current_spec_g_file = current_cfg_yml['g_mapping_file']
        for folder_file in folder_files:
            if folder_file['title']==current_spec_g_file:
                return folder_file
        return {}

    def __get_bsc_specs(self, spec_config, spec_folder_files):
        specs_list = {}
        for current_config in spec_config:
            print("Searching %s mapping file." % current_config['name'])
            spec_folder_id = self.__get_gfolder_id(current_config, spec_folder_files)
            spec_file_dic = self.__get_gfile_dic(current_config, spec_folder_id)
            try:
                current_config['spec_mapping_url'] = spec_file_dic['alternateLink']
                specs_list[spec_file_dic['id']] = current_config
            except KeyError as e:
                print("Issue loading %s folder, skipping." % current_config['name'])
        return specs_list

    def get_specification_list(self):
        print("Reading Configuration file.")
        self.yml_config.set_yml_path(config_file_path)
        spec_config = self.yml_config.get_spec_yml_config()
        spec_folder_files = self.__get_spec_folder_files()
        all_bsc_specs=self.__get_bsc_specs(spec_config, spec_folder_files)
        print("All mapping files obtained.")
        return all_bsc_specs
