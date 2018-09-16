import spec2model.file_manager as f_manager
import spec2model.mapping as mapper
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

    def __get_all_specs_dic(self):
        all_specs =[]
        for bsc_spec in self.bsc_spec_list:
            self.bsc_parser.set_gsheet_id(bsc_spec)
            self.bsc_parser.set_spec_metadata(self.bsc_spec_list[bsc_spec])
            all_specs.append(self.bsc_parser.get_mapping_g_sheets())
        return all_specs

    def __get_specification_post(self, spec_dic):
        spec_metadata={}
        spec_post=frontmatter.Post('')
        for spec_field in spec_dic:
            spec_metadata[spec_field]=spec_dic[spec_field]
        spec_post.metadata=spec_metadata
        return spec_post

    def __create_spec_folder_struct(self, spec_name):
        spec_dir = self.md_files_path + spec_name + '/'
        if not os.path.exists(spec_dir):
            os.makedirs(spec_dir)

        spec_exp_dir = spec_dir + 'examples/'

        if not os.path.exists(spec_exp_dir):
            os.makedirs(spec_exp_dir)
            example_file = open(spec_exp_dir+"README.md","w")
            example_file.write("## %s coding examples. \n" % spec_name)
            example_file.write("Folder that stores JSON-LD, RDFa or microdata examples.\n")
            example_file.write(">Examples will be added in a future map2model release.\n")
            example_file.close()
        print("%s file structure created." % spec_name)

    def __write_README(self, spec_md_file_path, formatted_spec):
        readme_file = open(spec_md_file_path+"/README.md","w")
        readme_file.write("## %s specification v. %s \n\n" % (formatted_spec['name'], formatted_spec['version']))

        readme_file.write("**"+formatted_spec['spec_type']+"** \n\n")

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

    def parse_front_matter(self):

        self.bsc_spec_list = self.bsc_file_manager.get_specification_list(self.input_folder)
        all_specs_formatted=self.__get_all_specs_dic()

        for formatted_spec in all_specs_formatted:
            temp_spec_post=self.__get_specification_post(formatted_spec)
            if formatted_spec['spec_type'] == 'Type':
                temp_spec_post.metadata['layout']= 'new_type_detail'
            else:
                temp_spec_post.metadata['layout']= 'new_spec_detail'
            md_fm_bytes = BytesIO()
            temp_spec_post.metadata['version'] = str(temp_spec_post.metadata['version'])
            frontmatter.dump(temp_spec_post, md_fm_bytes)
            spec_name=temp_spec_post.metadata['name']
            self.__create_spec_folder_struct(spec_name)
            spec_md_file_path=self.md_files_path + spec_name
            self.__write_README(spec_md_file_path, formatted_spec)
            with open(spec_md_file_path+ '/specification.html', 'w') as outfile:
                temp_str=str(md_fm_bytes.getvalue(),'utf-8')
                outfile.write(temp_str)
                outfile.close()
            print ('%s MarkDown file generated.' % temp_spec_post.metadata['name'])
        os.remove(self.creds_file_path)
        print('Goggle Drive connection closed and credit file deleted.')
        print ('All Jekyll formatted MarkDown files generated.')
