# (C) Copyright 2017-2021 UCAR
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.

#
# IODA bundle
#

cmake_minimum_required( VERSION 3.12 FATAL_ERROR )

project( ioda-bundle VERSION 1.0.0 LANGUAGES C CXX Fortran )

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

include( ecbuild_bundle )

set( ENABLE_MPI ON CACHE BOOL "Compile with MPI" )

ecbuild_bundle_initialize()

ecbuild_bundle( PROJECT jedicmake GIT "https://github.com/JCSDA-internal/jedi-cmake.git" )
include( jedicmake/cmake/Functions/git_functions.cmake )

# ECMWF libs
# ----------
option("BUNDLE_SKIP_ECKIT" "Don't build eckit" "ON" ) # Skip eckit build unless user passes -DBUNDLE_SKIP_ECKIT=OFF
option("BUNDLE_SKIP_FCKIT" "Don't build fckit" "ON") # Skip fckit unless user passes -DBUNDLE_SKIP_FCKIT=OFF
option("BUNDLE_SKIP_ATLAS" "Don't build atlas" "ON") # Skip atlas unless user passes -DBUNDLE_SKIP_ATLAS=OFF
option("BUNDLE_SKIP_ODC" "Don't build odc" "ON") # Skip odc unless user passes -DBUNDLE_SKIP_ODC=OFF

ecbuild_bundle( PROJECT eckit GIT "https://github.com/ecmwf/eckit.git" TAG 1.18.2 )
ecbuild_bundle( PROJECT fckit GIT "https://github.com/ecmwf/fckit.git" TAG 0.9.5 )
ecbuild_bundle( PROJECT atlas GIT "https://github.com/ecmwf/atlas.git" TAG 0.27.0 )
ecbuild_bundle( PROJECT odc GIT "https://github.com/ecmwf/odc.git" TAG 1.4.4 )

# Core JEDI repositories
ecbuild_bundle( PROJECT oops GIT "https://github.com/JCSDA-internal/oops.git" )
ecbuild_bundle( PROJECT ioda GIT "https://github.com/JCSDA-internal/ioda.git" )

ecbuild_bundle( PROJECT ufo-data GIT "https://github.com/JCSDA-internal/ufo-data.git" )


# Build IODA converters
option(BUILD_IODA_CONVERTERS "Build IODA Converters" OFF)
if(BUILD_IODA_CONVERTERS)
  ecbuild_bundle( PROJECT iodaconv GIT "https://github.com/JCSDA-internal/ioda-converters.git" )
endif()

# Build Doxygen documentation
option(BUILD_IODA_BUNDLE_DOC "Build documentation" OFF)
if(BUILD_IODA_BUNDLE_DOC)
   add_subdirectory( Documentation )
endif(BUILD_IODA_BUNDLE_DOC)

ecbuild_bundle_finalize()

include(cmake/cdash-integration.cmake)
include(CTest)
