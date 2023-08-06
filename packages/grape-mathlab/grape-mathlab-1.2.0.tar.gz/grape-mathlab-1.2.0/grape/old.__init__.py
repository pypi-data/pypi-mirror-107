"""
GRAPE (GRAph Parallel Environment) is a Python package that takes advantage of
Graph Theory into a High Performance Computing (HPC) environment to develope a
screening tool aimed at studying the effect of different kinds of perturbations
in interconnected systems, such as indsutrial plants.
"""

#__all__ = [] # TBD

def get_current_year():
    """ Return current year """
    from datetime import datetime
    return datetime.now().year

__project__ = 'GRAPE'
__title__ = "grape"
__author__ = "Aurora Maurizio, Martina Teruzzi, Nicola Demo"
__copyright__ = "Copyright 2019-{}, GRAPE contributors".format(get_current_year())
__license__ = "MIT"
__version__ = "1.2.0"
__mail__ = 'auroramaurizio1@gmail.com, teruzzi.martina@gmail.com, demo.nicola@gmail.com'
__maintainer__ = __author__
__status__ = "Alpha"

from grape.general_graph import GeneralGraph
from grape.parallel_general_graph import ParallelGeneralGraph
from grape.fault_diagnosis import FaultDiagnosis
