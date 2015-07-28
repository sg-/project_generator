# Copyright 2015 0xc0170
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
import os
import yaml
import shutil

from unittest import TestCase

from project_generator.generate import Generator
from simple_project import *


class TestProject(TestCase):

    """test things related to the uvision tool"""

    def setUp(self):
        if not os.path.exists('test_workspace'):
            os.makedirs('test_workspace')
        # write project file
        with open(os.path.join(os.getcwd(), 'test_workspace/project_1.yaml'), 'wt') as f:
            f.write(yaml.dump(project_1_yaml, default_flow_style=False))
        # write projects file
        with open(os.path.join(os.getcwd(), 'test_workspace/projects.yaml'), 'wt') as f:
            f.write(yaml.dump(project_1_yaml, default_flow_style=False))

        self.project = Generator(projects_yaml).generate('project_1').next()

    def tearDown(self):
        # remove created directory
        shutil.rmtree('test_workspace', ignore_errors=True)
        shutil.rmtree('generated_projects', ignore_errors=True)

    def test_export_project(self):
        self.project.export('uvision', False)
        projectfiles = self.project.get_generated_project_files('uvision')
        assert projectfiles
        assert os.path.splitext(projectfiles['files'][0])[1] == '.uvproj'

    def test_export_project_to_diff_directory(self):
        project_1_yaml['common']['export_dir'] = ['create_this_folder']
        with open(os.path.join(os.getcwd(), 'test_workspace/project_1.yaml'), 'wt') as f:
            f.write(yaml.dump(project_1_yaml, default_flow_style=False))
        generator = Generator(projects_yaml)
        for project in generator.generate('project_1'):
            project.export('uvision', False)

        assert os.path.isdir('create_this_folder')
        shutil.rmtree('create_this_folder')

    def test_build_project(self):
     self.project.export('uvision', False)
     self.project.build('uvision')
