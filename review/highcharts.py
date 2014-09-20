# -*- coding: utf-8 -*-

TEMPLATE = """
var chart%(id)d;
var plotOptions%(id)d = %(plotOptions)s;
var tooltip%(id)d = {};

if (plotOptions%(id)d['pie']) {
    plotOptions%(id)d['pie']['dataLabels']['formatter'] = function() { return (this.point.name.length > 30 ? this.point.name.substr(0, 30) + '...' : this.point.name) + ': <b>'+ this.y + '</b>' ; };
    plotOptions%(id)d['pie']['dataLabels']['style'] = {fontSize: '9px'};
    var tooltip%(id)d = {
        formatter: function() {
            return this.point.name +': <b>'+ this.y + '</b> de ' + this.total + ' ('+ this.percentage.toFixed(2) +'%%)';
        }
    }
}

$(document).ready(function() {
   chart%(id)d = new Highcharts.Chart({
      chart: %(chart)s,
      title: %(title)s,
      legend: %(legend)s,
      subtitle: %(subtitle)s,
      plotOptions: plotOptions%(id)d,
      series: %(series)s,
      xAxis: %(xAxis)s,
      yAxis: %(yAxis)s,
      tooltip: tooltip%(id)d,
      credits : %(credits)s,
   });
});

"""

from django.utils import simplejson
from django.utils.safestring import mark_safe


class Chart(object):
    
    def __init__(self, renderTo, **kwargs):
        self.chart = dict(renderTo=renderTo)
        self.credits = dict(enabled=False)
        self.labels = dict()
        self.legend = dict()
        self.plotOptions = dict()
        self.series = dict()
        self.title = dict()
        self.subtitle = dict()
        self.xAxis = dict()
        self.yAxis = dict()
        
        if 'title' in kwargs:
            self.title['text'] = kwargs['title']
        if 'subtitle' in kwargs:
            self.subtitle['text'] = kwargs['subtitle']
    
    def __unicode__(self):
        ctx = dict()
        for key, val in self.__dict__.items():
            ctx[key] = simplejson.dumps(getattr(self, key))
        ctx['id'] = id(self)
        return mark_safe(TEMPLATE % ctx)


class PieChart(Chart):
    def __init__(self, renderTo, **kwargs):
        """
        ``data``: [['Item 1', 10], ['Item 2', 20]]
        """
        if 'data' not in kwargs:
            raise ValueError('"data" param must be supplied.')
        
        show_legend = kwargs.pop('show_legend') if 'show_legend' in kwargs else True
        
        super(PieChart, self).__init__(renderTo, **kwargs)
        self.kind = 'PieChart'
        self.plotOptions = dict(
            pie = dict(
                allowPointSelect = True,
                cursor           = 'pointer',
                dataLabels       = dict(),
                showInLegend     = show_legend
            ),
        )
        self.series = [dict(type='pie', data=kwargs['data'])]


class ColumnChart(Chart):
    def __init__(self, renderTo, **kwargs):
        """
        ``data``: [['Item 1', 10], ['Item 2', 20]]
        ``minPointLength``: 0
            Indica a altura mínima em pixels (mesmo se for valor zero)
        """
        if 'data' not in kwargs:
            raise ValueError('"data" param must be supplied.')
        
        super(ColumnChart, self).__init__(renderTo, **kwargs)
        self.kind = 'ColumnChart'
        self.chart['defaultSeriesType'] = 'column'
        self.xAxis = dict(categories=[i[0] for i in kwargs['data']])
        self.yAxis['title'] = dict(text=u'Total')
        self.series = [dict(name=u'Total', data=[i[1] for i in kwargs['data']])]
        self.legend = dict(enabled=False)
        self.plotOptions['series'] = dict(minPointLength=kwargs.get('minPointLength', 0))


class BarChart(Chart):
    def __init__(self, renderTo, **kwargs):
        """
        ``data``: [['Item 1', 10], ['Item 2', 20]]
        ``minPointLength``: 0
            Indica a altura mínima em pixels (mesmo se for valor zero)
        """
        if 'data' not in kwargs:
            raise ValueError('"data" param must be supplied.')
        
        super(BarChart, self).__init__(renderTo, **kwargs)
        self.kind = 'ColumnChart'
        self.chart['defaultSeriesType'] = 'bar'
        self.xAxis = dict(categories=[i[0] for i in kwargs['data']])
        self.yAxis['title'] = dict(text=u'Total')
        self.series = [dict(name=u'Total', data=[i[1] for i in kwargs['data']])]
        self.legend = dict(enabled=False)
        self.plotOptions['series'] = dict(minPointLength=kwargs.get('minPointLength', 0))
        

class GroupedColumnChart(Chart):
    def __init__(self, renderTo, **kwargs):
        # groups: ['Jan', 'Fev', 'Mar']
        # data: [['Store A', 10, 15, 20], ['Store B', 20, 25, 30], ['Store C', 30, 35, 40]]
        if 'data' not in kwargs:
            raise ValueError('"data" param must be supplied.')
        if 'groups' not in kwargs:
            raise ValueError('"groups" param must be supplied.')
        
        super(GroupedColumnChart, self).__init__(renderTo, **kwargs)
        self.kind = 'GroupedColumnChart'
        self.chart['defaultSeriesType'] = 'column'
        self.xAxis = dict(categories=[i[0] for i in kwargs['data']])
        self.yAxis = dict(title=dict(text=u'Total'))
        
        # Formatando series
        if 'stack' not in kwargs:
            self.series = []
            for idx, category in enumerate(kwargs['groups']):
                self.series.append(dict(name=category, data=[i[idx+1] for i in kwargs['data']]))
        else:
            self.plotOptions = dict(
                                    column = dict(
                                               stacking           = 'normal',
                                               ),
                                    )
            
            self.series = []
            for idx, category in enumerate(kwargs['groups']):
                for z,stack in enumerate(kwargs['stack']):
                    self.series.append(dict(name=category, data=[i[idx+1] for i in kwargs['data']],stack=stack ))
            
            
        
class LineChart(Chart):
    def __init__(self, renderTo, **kwargs):
        if 'data' not in kwargs:
            raise ValueError('"data" param must be supplied.')
        if 'groups' not in kwargs:
            raise ValueError('"groups" param must be supplied.')
        
        super(LineChart, self).__init__(renderTo, **kwargs)
        self.kind = 'LineChart'
        self.chart['defaultSeriesType'] = 'line'
        self.xAxis = dict(categories=[i[0] for i in kwargs['data']])
        self.yAxis = dict(title=dict(text=kwargs.get('yAxis_title_text', u'Total')))

        self.plotOptions['line'] = dict(
            dataLabels=dict(
                enabled=kwargs.get('plotOptions_line_dataLabels_enable', False),
            enableMouseTracking=kwargs.get('plotOptions_line_enableMouseTracking', False)))
        
        # Formatando series
        self.series = []
        for idx, category in enumerate(kwargs['groups']):
            self.series.append(dict(name=category, data=[i[idx+1] for i in kwargs['data']]))
