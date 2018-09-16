import spec2model.config_manager as yml_manager

config_file_path = 'spec2model/configuration.yml'

class FolderDigger:

    yml_config = ''

    def __init__(self):
        self.specs_list = {}
        self.yml_config = yml_manager.YamlIO()

    def set_spec_file_id(self, file_id):
        self.specs_id = file_id
       
    def __get_bsc_specs(self, spec_config, input_folder):
        specs_list = {}
        for current_config in spec_config:

            # If name not defined, will skip because None
            spec_name = current_config.get('name')

            # The names of the folders and files are predictable
            spec_folder = os.path.join(input_folder, spec_name)

            # Only alert user if missing, other prints are distracting
            if os.path.exists(spec_folder):
                spec_mapping_file = os.path.join(spec_folder, '%s_Mapping.xlsx' % spec_name)
                if os.path.exists(spec_mapping_file):
                    specs_list[spec_name] = current_config
                else:
                    print("Missing %s mapping file." % spec_name)
            else:
                # Check if folder is draft
                spec_folder_draft = os.path.join(input_folder, '_' + spec_name)
                if os.path.exists(spec_folder_draft):
                    print("Skipping draft folder %s (%s)" % (spec_name, spec_folder_draft))
                else:
                    print("Missing specification folder %s (%s)" % (spec_name, spec_folder))
  
        return specs_list

    def get_specification_list(self, input_folder):
        print("Reading Configuration file.")
        self.yml_config.set_yml_path(config_file_path)
        spec_config = self.yml_config.get_spec_yml_config()
        all_bsc_specs = self.__get_bsc_specs(spec_config, input_folder)
        print("%s mapping files obtained." % len(all_bsc_specs))
        return all_bsc_specs
