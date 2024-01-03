# (C) Copyright 2017-2022 UCAR.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.

################################################################################
# UFO Test Files
################################################################################

cmake_minimum_required( VERSION 3.3.2 FATAL_ERROR )

project( ufo_data VERSION 1.9.0 DESCRIPTION "UFO Test Files" )

find_package( ecbuild QUIET )
include( ecbuild_system NO_POLICY_SCOPE )
ecbuild_declare_project()
set( CMAKE_DIRECTORY_LABELS ${PROJECT_NAME} )

# This CMake script adds many tests to validate all of the testing data files
# within the ufo-data repository.

find_package(ioda REQUIRED)

file( GLOB_RECURSE OBS_FILES *.nc4 *.nc *.ioda )
# We filter the expression to remove the geovals and obsdiag files, which are geovals-based
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)geoval(.*)" )
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)obsdiag(.*)" )
# Remove satbias files
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)satbias(.*)" )
# Remove misc test files
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)interpolation(.*)" )
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)obserror_multi_variant(.*)" )

# Remove known buggy non-obs files
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)met_office_gauss_thinning_groundgnssnames_obs.nc4" )
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)obserror_4d.nc" )  # Wrong dimension attachment
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)obserror_2d_fullr.nc" )
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)obserror_latitude_longitude.nc" )
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)satwind_pressure_errors.nc4" )
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)satwind_pressure_errors_nomissing.nc4" )
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)scatwind_obs_2d_2020100106.nc4" )
list( FILTER OBS_FILES EXCLUDE REGEX "(.*)superob_testdata.nc4" )

foreach ( f ${OBS_FILES} )
	get_filename_component(filename ${f} NAME)

	# Note: IODA_YAML_ROOT is provided by find_package(ioda).
	# The ObsSpace.yaml file is *not* a test file. It always exists.
	ecbuild_add_test(
		TARGET ufo_data_validate_${filename}
		COMMAND ioda-validate.x
		LABELS ufo_data_validate
		ENVIRONMENT "ECKIT_COLOUR_OUTPUT=1"
		ARGS "--ignore-warn"
                     "--ignore-error"
                     "${IODA_YAML_ROOT}/validation/ObsSpace.yaml"
                     "${f}"
		)
endforeach()



ecbuild_print_summary()

