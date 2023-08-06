from collections import OrderedDict
from .decorators import not_implemented


class GKOutput(OrderedDict):

    def __init__(self,
                 pyro=None):

        """
        if pyro is None:
            print('Initialised empty GK Output')

            self['phi'] = None
            self['apar'] = None
            self['bpar'] = None
            self['time'] = None
            self['kx'] = None
            self['ky'] = None
            self['theta'] = None
            self['fluxes'] = None
            self['eigen_func'] = None

            self['growth_rate'] = None
            self['frequency'] = None

        else:

            self['kx'] = pyro.numerics['kx']
            self['ky'] = pyro.numerics['ky']
            self['theta'] = pyro.numerics['theta']
        """
        pass

    @not_implemented
    def read_grids(self):
        """
        reads in numerical grids
        """
        pass

    @not_implemented
    def read_output_data(self,
                    ):
        """
        reads in data not currently read in by default
        """
        pass

    @not_implemented
    def read_eigenvalues(self):
        """
        reads in eigenvalue
        """
        pass

    @not_implemented
    def read_eigenfunctions(self):
        """
        reads in eigenfunction
        """
        pass

    @not_implemented
    def read_fields(self):
        """
        reads in 3D fields
        """
        pass

    @not_implemented
    def read_fluxes(self):
        """
        reads in fluxes
        """
        pass

