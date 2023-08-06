##################################################################################################
# Based on https://gitlab.cern.ch/atlas-physics/stat/tools/StatisticsTools by Stefan Gadatsch
# Author: Alkaid Cheng
# Email: chi.lung.cheng@cern.ch
##################################################################################################
import os
import math
import fnmatch
from typing import List, Optional

import ROOT

import quickstats
from quickstats.components.numerics import is_integer
from quickstats.utils.root_utils import load_macro

class ExtendedModel(object):
    def __init__(self, fname:str, ws_name:Optional[str]=None, model_config_name:Optional[str]=None,
                 data_name:str="combData", snapshot_name:Optional[str]="nominalNuis",
                 binned_likelihood:bool=True, tag_as_measurement:str="pdf_",
                 fix_cache:bool=True, fix_multi:bool=True, interpolation_code:int=-1,
                 load_extension:bool=True):
        self.fname = fname
        self.ws_name = ws_name
        self.mc_name = model_config_name
        self.data_name = data_name
        self.snapshot_name = snapshot_name
        self.binned_likelihood = binned_likelihood
        self.tag_as_measurement = tag_as_measurement
        self.fix_cache = fix_cache
        self.fix_multi = fix_multi
        self.interpolation_code = interpolation_code
        if load_extension:
            self.load_extension()
        self.initialize()
  
    @property
    def file(self):
        return self._file
    @property
    def workspace(self):
        return self._workspace
    @property
    def model_config(self):
        return self._model_config
    @property
    def pdf(self):
        return self._pdf
    @property
    def data(self):
        return self._data
    @property
    def nuisance_parameters(self):
        return self._nuisance_parameters
    @property
    def global_observables(self):
        return self._global_observables
    @property
    def pois(self):
        return self._pois
    @property
    def observables(self):
        return self._observables        
    
    @staticmethod
    def load_extension():
        try:
            if not hasattr(ROOT, 'RooTwoSidedCBShape'):
                result = load_macro('RooTwoSidedCBShape')
                if hasattr(ROOT, 'RooTwoSidedCBShape'):
                    print('INFO: Loaded extension module "RooTwoSidedCBShape"')
        except Exception as e:
            print(e)
    @staticmethod
    def modify_interp_codes(ws, interp_code, classes=None):
        if classes is None:
            classes = [ROOT.RooStats.HistFactory.FlexibleInterpVar, ROOT.PiecewiseInterpolation]
        for component in ws.components():
            for cls in classes:
                if (component.IsA() == cls.Class()):
                    component.setAllInterpCodes(interp_code)
                    class_name = cls.Class_Name().split('::')[-1]
                    print('INFO: {} {} interpolation code set to {}'.format(component.GetName(),
                                                                            class_name,
                                                                            interp_code))
        return None

    @staticmethod
    def activate_binned_likelihood(ws):
        print('INFO: Activating binned likelihood evaluation')
        for component in ws.components():
            if (component.IsA() == ROOT.RooRealSumPdf.Class()):
                component.setAttribute('BinnedLikelihood')
                print('INFO: Activated binned likelihood attribute for {}'.format(component.GetName()))
        return None
                          
    @staticmethod
    def set_measurement(ws, condition):
        print('INFO: Activating measurements to reduce memory consumption')
        for component in ws.components():
            name = component.GetName()
            if ((component.IsA() == ROOT.RooAddPdf.Class()) and condition(name)):
                component.setAttribute('MAIN_MEASUREMENT')
                print('INFO: Activated main measurement attribute for {}'.format(name))
        return None
    
    @staticmethod
    def deactivate_lv2_const_optimization(ws, condition):
        print('INFO: Deactivating level 2 constant term optimization for specified pdfs')
        for component in ws.components():
            name = component.GetName()
            if (component.InheritsFrom(ROOT.RooAbsPdf.Class()) and condition(name)):
                component.setAttribute("NOCacheAndTrack")
                print('INFO: Deactivated level 2 constant term optimizatio for {}'.format(name))
            
    def initialize(self):
        if not os.path.exists(self.fname):
            raise FileNotFoundError('workspace file {} does not exist'.format(self.fname))
        print('Opening file: {}'.format(self.fname))
        file = ROOT.TFile(self.fname) 
        if (not file):
            raise RuntimeError("Something went wrong while loading the root file: {}".format(self.fname))
        # load workspace
        if self.ws_name is None:
            ws_names = [i.GetName() for i in file.GetListOfKeys() if i.GetClassName() == 'RooWorkspace']
            if not ws_names:
                raise RuntimeError("No workspaces found in the root file: {}".fomat(fname))
            if len(ws_names) > 1:
                print("WARNING: Found multiple workspace instances from the root file: {}. Available workspaces"
                      " are \"{}\". Will choose the first one by default".format(fname, ','.join(ws_names)))
            self.ws_name = ws_names[0]

        ws = file.Get(self.ws_name)
        if not ws:
            raise RuntimeError('failed to load workspace "{}"'.format(self.ws_name))
        print('INFO: Loaded workspace "{}"'.format(self.ws_name))
        # load model config
        if self.mc_name is None:
            mc_names = [i.GetName() for i in ws.allGenericObjects() if 'ModelConfig' in i.ClassName()]
            if not mc_names:
                raise RuntimeError("no ModelConfig object found in the workspace: {}".fomat(ws_name))
            if len(mc_names) > 1:
                print("WARNING: Found multiple ModelConfig instances from the workspace: {}. "
                      "Available ModelConfigs are \"{}\". "
                      "Will choose the first one by default".format(ws_name, ','.join(mc_names)))
            self.mc_name = mc_names[0]
        model_config = ws.obj(self.mc_name)
        if not model_config:
            raise RuntimeError('failed to load model config "{}"'.format(self.mc_name))
        print('INFO: Loaded model config "{}"'.format(self.mc_name))
            
        # modify interpolation code
        if self.interpolation_code != -1:
            self.modify_interp_codes(ws, self.interpolation_code,
                                     classes=[ROOT.RooStats.HistFactory.FlexibleInterpVar, ROOT.PiecewiseInterpolation])
        
        # activate binned likelihood
        if self.binned_likelihood:
            self.activate_binned_likelihood(ws)
        
        # set main measurement
        if self.tag_as_measurement:
            self.set_measurement(ws, condition=lambda name: name.startswith(self.tag_as_measurement))
                          
        # deactivate level 2 constant term optimization
            self.deactivate_lv2_const_optimization(ws, 
                condition=lambda name: (name.endswith('_mm') and 'mumu_atlas' in name))

        # load pdf
        pdf = model_config.GetPdf()
        if not pdf:
            raise RuntimeError('Failed to load pdf')
        print('INFO: Loaded model pdf "{}" from model config'.format(pdf.GetName()))
             
        # load dataset
        data = ws.data(self.data_name)
        if not data:
            raise RuntimeError('Failed to load dataset')
        print('INFO: Loaded dataset "{}" from workspace'.format(data.GetName()))
                
        # load nuisance parameters
        nuisance_parameters = model_config.GetNuisanceParameters()
        if not nuisance_parameters:
            raise RuntimeError('Failed to load nuisance parameters')
        print('INFO: Loaded nuisance parameters from model config')
                
        # Load global observables
        global_observables = model_config.GetGlobalObservables()
        if not global_observables:
            raise RuntimeError('Failed to load global observables')          
        print('INFO: Loaded global observables from model config')                  
    
        # Load POIs
        pois = model_config.GetParametersOfInterest()
        if not pois:
            raise RuntimeError('Failed to load parameters of interest')
        print('INFO: Loaded parameters of interest from model config')
                                  
        # Load observables
        observables = model_config.GetObservables()
        if not observables:
            raise RuntimeError('Failed to load observables')     
        print('INFO: Loaded observables from model config')
        
        self._file                = file
        self._workspace           = ws
        self._model_config        = model_config
        self._pdf                 = pdf
        self._data                = data
        self._nuisance_parameters = nuisance_parameters
        self._global_observables  = global_observables
        self._pois                = pois
        self._observables         = observables
                          
        # Load snapshots
        if (self.snapshot_name) and self.workspace.getSnapshot(self.snapshot_name):
            self._workspace.loadSnapshot(self.snapshot_name)
            print('INFO: Loaded snapshot "{}"'.format(self.snapshot_name))
        return None
                
    @staticmethod
    def _fix_parameters(source:"ROOT.RooArgSet", param_expr=None, param_str='parameter'):
        '''
            source: parameters instance
            param_expr: 
        '''            
        param_dict = ExtendedModel.parse_param_expr(param_expr)
        return ExtendedModel._set_parameters(source, param_dict, mode='fix', param_str=param_str)           
    
    @staticmethod
    def _profile_parameters(source:"ROOT.RooArgSet", param_expr=None, param_str='parameter'):
        '''
            source: parameters instance
            param_expr: 
        '''                          
        param_dict = ExtendedModel.parse_param_expr(param_expr)
        return ExtendedModel._set_parameters(source, param_dict, mode='free', param_str=param_str)   
    
    def fix_parameters(self, param_expr=None):
        return self._fix_parameters(self.workspace.allVars(), param_expr=param_expr,
                                    param_str='parameter')
    
    def profile_parameters(self, param_expr=None):
        profiled_parameters = self._profile_parameters(self.workspace.allVars(), param_expr=param_expr,
                                                       param_str='parameter') 
        if not profiled_parameters:
            print('Info: No parameters are profiled.')
        return profiled_parameters 
    
    def fix_nuisance_parameters(self, param_expr=None):
        return self._fix_parameters(self.nuisance_parameters, param_expr=param_expr,
                                    param_str='nuisance parameter')
                          
    def fix_parameters_of_interest(self, param_expr=None):
        return self._fix_parameters(self.pois, param_expr=param_expr, param_str='parameter of interest')

    def profile_parameters_of_interest(self, param_expr=None):
        return self._profile_parameters(self.pois, param_expr=param_expr, param_str='parameter of interest')
    
    @staticmethod
    def _set_parameters(source:"ROOT.RooArgSet", param_dict, mode=None, param_str='parameter'):
        set_parameters = []
        available_parameters = [param.GetName() for param in source]
        for name in param_dict:
            selected_params = [param for param in available_parameters if fnmatch.fnmatch(param, name)]
            if not selected_params:
                print('WARNING: Parameter "{}" does not exist. No modification will be made.'.format(name))
            for param_name in selected_params:
                ExtendedModel._set_parameter(source[param_name], param_dict[name], mode=mode, param_str=param_str)
                set_parameters.append(source[param_name])

        return set_parameters
    
    @staticmethod
    def _set_parameter(param, value, mode=None, param_str='parameter'):
        name = param.GetName()
        old_value = param.getVal()
        new_value = old_value
        if isinstance(value, (float, int)):
            new_value = value
        elif isinstance(value, (list, tuple)):
            if len(value) == 3:
                new_value = value[0]
                v_min, v_max = value[1], value[2]
            elif len(value) == 2:
                v_min, v_max = value[0], value[1]
            else:
                raise ValueError('invalid expression for profiling parameter: {}'.format(value))
            # set range
            if (v_min is not None) and (v_max is not None):
                if (new_value < v_min) or (new_value > v_max):
                    new_value = (v_min + v_max)/2
                param.setRange(v_min, v_max)
                print('INFO: Set {} "{}" range to ({},{})'.format(param_str, name, v_min, v_max))
            elif (v_min is not None):
                if (new_value < v_min):
                    new_value = v_min
                # lower bound is zero, if original value is negative, will flip to positive value
                if (v_min == 0) and (old_value < 0):
                    new_value = abs(old_value)
                param.setMin(v_min)
                print('INFO: Set {} "{}" min value to ({},{})'.format(param_str, name, v_min))
            elif (v_max is not None):
                if (new_value > v_max):
                    new_value = v_max
                # upper bound is zero, if original value is positive, will flip to negative value
                if (v_max == 0) and (old_value > 0):
                    new_value = -abs(old_value)                    
                param.setMax(v_max)
                print('INFO: Set {} "{}" max value to ({},{})'.format(param_str, name, v_max))
        if new_value != old_value:
            param.setVal(new_value)              
            print('INFO: Set {} "{}" value to {}'.format(param_str, name, new_value))
        if mode=='fix':
            param.setConstant(1)
            print('INFO: Fixed {} "{}" at value {}'.format(param_str, name, param.getVal()))
        elif mode=='free':
            param.setConstant(0)
            print('INFO: "{}" = [{}, {}]'.format(name, param.getMin(), param.getMax()))
        return None

    @staticmethod
    def set_parameter_defaults(source:"ROOT.RooArgSet", value=None, error=None, constant=None,
                               remove_range=None, target:List[str]=None):

        for param in source:
            if (not target) or (param.GetName() in target):
                if remove_range:
                    param.removeRange()            
                if value is not None:
                    param.setVal(value)
                if error is not None:
                    param.setError(error)
                if constant is not None:
                    param.setConstant(constant)
        return None
    
    @staticmethod
    def parse_param_expr(param_expr):
        param_dict = {}
        # if parameter expression is not empty string or None
        if param_expr: 
            if isinstance(param_expr, str):
                param_dict = ExtendedModel.parse_param_str(param_expr)
            elif isinstance(param_expr, dict):
                param_dict = param_dict
            else:
                raise ValueError('invalid format for parameter expression: {}'.format(param_expr))
        elif param_expr is None:
        # if param_expr is None, all parameters will be parsed as None by default
            param_dict = {param.GetName():None for param in source}
        return param_dict

    @staticmethod
    def parse_param_str(param_str):
        '''
        Example: "param_1,param_2=0.5,param_3=-1,param_4=1,param_5=0:100,param_6=:100,param_7=0:"
        '''
        param_str = param_str.replace(' ', '')
        param_list = param_str.split(',')
        param_dict = {}
        for param_expr in param_list:
            expr = param_expr.split('=')
            # case only parameter name is given
            if len(expr) == 1:
                param_dict[expr[0]] = None
            # case both parameter name and value is given
            elif len(expr) == 2:
                param_name = expr[0]
                param_value = expr[1]
                # range like expression
                if ':' in param_value:
                    param_range = param_value.split(':')
                    if len(param_range) != 2:
                        raise ValueError('invalid parameter range: {}'.format(param_value))
                    param_min = float(param_range[0]) if param_range[0].isnumeric() else None
                    param_max = float(param_range[1]) if param_range[1].isnumeric() else None
                    param_dict[param_name] = [param_min, param_max]
                elif is_integer(param_value):
                    param_dict[param_name] = int(param_value)
                else:
                    param_dict[param_name] = float(param_value)
            else:
                raise ValueError('invalid parameter expression: {}'.format(param))
        return param_dict
    
    @staticmethod
    def find_unique_prod_components(root_pdf, components, recursion_count=0):
        if (recursion_count > 50):
            raise RuntimeError('find_unique_prod_components detected infinite loop')
        pdf_list = root_pdf.pdfList()
        if pdf_list.getSize() == 1:
            components.add(pdf_list)
            #print('ProdPdf {} is fundamental'.format(pdf_list.at(0).GetName()))
        else:
            for pdf in pdf_list:
                if pdf.ClassName() != 'RooProdPdf':
                    #print('Pdf {} is no RooProdPdf. Adding it.')
                    components.add(pdf)
                    continue
                find_unique_prod_components(pdf, components, recursion_count+1)
    
    def get_all_constraints(self):
        all_constraints = ROOT.RooArgSet()
        cache_name = "CACHE_CONSTR_OF_PDF_{}_FOR_OBS_{}".format(self.pdf.GetName(), 
                     ROOT.RooNameSet(self.data.get()).content())                 
        constr = self.workspace.set(cache_name)
        if constr:
            # retrieve constrains from cache     
            all_constraints.add(constr)
        else:
            # load information needed to determine attributes from ModelConfig 
            obs = deepcopy(self.observables)
            nuis = deepcopy(self.nuisance_parameters)
            all_constraints = self.pdf.getAllConstraints(obs, nuis, ROOT.kFALSE)
            
        # take care of the case where we have a product of constraint terms
        temp_all_constraints = ROOT.RooArgSet(all_constraints.GetName())
        for constraint in all_constraints:
            if constraint.IsA() == ROOT.RooProdPdf.Class():
                buffer = ROOT.RooArgSet()
                ExtendedModel.find_unique_prod_components(constraint, buffer)
                temp_all_constraints.add(buffer)
            else:
                temp_all_constraints.add(constraint)
        return temp_all_constraints
    
    def inspect_constrained_nuisance_parameter(self, nuis, constraints):
        nuis_name = nuis.GetName()
        print('INFO: On nuisance parameter {}'.format(nuis_name))
        nuip_nom = 0.0
        prefit_variation = 1.0
        found_constraint = ROOT.kFALSE
        found_gaussian_constraint = ROOT.kFALSE
        constraint_type = None
        for constraint in constraints:
            constr_name = constraint.GetName()
            if constraint.dependsOn(nuis):
                found_constraint = ROOT.kTRUE
                constraint_type = 'unknown'
                # Loop over global observables to match nuisance parameter and
                # global observable in case of a constrained nuisance parameter
                found_global_observable = ROOT.kFALSE
                for glob_obs in self.global_observables:
                    if constraint.dependsOn(glob_obs):
                        found_global_observable = ROOT.kTRUE
                        # find constraint width in case of a Gaussian
                        if constraint.IsA() == ROOT.RooGaussian.Class():
                            found_gaussian_constraint = ROOT.kTRUE
                            constraint_type = 'gaus'
                            old_sigma_value = 1.0
                            found_sigma = ROOT.kFALSE
                            for server in constraint.servers():
                                if (server != glob_obs) and (server != nuis):
                                    old_sigma_value = server.getVal()
                                    found_sigma = ROOT.kTRUE
                            if math.isclose(old_sigma_value, 1.0, abs_tol=0.001):
                                old_sigma_value = 1.0
                            if not found_sigma:
                                print('INFO: Sigma for pdf {} not found. Uisng 1.0.'.format(constr_name))
                            else:
                                print('INFO: Uisng {} for sigma of pdf {}'.format(old_sigma_value, constr_name))

                            prefit_variation = old_sigma_value
                        elif constraint.IsA() == ROOT.RooPoisson.Class():
                            constraint_type = 'pois'
                            tau = glob_obs.getVal()
                            print('INFO: Found tau {} of pdf'.format(constr_name))
                            prefit_variation = 1. / math.sqrt(tau)
                            print('INFO: Prefit variation is {}'.format(prefit_variation))
                            nuip_nom = 1.0
                            print("INFO: Assume that {} is nominal value of the nuisance parameter".format(nuip_nom))
        return prefit_variation, constraint_type, nuip_nom
        
    def set_initial_errors(self, source:Optional["ROOT.RooArgSet"]=None):
        if not source:
            source = self.nuisance_parameters
    
        all_constraints = self.get_all_constraints()
        for nuis in source:
            nuis_name = nuis.GetName()
            prefit_variation, constraint_type, _ = self.inspect_constrained_nuisance_parameter(nuis, all_constraints)
            if constraint_type=='gaus':
                print('INFO: Changing error of {} from {} to {}'.format(nuis_name, nuis.getError(), prefit_variation))
                nuis.setError(prefit_variation)
                nuis.removeRange()    
        return None
    @staticmethod
    def to_dataframe(args):
        import pandas as pd
        data = [{'Name':i.GetName(), 'Value':i.getVal(), "Constant":i.isConstant(), "Min":i.getMin(), "Max":i.getMax()} for i in args]
        df = pandas.DataFrame(data)
        return df
    
    @staticmethod
    def load_ws(fname:str, ws_name:Optional[str]=None, mc_name:Optional[str]=None):
        if not os.path.exists(fname):
            raise FileNotFoundError('workspace file {} does not exist'.format(fname))
        file = ROOT.TFile(fname)
        if (not file):
            raise RuntimeError("Something went wrong while loading the root file: {}".format(fname))        
        # load workspace
        if ws_name is None:
            ws_names = [i.GetName() for i in file.GetListOfKeys() if i.GetClassName() == 'RooWorkspace']
            if not ws_names:
                raise RuntimeError("No workspaces found in the root file: {}".fomat(fname))
            if len(ws_names) > 1:
                print("WARNING: Found multiple workspace instances from the root file: {}. Available workspaces"
                      " are \"{}\". Will choose the first one by default".format(fname, ','.join(ws_names)))
            ws_name = ws_names[0]
        ws = file.Get(ws_name)
        if not ws:
            raise RuntimeError('Failed to load workspace: "{}"'.format(ws_name))
        # load model config
        if mc_name is None:
            mc_names = [i.GetName() for i in ws.allGenericObjects() if 'ModelConfig' in i.ClassName()]
            if not mc_names:
                raise RuntimeError("no ModelConfig object found in the workspace: {}".fomat(ws_name))
            if len(mc_names) > 1:
                print("WARNING: Found multiple ModelConfig instances from the workspace: {}. "
                      "Available ModelConfigs are \"{}\". "
                      "Will choose the first one by default".format(ws_name, ','.join(mc_names)))
            mc_name = mc_names[0]     
        mc = ws.obj(mc_name)
        if not mc:
            raise RuntimeError('Failed to load model config "{}"'.format(mc_name))
        return file, ws, mc
    
    @staticmethod
    def get_nuisance_parameter_names(fname:str, ws_name:Optional[str]=None, mc_name:Optional[str]=None):
        ExtendedModel.load_extension()
        file, ws, mc = ExtendedModel.load_ws(fname, ws_name, mc_name)
        nuisance_parameters = mc.GetNuisanceParameters()
        if not nuisance_parameters:
            raise RuntimeError('Failed to load nuisance parameters')
        return [nuis.GetName() for nuis in nuisance_parameters]
    
    @staticmethod
    def get_poi_names(fname:str, ws_name:Optional[str]=None, mc_name:Optional[str]=None):
        ExtendedModel.load_extension()
        file, ws, mc = ExtendedModel.load_ws(fname, ws_name, mc_name)
        pois = mc.GetParametersOfInterest()
        if not pois:
            raise RuntimeError('Failed to load parameters of interest')        
        return [poi.GetName() for poi in pois]

    @staticmethod
    def get_dataset_names(fname:str, ws_name:Optional[str]=None, mc_name:Optional[str]=None):
        ExtendedModel.load_extension()
        file, ws, mc = ExtendedModel.load_ws(fname, ws_name, mc_name)
        datasets = ws.allData()
        if not datasets:
            raise RuntimeError('Failed to load datasets')
        return [dataset.GetName() for dataset in datasets]