import pandas as pd
import numpy as np
import numpy.polynomial.polynomial as poly
import scipy.stats as stats

import warnings

import matplotlib.pyplot as plt
#from matplotlib.ticker import FormatStrFormatter
import bluebelt.helpers.mpl_format as mpl_format

import bluebelt.styles

class Polynomial():
    
    """
    Find the polynomial of a series and project a bandwidth
    series: pandas.Series
    shape: int or tuple
        when an int is provided the polynomial is provided as n-th degree polynomial
        when a tuple is provided the function will find an optimised polynomial between first and second value of the tuple
        default value: (0, 6)
    validation: string
        validation type for shape tuple
        p_val: test for normal distribution of the residuals
        rsq: check for improvement of the rsq value
        default value: p_val
    threshold: float
        the threshold for normal distribution test or rsq improvement
        default value: 0.05
    confidence: float
        the bound confidence
        default value: 0.8
    outlier_sigma: float
        outliers are datapoints outside the outlier_sigma fraction
        default value: 2
    adjust: boolean
        adjust polynomial for outliers
        default value: True
    """

    def __init__(self, series, shape=(0, 6), validation='p_val', threshold=0.05, confidence=None, rolling=None, outlier_sigma=2, adjust=True, **kwargs):
        
        self.series = series
        self.shape = shape
        self.validation = validation
        self.threshold = threshold
        self.confidence = confidence
        self.rolling = rolling
        self.outlier_sigma = outlier_sigma
        self.adjust = adjust

        self.calculate()

    def calculate(self):
        
        # set pattern and residuals
        self.pattern, self.residuals, self.p_val, self.rsq = _poly_hand_granade(series=self.series, shape=self.shape, validation=self.validation, threshold=self.threshold)

        # set outliers
        self.outliers = pd.Series(data=np.where(self.residuals.abs() > self.residuals.std() * self.outlier_sigma, self.series, None), index=self.series.index)
        self.outliers_count = np.count_nonzero(self.outliers)

        # handle adjusted
        self.adjusted = self.series.loc[~self.outliers.notnull()]
        if self.adjust:
            # replace outliers with None values so they will be ignored by _poly_hand_granade and reset pattern
            values = pd.Series(data=np.where(self.outliers.notnull(), None, self.series).astype(np.float), index=self.series.index)
            self.pattern, self.residuals, self.p_val, self.rsq = _poly_hand_granade(series=values, shape=self.shape, validation=self.validation, threshold=self.threshold)
        
        # handle bounds
        # self.sigma_level = stats.norm.ppf(1-(1-self.confidence)/2)
        # self.upper = self.pattern + self.residuals.std() * self.sigma_level
        # self.lower = self.pattern - self.residuals.std() * self.sigma_level
        # self.out_of_bounds = self.series[((self.series > self.upper) | (self.series < self.lower)) & (self.outliers.isnull())]
        if self.confidence:
            _calculate_bounds(self)
            
    def plot(self, **kwargs):
        
        return _pattern_plot(self)
        # style = kwargs.get('style', bluebelt.styles.paper)
        # kwargs.pop('style', None)

        # path = kwargs.pop('path', None)        
        
        # # prepare figure
        # fig = plt.figure(constrained_layout=False, **kwargs)
        # gridspec = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[5,3], wspace=0, hspace=0)
        # ax1 = fig.add_subplot(gridspec[0, 0], zorder=50)
        # ax2 = fig.add_subplot(gridspec[1, 0], zorder=40)
        
        # # observations
        # ax1.plot(self.series, **style.patterns.observations)

        # # pattern
        # ax1.plot(self.pattern, **style.patterns.pattern)
        
        # # outliers
        # ax1.plot(self.outliers, **style.patterns.outlier_background)
        # ax1.plot(self.outliers, **style.patterns.outlier)

        # # bandwidth
        # ax1.fill_between(self.series.index, self.lower, self.upper, **style.patterns.bandwidth_fill_between)
        # ax1.plot(self.lower, **style.patterns.lower)
        # ax1.plot(self.upper, **style.patterns.upper)
        
        # # out of bounds
        # ax1.plot(self.out_of_bounds, **style.patterns.out_of_bounds)
        
        # # labels
        # ax1.set_title(f'{self.pattern.name} probability chart of {self.series.name}', **style.patterns.title)
        # ax1.set_ylabel('value')

        # #ax1.text(0.02, 0.9, r'$R^2$'+f': {self.rsq}', transform=ax1.transAxes, va='center', ha='left')
        

        # # set x axis locator
        # mpl_format.axisformat(ax1, self.series)


        # # histogram
        # ax2.hist(self.residuals, **style.patterns.histogram)
        # ax2.set_yticks([])

        # # get current limits
        # xlims = ax2.get_xlim()
        # ylims = ax2.get_ylim()
        
        # # fit a normal distribution to the data
        # norm_mu, norm_std = stats.norm.fit(self.residuals.dropna())
        # pdf_x = np.linspace(xlims[0], xlims[1], 100)
        # ax2.plot(pdf_x, stats.norm.pdf(pdf_x, norm_mu, norm_std), **style.patterns.normal_plot)

        # # histogram x label
        # ax2.set_xlabel('residuals distribution')
 
                
        # ax2.set_ylim(ylims[0], ylims[1]*1.5)
        # ax2.spines['left'].set_visible(False)
        # ax2.spines['right'].set_visible(False)

        # #ax2.text(0.02, 0.7, "residuals distribution", bluebelt.statistics.hypothesis_testing=ax2.transAxes, va='center', ha='left')
        # #ax2.text(0.02, 0.7, f'p: {self.p_val:1.2f}', transform=ax2.transAxes, va='center', ha='left')

        # plt.gcf().subplots_adjust(right=0.8)

        # if path:
        #     plt.savefig(path)
        #     plt.close()
        # else:
        #     plt.close()
        #     return fig

