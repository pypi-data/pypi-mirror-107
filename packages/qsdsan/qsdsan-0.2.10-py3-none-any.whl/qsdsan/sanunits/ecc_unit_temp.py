#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
QSDsan: Quantitative Sustainable Design for sanitation and resource recovery systems

This module is developed by:
    Smiti Mittal <smitimittal@gmail.com>
    Yalin Li <zoe.yalin.li@gmail.com>
    Anna Kogler

This module is under the University of Illinois/NCSA Open Source License.
Please refer to https://github.com/QSD-Group/QSDsan/blob/master/LICENSE.txt
for license details.
'''

# %%
import math
#!!! Change this to relative importing when compiled into qsdsan
from qsdsan import Equipment, SanUnit, Component, WasteStream
# from .. import SanUnit, Equipment # relative importing

isinstance = isinstance

# __all__ = ('Electrode', 'ElectroChemCell')

# %%

# Be sure to include documentation and examples
class Electrode(Equipment):
    '''
    Electrodes to be used in an electrochemical cell.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    N : int
        Number of units of the given electrode.
    electrode_type : str
        Type of the electrode, can only be "anode" or "cathode".
    material: str
        Material of the electrode.
    unit_cost: float
        Unit cost of the electrode, will use default cost (if available)
        if not provided.
    surface_area : float
        Surface area of the electrode in m2.

    See Also
    --------
    :class:`ElectroChemCell`

    '''

    # Include all attributes (no properties) in addition to the ones in the
    # parent `Equipment` class
    # Using __slots__ can improve computational efficiency when the class does not
    # have many attributes
    __slots__ = ('_type', '_material', '_N', 'unit_cost', 'surface_area')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units={}, # if no value, then should be an empty dict
                 F_BM=1.,
                 lifetime=10000, lifetime_unit='hr', N=0,
                 electrode_type='anode', # note that I prefer not to use 'type' because it's a builtin function
                 material='graphite', unit_cost=0.1, surface_area=1):
        Equipment.__init__(self=self, name=name, design_units=design_units, F_BM=F_BM, lifetime=lifetime, lifetime_unit=lifetime_unit)
        self.N = N
        self.electrode_type = electrode_type
        self.unit_cost = unit_cost
        self.material = material
        self.surface_area = surface_area

    # All subclasses of `Equipment` must have a `_design` and a `_cost` method
    def _design(self):
        design = {
            f'Type of electrode' : self.electrode_type,
            f'Number of {self.electrode_type}': self.N,
            f'Material of {self.electrode_type}': self.material,
            f'Surface area of {self.electrode_type}': self.surface_area
            }
        self.design_units = {f'Surface area of {self.electrode_type}': 'm2'}
        return design

    # All subclasses of `Equipment` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N

    # You can use property to add checks
    @property
    def N(self):
        '''[str] Number of units of the electrode.'''
        return self._N
    @N.setter
    def N(self, i):
        try:
            self._N = int(i)
        except:
            raise ValueError(f'N must be an integer')

    @property
    def electrode_type(self):
        '''[str] Type of the electrode, either "anode" or "cathode".'''
        return self._type
    @electrode_type.setter
    def electrode_type(self, i):
        if i.lower() in ('anode', 'cathode'):
            self._type = i
        else:
            raise ValueError(f'Electrode can only be "anode" or "cathode", not {i}.')

    @property
    def material(self):
        '''[str] Material of the electrode.'''
        return self._material
    @material.setter
    def material(self, i):
        material = i.lower()
        if material == 'graphite':
            # You can have some default unit cost based on the material,
            # I'm just making up numbers
            # But be careful that by doing this, you might overwriter users' input
            if not self.unit_cost:
                self.unit_cost = 50
        self._material = material

class Membrane(Equipment):
    '''
    Membranes to be used in an electrochemical cell.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    N : int
        Number of units of the given membrane.
    material: str
        Material of the membrane.
    unit_cost: float
        Unit cost of the membrane per m2, will use default cost (if available)
        if not provided.
    surface_area : float
        Surface area of the membrane in m2.

    See Also
    --------
    :class:`ElectroChemCell`

    '''
    __slots__ = ('_N', 'name', 'unit_cost', 'material', 'surface_area')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units={},
                 F_BM=1., lifetime=10000, lifetime_unit='hr', N=0,
                 material='polypropylene', unit_cost=0.1, surface_area=1):
        Equipment.__init__(self=self, name=name, design_units=design_units, F_BM=F_BM, lifetime=lifetime, lifetime_unit=lifetime_unit)
        self.name = name
        self.N = N
        self.unit_cost = unit_cost
        self.material = material
        self.surface_area = surface_area

    # All subclasses of `Membrane` must have a `_design` and a `_cost` method
    def _design(self):
        design = {
            f'Number of {self.name}': self.N,
            f'Material of {self.name}': self.material,
            f'Surface area of {self.name}': self.surface_area
            }
        self.design_units = {f'Surface area of {self.name}': 'm2'}
        return design

    # All subclasses of `Membrane` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N*self.surface_area

    # You can use property to add checks
    @property
    def N(self):
        '''[str] Number of units of the electrode.'''
        return self._N
    @N.setter
    def N(self, i):
        try:
            self._N = int(i)
        except:
            raise ValueError(f'N must be an integer')

class Column(Equipment):
    '''
    Columns to be used in an electrochemical cell.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    N : int
        Number of units of the given column.
    material: str
        Material of the column.
    unit_cost: float
        Unit cost of the column per m2, will use default cost (if available)
        if not provided.
    surface_area : float
        Surface area of the column in m2.

    See Also
    --------
    :class:`ElectroChemCell`

    '''

    __slots__ = ('_N', 'name', 'unit_cost', 'material', 'surface_area')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units={},
                 F_BM=1., lifetime=10000, lifetime_unit='hr', N=0,
                 material='resin', unit_cost=0.1, surface_area=1):
        Equipment.__init__(self=self, name=name, design_units=design_units, F_BM=F_BM, lifetime=lifetime, lifetime_unit=lifetime_unit)
        self.name = name
        self.N = N
        self.unit_cost = unit_cost
        self.material = material
        self.surface_area = surface_area

    # All subclasses of `Column` must have a `_design` and a `_cost` method
    def _design(self):
        design = {
            f'Number of {self.name}': self.N,
            f'Material of {self.name}': self.material,
            f'Surface area of {self.name}': self.surface_area
            }
        self.design_units = {f'Surface area of {self.name}': 'm2'}
        return design

    # All subclasses of `Column` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N*self.surface_area

    # You can use property to add checks
    @property
    def N(self):
        '''[str] Number of units of the electrode.'''
        return self._N
    @N.setter
    def N(self, i):
        try:
            self._N = int(i)
        except:
            raise ValueError(f'N must be an integer')

class Machine(Equipment):
    '''
    Supplementary machines to be used in an electrochemical process.
    Refer to the example in :class:`ElectroChemCell` for how to use this class.

    Parameters
    ----------
    N : int
        Number of units of the given machine.
    unit_cost: float
        Unit cost of the machine

    See Also
    --------
    :class:`ElectroChemCell`

    '''
    __slots__ = ('_N', 'name', 'unit_cost')

    def __init__(self, name=None, # when left as None, will be the same as the class name
                 design_units={},
                 F_BM=1., lifetime=10000, lifetime_unit='hr', N=0,
                 unit_cost=0.1):
        Equipment.__init__(self=self, name=name, design_units=design_units, F_BM=F_BM, lifetime=lifetime, lifetime_unit=lifetime_unit)
        self.name = name
        self.N = N
        self.unit_cost = unit_cost

    # All subclasses of `Machine` must have a `_design` and a `_cost` method
    def _design(self):
        design = {
            f'Number of {self.name}': self.N,
            }
        return design

    # All subclasses of `Membrane` must have a `_cost` method, which returns the
    # purchase cost of this equipment
    def _cost(self):
        return self.unit_cost*self.N

    # You can use property to add checks
    @property
    def N(self):
        '''[str] Number of units of the electrode.'''
        return self._N
    @N.setter
    def N(self, i):
        try:
            self._N = int(i)
        except:
            raise ValueError(f'N must be an integer')

# =============================================================================
# Then we can construct the unit with the different equipment
# =============================================================================

#!!! Note `Electrode` and `ElectroChemCell` has not been include in `qsdsan` now,
# so to actual run the example below, first run this script, then change
# `qs.sanunits.Electrode` to `Electrode` and `qs.sanunits.ElectroChemCell` to `ElectroChemCell`

class ElectroChemCell(SanUnit):

    '''

    Electrochemical cell for nutrient recovery.

    This unit has the following equipment:
        - :class:`Electrode`
        - :class: `Membrane`
        - :class: `Column`
        - :class: `Machine`

    Parameters
    ----------
    recovery : dict
        Keys refer to chemical component IDs. Values refer to recovery fractions (with 1 being 100%) for the respective chemicals.
    removal : dict
        Keys refer to chemical component IDs. Values refer to removal fractions (with 1 being 100%) for the respective chemicals.
    equipments : list
        List of Equipment objects part of the Electrochemical Cell.

    '''

    def __init__(self, ID='', ins=None, outs=(), recovery={'NH3':0.6}, removal={'NH3':0.2},
                 equipments=()):
        if isinstance(equipments, Equipment):
            equipments = (equipments,)
        SanUnit.__init__(self=self, ID=ID, ins=ins, outs=outs, equipments=equipments)
        self.recovery = recovery
        self.removal = removal

    _N_ins = 2
    _N_outs = 3

    def _run(self):
        influent, cleaner = self.ins
        recovered, removed, left = self.outs

        mixture = WasteStream()
        mixture.mix_from(self.ins)
        left = mixture.copy()

        for chemical, ratio in self.recovery.items():
            recovered.imass[chemical] = mixture.imass[chemical]*ratio
            left.imass[chemical] = left.imass[chemical]*(1-ratio)

        for chemical, ratio in self.removal.items():
            removed.imass[chemical] = mixture.imass[chemical]*ratio
            left.imass[chemical] = left.imass[chemical]*(1-ratio)


    def _design(self):
        self.add_equipment_design()

    def _cost(self):
        self.add_equipment_cost()

print('classes compiled')

#sample code
# Set components
import qsdsan as qs
kwargs = dict(particle_size='Soluble',
              degradability='Undegradable',
              organic=False)
H2O = qs.Component.from_chemical('H2O', phase='l', **kwargs)
NH3 = qs.Component.from_chemical('NH3', phase='g', **kwargs)
NH3.particle_size = 'Dissolved gas'
NH4OH = qs.Component.from_chemical('NH4OH', phase='l', **kwargs)
H2SO4 = qs.Component.from_chemical('H2SO4', phase='l', **kwargs)
AmmoniumSulfate = qs.Component.from_chemical('AmmoniumSulfate', phase='l',
                                             **kwargs)
CleaningAgent = qs.Component('CleaningAgent', MW=1, phase='l', **kwargs)
cmps = qs.Components((H2O, NH3, NH4OH, H2SO4, AmmoniumSulfate, CleaningAgent))
# Assuming all has the same molar volume as water for demonstration purpose
for cmp in cmps:
    cmp.copy_models_from(H2O, names=['V'])
    cmp.default()
qs.set_thermo(cmps)
# Set waste streams
influent = qs.WasteStream('influent', H2O=1000, NH4OH=50)
cleaning_agent = qs.WasteStream('cleaning_agent', price=5)
# Set anode and cathode
anode = Electrode(name='anode', electrode_type='anode',
                              material='graphite', surface_area=10)
cathode = Electrode(name='cathode', electrode_type='cathode',
                                material='carbon', surface_area=10, unit_cost=1)
membrane = Membrane(name='membrane', N=2,
            material='polyethylene', unit_cost=0.2, surface_area=1)
column = Column(name='column1', N=3,
            material='resin', unit_cost=2, surface_area=20)
machine = Machine(name='fan', N=1, unit_cost=3)
# Set the unit
U1 = ElectroChemCell('U1', ins=(influent, cleaning_agent),
                                outs=('recovered', 'removed', 'leftover'),
                                recovery={'NH4OH':0.6}, removal={'NH4OH':0.2},
                                equipments=(anode, cathode, membrane, column, machine))
# Simulate and look at the results
U1.simulate()
U1.diagram()
U1.show()
U1.results()