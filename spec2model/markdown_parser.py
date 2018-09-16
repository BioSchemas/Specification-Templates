import spec2model.file_manager as f_manager
import spec2model.mapping as mapper
import spec2model.workbook_validator as validator
from openpyxl import load_workbook
import frontmatter
import os
import sys
from io import BytesIO

class FrontMatterParser:
    md_files_path = ''
    bsc_parser = ''
    bsc_spec_list = ''

    def __init__(self, input_folder='specifictions'):
        self.__check_input_folder(input_folder)
        self.md_files_path = 'docs/spec_files/'
        self.bsc_file_manager = f_manager.FolderDigger()
        self.bsc_parser = mapper.WorkbookParser()
        self.validator = validator.WorkbookValidator

    def __check_input_folder(self, input_folder):
        '''check for the existence of the input folder, and ensure full path
           
           Parameters
           ==========
           input_folder: path (relative or full) to input folder with specification
           subdirectories.
        '''
        self.input_folder = os.path.abspath(input_folder)
        if not os.path.exists(input_folder):
            print('Cannot find %s' % input_folder)
            sys.exit(1)
        print('Found %s' % input_folder)

    def __get_all_specs_dict(self):
        '''return listing of specs, meaning loaded workbooks. We don't validate
           the workbooks here. It's expected that self.bsc_spec_list is a dictionary
           of specs, with keys as folder names and values as parameters, one of which
           is the 'mapping_file'
        '''
        all_specs = dict()

        for bsc_spec, bsc_params in self.bsc_spec_list.items():

            # Save metadata with workbook parser, in case we need it
            self.bsc_parser.set_spec_metadata(bsc_params)

            # Generate the mapping from the workbook
            mapping_file = bsc_params['mapping_file']
            all_specs[bsc_spec] = self.bsc_parser.get_mapping(mapping_file)

        return all_specs

    def __get_specification_post(self, spec_dict):
        '''for a spec_workbook, which is a dictionary with "name" "workbook" and "params"
           derive the post material, an html file that is mostly yaml metadata
 
           Parameters
           ==========
           spec_dict: a dictionary with:
               name: the name of the folder (and Specification)
               workbook: the loaded workbook (or file to it)
               params: the original values in the configuration.yml for the folder
        '''
        spec_metadata = {}
        spec_post = frontmatter.Post('')

        # Skip over set of pre-defined fields
        # TODO: in future this should link to xlsx in Github repository
        skip_fields = ['mapping_file']

        for spec_field in spec_dict['params']:
            if spec_field not in skip_fields:
                spec_metadata[spec_field] = spec_dict['params'][spec_field]

        spec_post.metadata = spec_metadata
        return spec_post

    def __create_spec_folder_struct(self, spec_name):
        '''create a spec folder and subdirectory for examples for a 'spec_name'
           only if it doesn't exist.

           Parameters
           ==========
           spec_name: the name of the specification
        '''
        # Individual specification folder under "docs/spec_files"
        spec_dir = os.path.join(self.md_files_path, spec_name)

        # Create if doesn't exist
        if not os.path.exists(spec_dir):
            os.makedirs(spec_dir)

        # Equivalent for "examples" subfolder
        spec_exp_dir = os.path.join(spec_dir, 'examples')
        if not os.path.exists(spec_exp_dir):
            os.makedirs(spec_exp_dir)

            with open(os.path.join(spec_exp_dir, "README.md"), "w") as example_file:
                example_file.write("## %s coding examples. \n" % spec_name)
                example_file.write("Folder that stores JSON-LD, RDFa or microdata examples.\n")
                example_file.write(">Examples will be added in a future map2model release.\n")            
                print("%s file structure created." % spec_name)

        # Either way, return the specification directory
        return spec_dir

    def __write_README(self, spec_md_folder, spec_dict):
        '''write a README for a particular spec_md_folder
 
           Parameters
           ==========
           spec_md_folder: a folder where a specification README should be written
           spec_dict: a dictionary with:
               name: the name of the folder (and Specification)
               workbook: the loaded workbook (or file to it)
               params: the original values in the configuration.yml for the folder
        '''
        spec_md_file_path = os.path.join(spec_md_folder, 'README.md')
        with open(spec_md_file_path, "w") as readme_file:
 
            # Look up some fields
            name = spec_dict['params']['name']
            version = spec_dict['params']['version']
            spec_type = spec_dict['params']['type']
 
            readme_file.write("## %s specification v. %s \n\n" % (name, version))
            readme_file.write("**%s** \n\n" % spec_type)

        for i_pos, step_hier in enumerate(reversed(formatted_spec['hierarchy'])):
            readme_file.write(step_hier)
            if i_pos < len(formatted_spec['hierarchy'])-1:
                readme_file.write(" > ")
        if formatted_spec['spec_type'] == "Type":
            readme_file.write(" > %s" % formatted_spec['name'])
        readme_file.write("\n\n**%s** \n" % formatted_spec['subtitle'].strip())
        readme_file.write("\n# Description \n")
        readme_file.write("%s \n" % formatted_spec['description'])
        readme_file.write("# Links \n")
        readme_file.write("- [Specification](http://bioschemas.org/bsc_specs/%s/specification/)\n" % formatted_spec['name'])
        readme_file.write("- [Specification source](specification.html)\n")
        readme_file.write("- [Mapping Spreadsheet](%s)\n" % formatted_spec['spec_mapping_url'])
        readme_file.write("- [Coding Examples](%s)\n" % formatted_spec['gh_examples'])
        readme_file.write("- [GitHUb Issues](%s)\n" % formatted_spec['gh_tasks'])
        readme_file.write("> These files were generated using [map2model](https://github.com/BioSchemas/map2model) Python Module.")
        readme_file.close()

========        # Perform validations first
        for spec_field in spec_workbook:
            validator = self.validator(spec_workbook)
            if validator.check_exists_worksheet('Specification Info'):

            spec_metadata[spec_field]=spec_dic[spec_field]
===========

    def parse_front_matter(self):

        # Dictionary of the entries in configuration.yml with folder name as index
        self.bsc_spec_list = self.bsc_file_manager.get_specification_list(self.input_folder)
        all_specs = self.__get_all_specs_list()

        for spec_dict in all_specs:

            # Create frontmatter post object with basic metadata
            temp_spec_post = self.__get_specification_post(spec_dict)

            if formatted_spec['spec_type'] == 'Type':
                temp_spec_post.metadata['layout']= 'new_type_detail'
            else:
                temp_spec_post.metadata['layout']= 'new_spec_detail'

            md_fm_bytes = BytesIO()
            temp_spec_post.metadata['version'] = str(temp_spec_post.metadata['version'])
            frontmatter.dump(temp_spec_post, md_fm_bytes)
            spec_name = temp_spec_post.metadata['name']

            # Create folder structure (examples) and README.md
            spec_md_file_path = self.__create_spec_folder_struct(spec_name)
            self.__write_README(spec_md_file_path, spec_dict)

            with open(spec_md_file_path+ '/specification.html', 'w') as outfile:
                temp_str=str(md_fm_bytes.getvalue(),'utf-8')
                outfile.write(temp_str)
                outfile.close()
            print ('%s MarkDown file generated.' % temp_spec_post.metadata['name'])
        os.remove(self.creds_file_path)
        print('Goggle Drive connection closed and credit file deleted.')
        print ('All Jekyll formatted MarkDown files generated.')
