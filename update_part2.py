'''
  (C) Crown Copyright 2022 Met Office

  @author: David Simonin?

  Adapted for GeoVaLs file by Anna Shlyaeva
'''
import os
import shutil
import netCDF4
import sys

def _renameVariableInDataFile_(input_file, output_file, old_variable_name, new_variable_name):
    '''rename a variable in a netCDF file
       
       input_file        - directory and filename of current data file (str)
       output_file       - directory and filename of the new data file (str)
       old_variable_name - Name of the variable that needs to be replaced.
       new_variable_name - Name of the new variable.
    '''

    data = netCDF4.Dataset(input_file)
    if (old_variable_name in data.variables):
        print("Renaming ", old_variable_name, " in ", input_file, " to ", new_variable_name)
        trg = netCDF4.Dataset(output_file, mode='w')
        src = data
        for name, dim in src.dimensions.items():
            trg.createDimension(name, len(dim) if not dim.isunlimited() else None)

        # Copy the global attributes
        trg.setncatts({a:src.getncattr(a) for a in src.ncattrs()})

        # Create the variables in the file
        for name, var in src.variables.items():
            thisname = name
            if (name == old_variable_name):
                thisname = new_variable_name
            trg.createVariable(thisname, var.dtype, var.dimensions)
            # Copy the variable attributes
            trg.variables[thisname].setncatts({a:var.getncattr(a) for a in var.ncattrs()})

            # Copy the variables values (as 'f4' eventually)
            trg.variables[thisname][:] = src.variables[name][:]

        trg.close()

def renameVariableInDataFile(workingDir, old_name, new_name):
    for workingDir_ in workingDir:
        repoName = workingDir_.split('/')[-2]
        for root,d_names,f_names in os.walk(workingDir_):
            for f in f_names:
                file_path_source = os.path.join(root, f)
                outfile = file_path_source+"_new.nc4"
                if f.endswith('.nc4') :
                    _renameVariableInDataFile_(file_path_source, outfile, old_name, new_name)
                if f.endswith('.nc') :
                    _renameVariableInDataFile_(file_path_source, outfile, old_name, new_name)
                if (os.path.exists(outfile)):
                    shutil.move(outfile, file_path_source)

def renameVariableInList(workingDir, old_name, new_name, filenames):
    for workingDir_ in workingDir:
        repoName = workingDir_.split('/')[-2]
        for root,d_names,f_names in os.walk(workingDir_):
            for f in f_names:
                if f in filenames:
                  file_path_source = os.path.join(root, f)
                  outfile = file_path_source+"_new.nc4"
                  if f.endswith('.nc4') :
                      _renameVariableInDataFile_(file_path_source, outfile, old_name, new_name)
                  if f.endswith('.nc') :
                      _renameVariableInDataFile_(file_path_source, outfile, old_name, new_name)
                  if (os.path.exists(outfile)):
                      shutil.move(outfile, file_path_source)


if __name__ == '__main__':

    # Change variable name in NetCDF/HDF5 file
    # -------------------------------------------------------------------------------
    workingDir = ["./"]
    # could also be specific_humidity_at_two_meters_above_surface
    renameVariableInDataFile(workingDir, "specific_humidity", "water_vapor_mixing_ratio_wrt_moist_air")
    renameVariableInDataFile(workingDir, "specific_humidity_at_two_meters_above_surface", "water_vapor_mixing_ratio_wrt_moist_air_at_2m")
    renameVariableInDataFile(workingDir, "specific_humidity_background_error", "water_vapor_mixing_ratio_wrt_moist_air_background_error")
    renameVariableInDataFile(workingDir, "water_vapor_mixing_ratio_wrt_moist_air_and_condensed_water", "water_vapor_mixing_ratio_wrt_moist_air")
    renameVariableInDataFile(workingDir, "water_vapor_mixing_ratio_wrt_moist_air_and_condensed_water_at_2m", "specific_humidity_at_two_meters_above_surface")
    renameVariableInDataFile(workingDir, "specific_humidity_at_two_meters_above_surface", "water_vapor_mixing_ratio_wrt_moist_air_at_2m")
    renameVariableInDataFile(workingDir, "water_vapor_mixing_ratio_wrt_moist_air_and_condensed_water_background_error", "water_vapor_mixing_ratio_wrt_moist_air_background_error")

#    # List of variables to remove condensed water from
#    files = ["gnssro_geoval_2018041500_1obs_bending_angle.nc4", "scatwind_geoval_2020121500_m.nc", "sfc_geoval_2020121500_m.nc", 
#             "sfcship_geoval_2020121500_m.nc", "gnssro_geoval_2018041500_3prof.nc4", "rass_tv_geoval_2020121500.nc",
#             "sondes_geovals_2021121200_m.nc4", "scatwind_geovals_2021121200_m.nc4",
#             "vadwind_geoval_2020121500.nc", "sfcship_geovals_2021121200_m.nc4", "pibal_geovals_2021121200_m.nc4",
#             "pibal_geoval_2021121200_m.nc4", "satwind_geovals_2021121200_m.nc4", "aircraft_geovals_2021121200_m.nc4",
#             "satwind_geoval_2020121500_m.nc", "sfc_geovals_2021121200_m.nc4", "sondes_geoval_2020121500_m.nc",
#             "aircraft_geoval_2020121500_m.nc", "gnssro_bend_geoval_2022061500_m.nc4", "gnssro_geoval_2018041500_m.nc4",
#             "gnssro_geoval_2018041500_s.nc4", "sondes_q_geoval_2020121500.nc4", "gnssro_geoval_2018041500_s_2d.nc4",
#             "aircraft_geoval_2018041500_m.nc4", "geovals_radar_mrms_202205122200.nc",
#             "gsisfc_tsen_geoval_2018041500_m.nc4", "gsisfc_uv_geoval_2018041500_m.nc4", "sondes_background_error_vert_interp_air_pressure_geoval_2018041500_s.nc4",
#             "sondes_background_error_vert_interp_height_geoval_2018041500_s.nc4", "geovals-mpas.mrms_reflectivity.20220216T000000Z_s.nc",
#             "aircraft_geoval_2018041500_s.nc4", "amsua_n19_geoval_2018041500_m_rttovcpp.nc4"]
#    renameVariableInList(workingDir, "water_vapor_mixing_ratio_wrt_moist_air_and_condensed_water", "water_vapor_mixing_ratio_wrt_moist_air", files)
#    files = ["sondes_background_error_vert_interp_height_obsdiag_2018041500_s.nc4"]
#    renameVariableInList(workingDir, "water_vapor_mixing_ratio_wrt_moist_air_background_error", "water_vapor_mixing_ratio_wrt_moist_air_and_condensed_water_background_error", files)
#    files = ["sondes_background_error_vert_interp_air_pressure_obsdiag_2018041500_s.nc4", "sondes_background_error_vert_interp_height_obsdiag_2018041500_s.nc4"]
#    renameVariableInList(workingDir, "water_vapor_mixing_ratio_wrt_moist_air_and_condensed_water_background_error", "water_vapor_mixing_ratio_wrt_moist_air_background_error", files)


