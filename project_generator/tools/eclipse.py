# Copyright 2014 0xc0170
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from posixpath import normpath, join, basename

from .exporter import Exporter
from .builder import Builder
from .gccarm import MakefileGccArm
from ..util import FILES_EXTENSIONS, SOURCE_KEYS
import os
from itertools import chain
import ntpath

class EclipseGnuARM(Exporter, Builder):
    file_types = {}
    for key in SOURCE_KEYS:
        for extension in FILES_EXTENSIONS[key]:
            file_types[extension] = 1

    def __init__(self, workspace, env_settings):
        self.definitions = 0
        self.exporter = MakefileGccArm(workspace, env_settings)
        self.workspace = workspace
        self.env_settings = env_settings

    @staticmethod
    def get_toolnames():
        return ['eclipse_make_gcc_arm', 'make_gcc_arm']

    @staticmethod
    def get_toolchain():
        return 'make_gcc_arm'

    def _expand_data(self, old_data, new_data, group):
        """ data expansion - uvision needs filename and path separately. """
        if group == 'Sources':
            old_group = None
        else:
            old_group = group
        for source in old_data[old_group]:
            if source:
                extension = source.split(".")[-1]
                # TODO: fix - workaround for windows, seems posixpath does not work
                source = source.replace('\\', '/')
                #source = source.replace(new_data['rel_path'], '')
                new_file = {"path": join('PARENT-%s-PROJECT_LOC' % new_data['output_dir']['rel_path'], normpath(source)), "name": basename(
                    source), "type": self.file_types[extension]}
                new_data['groups'][group].append(new_file)

    def _get_groups(self, data):
        """ Get all groups defined. """
        groups = []
        for attribute in SOURCE_KEYS:
                if data[attribute]:
                    for k, v in data[attribute].items():
                        if k == None:
                            k = 'Sources'
                        if k not in groups:
                            groups.append(k)
        return groups

    def _iterate(self, data, expanded_data, rel_path):
        """ Iterate through all data, store the result expansion in extended dictionary. """

        relpath = expanded_data['rel_path']
        for key in FILES_EXTENSIONS.keys():
            if type(expanded_data[key]) is dict:
                for k,v in expanded_data[key].items():
                    expanded_data[key][k] = [path.replace(relpath, '') for path in v]
            elif type(expanded_data[key]) is list:
                expanded_data[key] = [path.replace(relpath, '') for path in expanded_data[key]]
            else:
                expanded_data[key] = expanded_data[key].replace(relpath, '')
        

        for attribute in SOURCE_KEYS:
            for k, v in data[attribute].items():
                if k == None:
                    group = 'Sources'
                else:
                    group = k
                self._expand_data(data[attribute], expanded_data, group)

    def build_project(self):
        self.exporter.build_project()

    def _get_libs(self, data):
        data['lib_paths'] =[]
        data['libraries'] =[]
        data['source_files_a'] = list(chain(*data['source_files_a'].values()))
        for lib in data['source_files_a']:
            head, tail = ntpath.split(lib)
            file = tail
            if (os.path.splitext(file)[1] != ".a"):
                continue
            else:
                file = file.replace(".a","")
                data['lib_paths'].append(head)
                data['libraries'].append(file.replace("lib",''))

    def generate_project(self):
        """ Processes groups and misc options specific for eclipse, and run generator """

        data_for_make = self.workspace.copy()

        self.exporter.process_data_for_makefile(data_for_make)
        self.gen_file_jinja('makefile_gcc.tmpl', data_for_make, 'Makefile', data_for_make['output_dir']['path'])

        expanded_dic = self.workspace.copy()

        expanded_dic ['core'] = expanded_dic ['target'].core.lower()
        if expanded_dic['core'] == 'cortex-m4f':
            expanded_dic['core'] = 'cortex-m4'

        # change cortex-m0+ to cortex-m0plus
        if expanded_dic['core'] == 'cortex-m0+':
            expanded_dic['core'] = 'cortex-m0plus'

        expanded_dic['rel_path'] = data_for_make['output_dir']['rel_path']
        groups = self._get_groups(expanded_dic)
        expanded_dic['groups'] = {}
        for group in groups:
            expanded_dic['groups'][group] = []
        self._iterate(self.workspace, expanded_dic, expanded_dic['rel_path'])

        self._get_libs(expanded_dic)
        # Project file

        self.gen_file_jinja(
            'eclipse_makefile.cproject.tmpl', expanded_dic, '.cproject', data_for_make['output_dir']['path'])
        self.gen_file_jinja(
            'eclipse.project.tmpl', expanded_dic, '.project', data_for_make['output_dir']['path'])
        return 0

    def get_generated_project_files(self):
        return {'path': self.workspace['path'], 'files': [self.workspace['files']['proj_file'], self.workspace['files']['cproj'],
            self.workspace['files']['makefile']]}

