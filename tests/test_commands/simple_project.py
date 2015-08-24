project_1_yaml = {
    'common': {
        'sources': ['test_workspace/main.cpp'],
        'includes': ['test_workspace/header1.h'],
        'macros': ['MACRO1', 'MACRO2'],
        'target': ['lpc1768'],
        'core': ['core1'],
        'output_type': ['exe'],
        'debugger': ['j-link'],
    },
    'tool_specific' : {
        'make_gcc_arm':{
            'linker_file' : ['test_workspace/linker.ld']
        },
        'iar_arm':{
            'linker_file' : ['test_workspace/linker.ld']
        },
        'uvision':{
            'linker_file' : ['test_workspace/linker.ld']
        },
        'coide':{
            'linker_file' : ['test_workspace/linker.ld']
        }
    }
}

project_2_yaml = {
    'common': {
        'sources': ['test_workspace/main.cpp'],
        'includes': ['test_workspace/header1.h'],
        'macros': ['MACRO1', 'MACRO2'],
        'target': ['lpc1768'],
        'core': ['core2'],
        'output_type': ['exe'],
        'debugger': ['j-link'],
    },
    'tool_specific' : {
        'make_gcc_arm':{
            'linker_file' : ['test_workspace/linker.ld']
        },
        'iar_arm':{
            'linker_file' : ['test_workspace/linker.ld']
        },
        'uvision':{
            'linker_file' : ['test_workspace/linker.ld']
        },
        'coide':{
            'linker_file' : ['test_workspace/linker.ld']
        }
    }
}

projects_yaml = {
    'projects': {
        'project_1': ['test_workspace/project_1.yaml'],
        'project_2': ['test_workspace/project_2.yaml']
    }
}
