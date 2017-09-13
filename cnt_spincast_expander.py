# Author: Steven Warren
# Contact: sbw986@gmail.com
# File name: cnt_spincast_expander.py

def expand_bond_list(chip_pad_job,package_pad_job):
    """
    This program expands list of bond sites customized for spincast CNT bond jobs
    :param chip_pad_job: List of chip pad IDs to bond
    :param package_pad_job: List of package finger IDs to bond
    :return: expanded lists
    """

    chip_pad_job_left = []
    chip_pad_job_right = []

    package_pad_job_left = []
    package_pad_job_right = []

    for chip,package in zip(chip_pad_job,package_pad_job):
        chip_pad_job_left.append(chip + 'L')
        chip_pad_job_right.append(chip + 'R')
        package_pad_job_left.append(package)
        package_pad_job_right.append(58*3 + 1 - package)

    chip_pad_job_expanded = chip_pad_job_left + list(reversed(chip_pad_job_right))
    package_pad_job_expanded = package_pad_job_left + list(reversed(package_pad_job_right))

    return chip_pad_job_expanded, package_pad_job_expanded