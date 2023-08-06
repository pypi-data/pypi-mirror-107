import pandas as pd
import numpy as np
import scipy.stats as stats
import bluebelt.helpers.subsets

import bluebelt.datetime.dt

import bluebelt.statistics.std

import bluebelt.analysis.patterns
import bluebelt.statistics.hypothesis_testing

from bluebelt.core.exceptions import *

@pd.api.extensions.register_dataframe_accessor('blue')
class DataFrameToolkit():
    def __init__(self, pandas_obj):
        self._obj = pandas_obj
        self.dt = self.dt(self._obj)
        self.std = self.std(self._obj)
        self.patterns = self.patterns(self._obj)
        self.statistics = self.statistics(self._obj)
        self.test = self.test(self._obj)

    # first level functions

    # subsets
    def subset(self, inverse=False, **kwargs):
        return bluebelt.helpers.subsets.subset(self._obj, inverse=inverse, **kwargs)

        
    class dt():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj
    
        # bluebelt.datetime.dt
        def year(self, column=None, **kwargs):
            return bluebelt.datetime.dt.year(self._obj[column], **kwargs)

        def quarter(self, column=None, **kwargs):
            return bluebelt.datetime.dt.year(self._obj[column], **kwargs)

        def month(self, column=None, **kwargs):
            return bluebelt.datetime.dt.quarter(self._obj[column], **kwargs)

        def day(self, column=None, **kwargs):
            return bluebelt.datetime.dt.day(self._obj[column], **kwargs)

        def weekday(self, column=None, **kwargs):
            return bluebelt.datetime.dt.weekday(self._obj[column], **kwargs)
        
        def weekday_name(self, column=None, **kwargs):
            return bluebelt.datetime.dt.weekday_name(self._obj[column], **kwargs)

        def is_holiday(self, column=None, **kwargs):
            return bluebelt.datetime.dt.is_holiday(self._obj[column], **kwargs)

        def is_weekend(self, column=None, **kwargs):
            return bluebelt.datetime.dt.is_weekend(self._obj[column], **kwargs)
        
        def iso_year(self, column=None, **kwargs):
            return bluebelt.datetime.dt.iso_year(self._obj[column], **kwargs)

        def iso_week(self, column=None, **kwargs):
            return bluebelt.datetime.dt.iso_week(self._obj[column], **kwargs)
        
        def week(self, column=None, **kwargs):
            return bluebelt.datetime.dt.week(self._obj[column], **kwargs)
        
        def date_from_weeknumber(self, year=None, week=None, **kwargs):
            return bluebelt.datetime.dt.date_from_weeknumber(self._obj, year=year, week=week, **kwargs)

        def add(self, column=None, prefix='_', **kwargs):
            self._obj.loc[:,f'{prefix}year'] = bluebelt.datetime.dt.year(self._obj[column])
            self._obj.loc[:,f'{prefix}quarter'] = bluebelt.datetime.dt.quarter(self._obj[column])
            self._obj.loc[:,f'{prefix}month'] = bluebelt.datetime.dt.month(self._obj[column])
            self._obj.loc[:,f'{prefix}day'] = bluebelt.datetime.dt.day(self._obj[column])
            self._obj.loc[:,f'{prefix}weekday'] = bluebelt.datetime.dt.weekday(self._obj[column])
            self._obj.loc[:,f'{prefix}day_name'] = bluebelt.datetime.dt.day_name(self._obj[column])
            self._obj.loc[:,f'{prefix}is_holiday'] = bluebelt.datetime.dt.is_holiday(self._obj[column])
            self._obj.loc[:,f'{prefix}is_weekend'] = bluebelt.datetime.dt.is_weekend(self._obj[column])
            self._obj.loc[:,f'{prefix}iso_year'] = bluebelt.datetime.dt.iso_year(self._obj[column])
            self._obj.loc[:,f'{prefix}iso_week'] = bluebelt.datetime.dt.iso_week(self._obj[column])
            return self._obj



    class std():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        # standard deviation
        def pooled_std(self, columns=None, **kwargs):
            return bluebelt.statistics.std.pooled_std(self._obj, columns=columns)

    class patterns():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        # patterns
        def anomalies(self, values=None, pattern=None):
            return bluebelt.analysis.patterns.anomalies(self._obj, values=values, pattern=pattern)

    class statistics():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        def correlation(self, columns=None, confidence=0.95, **kwargs):
            return bluebelt.statistics.basic_statistics.Correlation(self._obj, columns=columns, confidence=confidence)

        
    class test():
        def __init__(self, pandas_obj):
            self._obj = pandas_obj

        def normal_distribution(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.NormalDistribution(self._obj, columns=columns, alpha=alpha, **kwargs)
        
        def dagostino_pearson(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.DAgostinoPearson(self._obj, columns=columns, alpha=alpha, **kwargs)
        
        # index
        @property
        def index(self):
            return bluebelt.statistics.hypothesis_testing.index()

        # hypothesis testing
        
        def two_sample_t(self, columns=None, related=False, confidence=0.95, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.TwoSampleT(self._obj, columns=columns, related=related, confidence=confidence, alpha=alpha, **kwargs)
        
        def wilcoxon(self, popmean=None, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Wilcoxon(self._obj, columns=columns, alpha=alpha, **kwargs)
        
        def equal_means(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.EqualMeans(self._obj, columns=columns, alpha=alpha, **kwargs)

        def anova(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Anova(self._obj, columns=columns, alpha=alpha, **kwargs)

        def kruskal(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.KruskalWallis(self._obj, columns=columns, alpha=alpha, **kwargs)

        kruskal_wallis = kruskal

        def mann_whitney(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.MannWhitney(self._obj, columns=columns, alpha=alpha, **kwargs)
        
        def levene(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Levene(self._obj, columns=columns, alpha=alpha, **kwargs)
        
        def bartlett(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.Bartlett(self._obj, columns=columns, alpha=alpha, **kwargs)
        
        def f_test(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.FTest(self._obj, columns=columns, alpha=alpha, **kwargs)
        
        def equal_variance(self, columns=None, alpha=0.05, **kwargs):
            return bluebelt.statistics.hypothesis_testing.EqualVariance(self._obj, columns=columns, alpha=alpha, **kwargs)
        
        equal_var = equal_variance