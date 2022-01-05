# (C) Copyright 2017-2022 UCAR.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.

################################################################################
# UFO Test Files
################################################################################

cmake_minimum_required( VERSION 3.3.2 FATAL_ERROR )

project( ufo_data VERSION 1.1.0 DESCRIPTION "UFO Test Files" )

find_package( ecbuild QUIET )
include( ecbuild_system NO_POLICY_SCOPE )
ecbuild_declare_project()
set( CMAKE_DIRECTORY_LABELS ${PROJECT_NAME} )

# This CMake script adds many tests to validate all of the testing data files
# within the ufo-data repository.

find_package(ioda REQUIRED)

file( GLOB_RECURSE OBS_FILES *.nc4 *.nc *.ioda )
# We filter the expression to remove the geovals
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)geoval(.*)" )
# Remove satbias files
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)satbias(.*)" )
# Remove misc test files
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)interpolation(.*)" )
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)obserror_multi_variant(.*)" )


list( LENGTH OBS_FILES OBS_FILES_LEN )

foreach ( f ${OBS_FILES} )
	get_filename_component(filename ${f} NAME)

	# Note: IODA_YAML_ROOT is provided by find_package(ioda).
	# The ObsSpace.yaml file is *not* a test file. It always exists.
	ecbuild_add_test(
		TARGET ufo_data_validate_${filename}
		COMMAND ioda-validate.x
		LABELS ufo_data_validate
		ENVIRONMENT "ECKIT_COLOUR_OUTPUT=1"
		ARGS "${IODA_YAML_ROOT}/validation/ObsSpace.yaml" "${f}"
		)
endforeach()



# Data file "installation" and project CMake exports


ecbuild_print_summary()