class Periodical():
    
    """
    Find the periodical pattern of a series and project a bandwidth
    series: pandas.Series
    rule: period representation used for resampling the series
        default value: "1W"
    how: define how the period must be evaluated
        options are "mean", "min", "max" and "std"
        default value: "mean"
    resolution: define the resolution of the pattern
        the pattern is rounded to fit the resolution
        default value: None
    confidence: float
        the bandwidth confidence
        default value: 0.8
    outlier_sigma: float
        outliers are datapoints outside the outlier_sigma fraction
        default value: 2
    
    """

    def __init__(self, series, rule='1W', how='mean', resolution=None, confidence=None, outlier_sigma=2, adjust=True, **kwargs):
        
        self.series = series
        self.rule = rule
        self.how = how
        self.resolution = resolution
        self.confidence = confidence
        self.outlier_sigma = outlier_sigma
        self.adjust = adjust
        
        self.calculate()

    def calculate(self):
        
        # set pattern and residuals        
        self.pattern, self.residuals, self.p_val, self.rsq = _peri_hand_granade(series=self.series, rule=self.rule, how=self.how, resolution=self.resolution)

        # set outliers
        self.outliers = pd.Series(data=np.where(self.residuals.abs() > self.residuals.std() * self.outlier_sigma, self.series, None), index=self.series.index)
        self.outliers_count = np.count_nonzero(self.outliers)

        # handle adjusted
        self.adjusted = self.series.loc[~self.outliers.notnull()]
        if self.adjust:
            # replace outliers with None values so they will be ignored by _peri_hand_granade and reset pattern
            values = pd.Series(data=np.where(self.outliers.notnull(), None, self.series).astype(np.float), index=self.series.index)
            self.pattern, self.residuals, self.p_val, self.rsq = _peri_hand_granade(series=values, rule=self.rule, how=self.how, resolution=self.resolution)
        
        self.pattern.rename(f'periodical ({self.rule})', inplace=True)

        # handle bounds
        if self.confidence:
            _calculate_bounds(self)

    def plot(self, **kwargs):
        return _pattern_plot(self)

