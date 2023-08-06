import pandas as pd
import numpy as np
import scipy.stats as stats


import bluebelt.datetime.dt

import bluebelt.statistics.std

import bluebelt.analysis.ci
import bluebelt.statistics.hypothesis_testing
import bluebelt.analysis.patterns
import bluebelt.analysis.datetime
import bluebelt.analysis.graphs
import bluebelt.analysis.ppa

from bluebelt.core.exceptions import *


@pd.api.extensions.register_series_accessor('blue')
class SeriesToolkit():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self.std = self.std(self._obj)
        self.patterns = self.patterns(self._obj)
        self.datetime = self.datetime(self._obj)
        self.graphs = self.graphs(self._obj)
        self.statistics = self.statistics(self._obj)
        self.test = self.test(self._obj)
        self.ppa = self.ppa(self._obj)
    
    def summary(self, **kwargs):
        return bluebelt.analysis.ppa.Summary(self._obj, **kwargs)
    
    class std():

        def __init__(self, pandas_obj):
            self._obj = pandas_obj
                
        # standard deviation
        def std_within(self, **kwargs):
            return bluebelt.statistics.std.std_within(self._obj, **kwargs)


        def average_moving_range(self, observations=2, **kwargs):
            return bluebelt.statistics.std.average_moving_range(self._obj, observations=observations, **kwargs)

        def median_moving_range(self, observations=2, **kwargs):
            return bluebelt.statistics.std.median_moving_range(self._obj, observations=observations, **kwargs)

        def sqrt_of_mssd(self, **kwargs):
            return bluebelt.statistics.std.sqrt_of_mssd(self._obj, **kwargs)

        
    class patterns():

        def __init__(self, pandas_obj):
            self._obj = pandas_obj
                
        # patterns
        def polynomial(self, **kwargs):
            return bluebelt.analysis.patterns.Polynomial(self._obj, **kwargs)

        def periodical(self, **kwargs):
            return bluebelt.analysis.patterns.Periodical(self._obj, **kwargs)
    
    class datetime():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        # week day
        def week_day(self, **kwargs):
            return bluebelt.analysis.datetime.WeekDay(self._obj, **kwargs)

        weekday = week_day

        # day of the month
        def day(self, **kwargs):
            return bluebelt.analysis.datetime.Day(self._obj, **kwargs)

        # week of the year
        def week(self, **kwargs):
            return bluebelt.analysis.datetime.Week(self._obj, **kwargs)

        # month of the year
        def month(self, **kwargs):
            return bluebelt.analysis.datetime.Month(self._obj, **kwargs)

        # year
        def year(self, **kwargs):
            return bluebelt.analysis.datetime.Year(self._obj, **kwargs) 

    class graphs():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj
        
        # rolling std
        def rolling_std(self, **kwargs):
            return bluebelt.analysis.graphs.RollingStd(self._obj, **kwargs)

    class statistics():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        
    class test():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        # index
        @property
        def index(self):
            return bluebelt.statistics.hypothesis_testing.index()

        # hypothesis testing
        def normal_distribution(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.NormalDistribution(self._obj, alpha=alpha)
        
        def dagostino_pearson(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.DAgostinoPearson(self._obj, alpha=alpha)
        
        def anderson_darling(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.AndersonDarling(self._obj, alpha=alpha)
                
        def one_sample_t(self, popmean=None, confidence=0.95, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.OneSampleT(self._obj, popmean=popmean, confidence=confidence, alpha=alpha, **kwargs)

        def wilcoxon(self, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Wilcoxon(self._obj, alpha=alpha, **kwargs)
        
    class ppa():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        def summary(self, **kwargs):
            return bluebelt.analysis.ppa.Summary(self._obj, **kwargs)
        
        def control_chart(self, **kwargs):
            return bluebelt.analysis.ppa.ControlChart(self._obj, **kwargs)
            
        def run_chart(self, alpha=0.05, **kwargs):
            return bluebelt.analysis.ppa.RunChart(self._obj, alpha=alpha, **kwargs)

        def process_capability(self, **kwargs):
            '''
            Display the process capability

            target = None   float: target value for the process
            usl = None      float: upper specification limit (usl and ub cannot be specified both)
            ub = None       float: upper bound (usl and ub cannot be specified both)
            lsl = None      float: lower specification limit
            lb = None       float: lower bound (lsl and lb cannot be specified both)
            tolerance = 6   float: sigma tolerance of the process
            '''
            return bluebelt.analysis.ppa.ProcessCapability(self._obj, **kwargs)
        
        