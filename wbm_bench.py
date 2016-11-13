###PYTHON2
from ILAMB.Variable import Variable
from ILAMB.ModelResult import ModelResult
from ILAMB.Confrontation import Confrontation
from netCDF4 import Dataset
import os

# Testing how data can be accessed

CAETE= ModelResult("./MODELS/CAETE", modelname = "CAETE")

#GLEAM = Variable(filename = "./DATA/et/GLEAM/et_GLEAM_1981_2010.nc", 
#                    variable_name = "et")

#Changing temporal scale to match with CAETE data (dont execute_ only for doc)
#GLEAM_AC=GLEAM.annualCycle()
#fcc = Dataset("et_GLEAM_1981_2010.nc", 'w')
#GLEAM_AC.toNetCDF4(fcc)
#fcc.close()

# Creating data confrontation

GLEAM_C = Confrontation(source   = './DATA/et/GLEAM/et_GLEAM_1981_2010.nc',
                  name     = "GLEAM",
                  variable = "annual_cycle_mean_of_et")

obs,mod = GLEAM_C.stageData(CAETE)

#GLEAM_C.confront(CAETE)

bias     = obs.bias(mod)
rmse     = obs.rmse(mod)
