# Author: Steven Warren
# Contact: sbw986@gmail.com
# File name: cnt_spincast_expander.py

def expand_bond_list_cnf(chip_pad_job,package_pad_job):
    """
    This program expands list of bond sites customized for spincast CNT bond jobs
    :param chip_pad_job: List of chip pad IDs to bond
    :param package_pad_job: List of package finger IDs to bond
    :return: expanded lists
    """

    chip_pad_job_left_D = []
    chip_pad_job_left_C = []
    chip_pad_job_left_B = []
    chip_pad_job_left_A = []
    chip_pad_job_right_D = []
    chip_pad_job_right_C = []
    chip_pad_job_right_B = []
    chip_pad_job_right_A = []

    package_pad_job_left_D = []
    package_pad_job_left_C = []
    package_pad_job_left_B = []
    package_pad_job_left_A = []
    package_pad_job_right_D = []
    package_pad_job_right_C = []
    package_pad_job_right_B = []
    package_pad_job_right_A = []

    grp_L_D = []
    grp_L_C = []
    grp_L_B = []
    grp_L_A = []
    grp_R_D = []
    grp_R_C = []
    grp_R_B = []
    grp_R_A = []

    chip_pt = ['PT01', 'CC01', 'PT02', 'PT03', 'CC03', 'PT04']
    package_pt = [59, 62, 116, 175, 178, 232]
    grp_PT = [1 for i,_ in enumerate(package_pt)]

    for chip,package in zip(chip_pad_job,package_pad_job):
        if package >=1 and package <= 58:
            if 'D' in chip:
                grp_L_D.append(1)
                grp_R_D.append(4)
                chip_pad_job_left_D.append(chip + 'L')
                chip_pad_job_right_D.append(chip + 'R')
                package_pad_job_left_D.append(package)
                package_pad_job_right_D.append(58 * 3 + 1 - package)
            elif 'C' in chip:
                grp_L_C.append(2)
                grp_R_C.append(3)
                chip_pad_job_left_C.append(chip + 'L')
                chip_pad_job_right_C.append(chip + 'R')
                package_pad_job_left_C.append(package)
                package_pad_job_right_C.append(58 * 3 + 1 - package)
            elif 'B' in chip:
                grp_L_B.append(3)
                grp_R_B.append(2)
                chip_pad_job_left_B.append(chip + 'L')
                chip_pad_job_right_B.append(chip + 'R')
                package_pad_job_left_B.append(package)
                package_pad_job_right_B.append(58 * 3 + 1 - package)
            elif 'A' in chip:
                grp_L_A.append(4)
                grp_R_A.append(1)
                chip_pad_job_left_A.append(chip + 'L')
                chip_pad_job_right_A.append(chip + 'R')
                package_pad_job_left_A.append(package)
                package_pad_job_right_A.append(58 * 3 + 1 - package)
            elif 'PT' in chip:
                grp_PT.append(1)

    chip_pad_job_expanded = chip_pad_job_left_D + chip_pad_job_left_C + chip_pad_job_left_B + chip_pad_job_left_A +\
                            chip_pad_job_right_A + chip_pad_job_right_B + chip_pad_job_right_C + chip_pad_job_right_D +\
                            chip_pt
    package_pad_job_expanded = package_pad_job_left_D + package_pad_job_left_C + package_pad_job_left_B + package_pad_job_left_A +\
                               package_pad_job_right_A + package_pad_job_right_B + package_pad_job_right_C + package_pad_job_right_D +\
                               package_pt
    groups_job_expanded = grp_L_D + grp_L_C + grp_L_B + grp_L_A + grp_R_A + grp_R_B + grp_R_C + grp_R_D + grp_PT

    return chip_pad_job_expanded, package_pad_job_expanded, groups_job_expanded

def expand_bond_list_erik(chip_pad_job,package_pad_job):
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

    chip_pt = ['PT01', 'CC01', 'PT02', 'PT03', 'CC03', 'PT04']
    package_pt = [59, 62, 116, 175, 178, 232]

    grp_L = [1 for i in range(len(chip_pad_job))]
    grp_R = [1 for i in range(len(chip_pad_job))]
    grp_PT = [2 for i,_ in enumerate(package_pt)]

    for chip,package in zip(chip_pad_job,package_pad_job):
        if package >=1 and package <= 58:

            chip_pad_job_left.append(chip + 'L')
            chip_pad_job_right.append(chip + 'R')
            package_pad_job_left.append(package)
            package_pad_job_right.append(58*3 + 1 - package)

    chip_pad_job_expanded = chip_pad_job_left + list(reversed(chip_pad_job_right)) + chip_pt
    package_pad_job_expanded = package_pad_job_left + list(reversed(package_pad_job_right)) + package_pt
    groups_job_expanded = grp_L + list(reversed(grp_R)) + grp_PT

    return chip_pad_job_expanded, package_pad_job_expanded, groups_job_expanded