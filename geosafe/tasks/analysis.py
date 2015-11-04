import os
from subprocess import call, Popen, PIPE
from celery.task import task
from geonode.layers.utils import file_upload

__author__ = 'lucernae'


@task(name='geosafe.tasks.analysis.run_analysis_docker', queue='cleanup')
def run_analysis_docker(arguments, output_file, layer_folder, output_folder):
    """
    Running an analysis via InaSAFE cli in docker container

    (useful for sandboxing InaSAFE environment and deps)
    """
    # call system function
    call(["inasafe", arguments, layer_folder, output_folder])
    # TODO: Save the layer file and all info to geonode (upload?)
    saved_layer = file_upload(
        output_file,
        overwrite=True,
    )
    saved_layer.set_default_permissions()


@task(name='geosafe.tasks.analysis.run_analysis_cli', queue='cleanup')
def run_analysis_cli(arguments, output_file):
    """
    Running an analysis via InaSAFE CLI directly in the filesystem

    inasafe-cli should be installed on /usr/local/bin or in the PATH
    """
    # call system function
    call("inasafe "+arguments)
    # TODO: Save the layer file and all info to geonode (upload?)


@task(name='geosafe.tasks.analysis.if_list', queue='cleanup')
def if_list(hazard_file=None, exposure_file=None):
    """
    Show possible IF list

    Can also return filtered IF list if arguments is provided
    :return: Filtered list of Impact Function IDs
    :rtype: list
    """
    # call system function
    if hazard_file and exposure_file:
        p = Popen(["inasafe", "--hazard=%s --exposure=%s --list-functions" % (
            hazard_file, exposure_file
        )], stdout=PIPE)
    else:
        p = Popen(["inasafe", "--list-functions"], stdout=PIPE)

    output, err = p.communicate()
    start = False
    ifs = []
    for line in output.split('\n'):
        if line == 'Available Impact Function:' and not start:
            start = True
        elif start and not line.strip() == '':
            ifs.append(line)
        elif start and line.strip() == '':
            break
    return ifs