def _poly_hand_granade(series, shape=(0, 6), validation='p_val', threshold=0.05, **kwargs):

    """
    Find the polynomial of a series.
    series = the pandas Series
    shape: int or tuple
        when an int is provided the polynomial is provided as n-th degree polynomial
        when a tuple is provided the function will find an optimised polynomial between first and second value of the tuple
    validation: only for tuple shape
        p_val: test for normal distribution of the residuals
        rsq: check for improvement of the rsq value
    threshold: the threshold for normal distribution test or rsq improvement
    """

    # get the index
    index = series.index.astype(int)-series.index.astype(int).min()
    index = index / np.gcd.reduce(index)

    # drop nan values
    _index = series.dropna().index.astype(int)-series.index.astype(int).min()
    _index = _index / np.gcd.reduce(_index)

    # get the values
    values = series.dropna().values

    # set first rsq
    _rsq = 0


    if isinstance(shape, int):
        pattern = pd.Series(index=series.index, data=np.polynomial.polynomial.polyval(index, np.polynomial.polynomial.polyfit(_index, values, shape)), name=f'{_get_nice_polynomial_name(shape)}')
        residuals = pd.Series(index=series.index, data=[a - b for a, b in zip(series.values, pattern)])
        
        p_val = stats.mstats.normaltest(residuals.dropna().values)[1]
        rsq = np.corrcoef(series.values, pattern.values)[1,0]**2


    elif isinstance(shape, tuple):

        with warnings.catch_warnings():
            warnings.filterwarnings('error')
            for shape in range(shape[0], shape[1]+1):
                try:
                    pattern = pd.Series(index=series.index, data=np.polynomial.polynomial.polyval(index, np.polynomial.polynomial.polyfit(_index, values, shape)), name=f'{_get_nice_polynomial_name(shape)}')
                    residuals = pd.Series(index=series.index, data=[a - b for a, b in zip(series.values, pattern)])
                    
                    np_err = np.seterr(divide='ignore', invalid='ignore') # ignore possible divide by zero
                    rsq = np.corrcoef(series.values, pattern.values)[1,0]**2
                    np.seterr(**np_err) # go back to previous settings
                    
                    p_val = stats.mstats.normaltest(residuals.dropna().values)[1]

                    if validation=='p_val' and p_val >= threshold:
                        break
                    elif validation=='rsq' and (rsq - _rsq) / rsq < threshold:
                        pattern = pd.Series(index=series.index, data=poly.polyval(index, poly.polyfit(_index, values, shape-1)), name=f'{_get_nice_polynomial_name(shape-1)}')    
                        residuals = pd.Series(index=series.index, data=[a - b for a, b in zip(series.values, pattern)])
                        
                        # reset rsq
                        rsq = _rsq
                        break
                    
                    # set previous rsq to current rsq
                    _rsq = rsq

                except poly.pu.RankWarning:
                    print(f'RankWarning at {_get_nice_polynomial_name(shape)}')
                    break
    else:
        pattern = None
        residuals = None

    return pattern, residuals, p_val, rsq

def _peri_hand_granade(series, rule, how, resolution, **kwargs):

    # set pattern and residuals
    if how=='mean':
        pattern = series.resample(rule=rule, label='left').mean().reindex_like(series, method='ffill')
    elif how=='min':
        pattern = series.resample(rule=rule, label='left').min().reindex_like(series, method='ffill')
    elif how=='max':
        pattern = series.resample(rule=rule, label='left').max().reindex_like(series, method='ffill')
    elif how=='std':
        pattern = series.resample(rule=rule, label='left').std().reindex_like(series, method='ffill')
    else:
        pattern = series
    
    if resolution:
        # adjust for resolution
        pattern = pattern.divide(resolution).round(0).multiply(resolution)
    
    residuals = series - pattern

    p_val = stats.mstats.normaltest(residuals.dropna().values)[1]
    rsq = np.corrcoef(series.values, pattern.values)[1,0]**2

    return pattern, residuals, p_val, rsq

