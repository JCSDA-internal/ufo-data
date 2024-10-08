'''
  (C) Crown Copyright 2022 Met Office

  @author: David Simonin?

  Adapted for GeoVaLs file by Anna Shlyaeva
'''
import os
import shutil
import netCDF4


def _renameVariableInDataFile_(input_file, output_file, old_variable_name, new_variable_name):
    '''rename a variable in a netCDF file
       
       input_file        - directory and filename of current data file (str)
       output_file       - directory and filename of the new data file (str)
       old_variable_name - Name of the variable that needs to be replaced.
       new_variable_name - Name of the new variable.
    '''

    data = netCDF4.Dataset(input_file)
    if (old_variable_name in data.variables):
        print("Renaming variable in file ", input_file)
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

if __name__ == '__main__':

    # Change variable name in NetCDF/HDF5 file
    # -------------------------------------------------------------------------------
    workingDir = ["/Users/annash/Documents/jedi/code/jedi-bundle/ufo-data/."]
    renameVariableInDataFile(workingDir, "surface_temperature", "air_temperature_at_2m")
    renameVariableInDataFile(workingDir, "surface_temperature_where_sea", "surface_skin_temperature_where_sea")
    renameVariableInDataFile(workingDir, "surface_temperature_where_land", "surface_skin_temperature_where_land")
    renameVariableInDataFile(workingDir, "surface_temperature_where_ice", "surface_skin_temperature_where_ice")
    renameVariableInDataFile(workingDir, "surface_temperature_where_snow", "surface_skin_temperature_where_snow")
    renameVariableInDataFile(workingDir, "skin_temperature", "surface_skin_temperature")
