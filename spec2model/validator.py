from openpyxl import load_workbook
import os
import sys

class FolderValidator:

    def __str__(self):
        return '[folder-validator:%s]' % self.name

    def __repr__(self):
        return self.__str__()

    def __init__(self, folder):

        self.folder = os.path.abspath(folder)
        self.name = os.path.basename(folder)
        self.defaults = WorksheetDefaults(self.name, folder)

    def validate(self, folder=None):
        '''validate runs each set of tests, and returns a list of results.
           If any validators fail, we return a False (failed) validation,
           otherwise True
        '''
        results = [self.validate_exists(folder),
                   self.validate_files()]

        for result in results:
            if result == False:
                return result
        return result

    def validate_exists(self, folder=None):
        '''Ensure the folder exists
 
           Parameters
           ==========
           folder: full (or relative) path to folder
        '''        
        if folder is None:
            folder = self.folder

        if not os.path.exists(folder):
            print('Invalid: Worksheet folder %s does not exist' % folder)
            return False
        return True

    def validate_files(self, ext='tsv'):
        '''Ensure that default files (self.defaults) exist in the folder
           (self.folder) 
        '''
        paths = self.defaults.get_paths()
        for key, path in paths.items():
            # 1. If changed the defaults, we wouldn't be able to load
            if not self.validate_extension(path, ext=ext):
                return False
 
            # 2. The path must exist
            if not os.path.exists(path):
                print('Invalid: Cannot find %s' % path)
                return False
        return True

    def validate_extension(self, path, ext='tsv'):
        '''Ensure the worksheet is a tsv file (default ends in tsv)
 
           Parameters
           ==========
           path: a name (string) of the worksheet file
           ext: the extension to check using "endswith"
        '''
        if not path.endswith(ext):
            print('Invalid: Worksheet %s must have extension %s' % (path, ext))
        return path.endswith(ext)
        

class WorksheetDefaults:
    
    def __init__(self, name, folder=None):
        self.name = name
        self.lookup = self.set_names(name)
        self.paths = self.set_paths(folder)
 
    def get_names(self):
        return self.lookup

    def get_paths(self):
        return self.paths

    def set_paths(self, folder=None):
        '''define expected set of file (fullpath) from names lookup with
           a folder name.

           Parameters
           ==========
           name: the name of the specification
        '''
        paths = {}
        if folder is not None:
            for key, filename in self.lookup.items():
                paths[key] = os.path.join(folder, filename)
        return paths

    def set_names(self, name, ext='tsv'):
        '''define expected set of file names (basepath) 
           based on Specification Name

           Parameters
           ==========
           name: the name of the specification
        '''
        lookup = {'mapping_file': '%s - Mapping.%s' % (name, ext),
                  'specification_file': '%s - Specification.%s' % (name, ext),
                  'bioschemas_file': '%s - Bioschemas.%s' % (name, ext),
                  'authors_file': '%s - Authors.%s' % (name, ext)}
        return lookup