def _get_nice_polynomial_name(shape):
    if shape==0:
        return 'linear'
    if shape==1:
        return str(shape)+'st degree polynomial'
    elif shape==2:
        return str(shape)+'nd degree polynomial'
    elif shape==3:
        return str(shape)+'rd degree polynomial'
    else:
        return str(shape)+'th degree polynomial'

def _calculate_bounds(pattern_obj):
        
    pattern_obj.sigma_level = stats.norm.ppf(1-(1-pattern_obj.confidence)/2)

    # set bounds
    pattern_obj.upper = pattern_obj.pattern + pattern_obj.residuals.std() * pattern_obj.sigma_level
    pattern_obj.lower = pattern_obj.pattern - pattern_obj.residuals.std() * pattern_obj.sigma_level

    # set out of bounds values
    pattern_obj.out_of_bounds = pattern_obj.series[((pattern_obj.series > pattern_obj.upper) | (pattern_obj.series < pattern_obj.lower)) & (pattern_obj.outliers.isnull())]

    return pattern_obj

def _pattern_plot(pattern_obj, **kwargs):
        
    style = kwargs.get('style', bluebelt.styles.paper)
    kwargs.pop('style', None)

    path = kwargs.pop('path', None)        
    
    # prepare figure
    fig = plt.figure(constrained_layout=False, **kwargs)
    gridspec = fig.add_gridspec(nrows=2, ncols=1, height_ratios=[5,3], wspace=0, hspace=0)
    ax1 = fig.add_subplot(gridspec[0, 0], zorder=50)
    ax2 = fig.add_subplot(gridspec[1, 0], zorder=40)
    
    # observations
    ax1.plot(pattern_obj.series, **style.patterns.observations)

    # pattern
    ax1.plot(pattern_obj.pattern, **style.patterns.pattern)
    
    # outliers
    ax1.plot(pattern_obj.outliers, **style.patterns.outlier_background)
    ax1.plot(pattern_obj.outliers, **style.patterns.outlier)

    # bounds
    if pattern_obj.confidence:
        ax1.fill_between(pattern_obj.series.index, pattern_obj.lower, pattern_obj.upper, **style.patterns.bandwidth_fill_between)
        ax1.plot(pattern_obj.lower, **style.patterns.lower)
        ax1.plot(pattern_obj.upper, **style.patterns.upper)
    
        # out of bounds
        ax1.plot(pattern_obj.out_of_bounds, **style.patterns.out_of_bounds)
        
    # labels
    ax1.set_title(f'{pattern_obj.pattern.name} probability chart of {pattern_obj.series.name}', **style.patterns.title)
    ax1.set_ylabel('value')

    #ax1.text(0.02, 0.9, r'$R^2$'+f': {pattern_obj.rsq}', transform=ax1.transAxes, va='center', ha='left')
    

    # set x axis locator
    mpl_format.axisformat(ax1, pattern_obj.series)


    # histogram
    ax2.hist(pattern_obj.residuals, **style.patterns.histogram)
    ax2.set_yticks([])

    # get current limits
    xlims = ax2.get_xlim()
    ylims = ax2.get_ylim()
    
    # fit a normal distribution to the data
    norm_mu, norm_std = stats.norm.fit(pattern_obj.residuals.dropna())
    pdf_x = np.linspace(xlims[0], xlims[1], 100)
    ax2.plot(pdf_x, stats.norm.pdf(pdf_x, norm_mu, norm_std), **style.patterns.normal_plot)

    # histogram x label
    ax2.set_xlabel('residuals distribution')

            
    ax2.set_ylim(ylims[0], ylims[1]*1.5)
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    ax2.text(0.02, 0.7, f'p: {pattern_obj.p_val:1.2f}', transform=ax2.transAxes, va='center', ha='left')

    plt.gcf().subplots_adjust(right=0.8)

    if path:
        plt.savefig(path)
        plt.close()
    else:
        plt.close()
        return fig