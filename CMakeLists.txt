# (C) Copyright 2017-2022 UCAR.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.

################################################################################
# UFO Test Files
################################################################################

cmake_minimum_required( VERSION 3.12 )
project( ufo-data VERSION 1.13.0 DESCRIPTION "UFO Test Files" )

find_package( ecbuild QUIET )
include( ecbuild_system NO_POLICY_SCOPE )
ecbuild_declare_project()
set( CMAKE_DIRECTORY_LABELS ${PROJECT_NAME} )

ecbuild_install_project( NAME ${PROJECT_NAME} )
ecbuild_print_summary()
