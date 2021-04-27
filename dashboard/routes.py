from flask import render_template, url_for
from dashboard import app
import math
import numpy as np
import pandas as pd
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, Legend, FactorRange
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, stack
from bokeh.palettes import Spectral6
from flask import Flask, render_template, request, url_for

def tax_to_gdp_contrib():
    tooltips = [
        ('Year','@x'),
        ('GDP per capita', '@y{0.000}')
    ]
    data = pd.read_csv("./dashboard/static/datasets/Tax revenue (percentage of GDP).csv")
    x = data["Year"].tolist()
    y = data["India"].tolist()
    TOOLS="crosshair,pan,box_zoom,reset,save,"
    fig = figure(
        title="Tax Revenue (% of GDP)", 
        x_axis_label="Year", 
        y_axis_label="Tax Revenue (in %)", 
        max_height=300, 
        max_width=500, 
        sizing_mode='stretch_both',
        tools=TOOLS
    )
    fig.line(x, y)
    fig.circle(x, y)
    r2 = fig.circle(x, y, size=8, alpha=0, hover_fill_color='black', hover_alpha=0.5)
    fig.add_tools(HoverTool(tooltips=tooltips, mode="vline", renderers=[r2]))
    fig.toolbar.active_drag = None
    return fig

def gdp_per_capita():
    tooltips = [
            ('Year','@x'),
            ('GDP per capita', '@y{0.000}')
        ]
    data = pd.read_csv("./dashboard/static/datasets/GDP-per-capita.csv")
    x = data["label"].tolist()
    y = data["GDP Per Capita"].tolist()
    TOOLS="crosshair,pan,box_zoom,reset,save,"
    fig = figure(
        title="GDP Per Capita Vs Year", 
        x_axis_label="Year", 
        y_axis_label="GDP Per Capita (in $)", 
        max_height=300, 
        max_width=500, 
        sizing_mode='stretch_both',
        tools=TOOLS
    )
    fig.line(x, y)
    fig.circle(x, y)
    r2 = fig.circle(x, y, size=8, alpha=0, hover_fill_color='black', hover_alpha=0.5)
    fig.add_tools(HoverTool(tooltips=tooltips, mode="vline", renderers=[r2]))
    fig.toolbar.active_drag = None
    return fig

def gdp_growth_rate():
    tooltips = [
            ('Year','@x'),
            ('GDP Growth Rate', '@y{0.000}')
        ]
    data = pd.read_csv("./dashboard/static/datasets/GDP-growth-rate.csv")
    x = data["label"].tolist()
    y = data["GDP Growth Rate"].tolist()
    TOOLS="crosshair,pan,box_zoom,reset,save,"
    fig = figure(
        title="GDP Growth Rate Vs Year", 
        x_axis_label="Year", 
        y_axis_label="GDP Growth Rate (in %)", 
        max_height=300, 
        max_width=500, 
        sizing_mode='stretch_both',
        tools=TOOLS
    )
    fig.line(x, y)
    fig.circle(x, y)
    r2 = fig.circle(x, y, size=8, alpha=0, hover_fill_color='black', hover_alpha=0.5)
    fig.line(x, 0, line_color="red")
    fig.add_tools(HoverTool(tooltips=tooltips, mode="vline", renderers=[r2]))
    fig.toolbar.active_drag = None
    return fig

def contrib_direct_and_indirect_tax():
    tooltips = [
            ('Year','@x'),
            ('Contribution', '@counts{0.00}')
        ]
    data = pd.read_csv("./dashboard/static/datasets/Revenue Realisation from Direct & Indirect Taxes from 2000-01 to 2020-21.csv")
    fy = [str(s) for s in data["Financial year"].tolist()]
    dt = data["% Share in Total Taxes - Direct Taxes"].tolist()
    idt = data["% Share in Total Taxes - Indirect Taxes"].tolist()
    x = [(_fy, _tax_type) for _fy in fy for _tax_type in ['Direct Tax', 'Indirect Tax']]
    counts = sum(zip(dt, idt), ())
    source = ColumnDataSource(data = dict(x = x, counts = counts))
    TOOLS="crosshair,pan,box_zoom,reset,save,"
    fig = figure(
        title="% Share in Total Taxes",
        x_range=FactorRange(*x),
        max_height=300, 
        max_width=800, 
        sizing_mode='stretch_both',
        tools=TOOLS
    )
    fig.vbar(
        x='x', 
        top='counts', 
        width=0.9, 
        fill_color=factor_cmap('x', palette=['#1F77B4', 'red'], factors=['Direct Tax', 'Indirect Tax'], start=1, end=2), 
        source=source,
        line_color="white"
    )
    fig.add_tools(HoverTool(tooltips=tooltips, mode="vline"))
    fig.xaxis.visible = False
    fig.toolbar.active_drag = None
    return fig

def annual_growth_direct_indirect_and_total_tax():
    data = pd.read_csv("./dashboard/static/datasets/Revenue Realisation from Direct & Indirect Taxes from 2000-01 to 2020-21.csv")
    x = data["Financial year"].tolist()
    y1 = data["% Annual Growth - Direct Taxes"].tolist()
    y2 = data["% Annual Growth - Indirect Taxes"].tolist()
    y3 = data["% Annual Growth - Total Taxes"].tolist()
    tooltips = [
        ('Year','@x'),
        ('Growth Rate', '@y{0.00}')
    ]
    data = dict(x=x, y1=y1, y2=y2, y3=y3)
    source = ColumnDataSource(data = data)
    TOOLS="crosshair,pan,box_zoom,reset,save,"
    fig = figure(
        title="Tax Growth Rate", 
        x_axis_label="Year", 
        y_axis_label="Growth Rate (in %)", 
        max_height=300, 
        max_width=800, 
        sizing_mode='stretch_both',
        tools=TOOLS,
        tooltips=tooltips
    )
    fig.line(x, y1, line_color="red", legend_label="Direct Taxes")
    fig.circle(x, y1, color="red")

    fig.line(x, y2, line_color="green", legend_label="Indirect Taxes")
    fig.circle(x, y2, color="green")
    
    fig.line(x, y3, line_color="navy", legend_label="Total Taxes")
    fig.circle(x, y3, color="navy")
    fig.toolbar.active_drag = None
    return fig

def various_taxes_to_revenue():
    tooltips = [
        ('Year','@x'),
        ('Tax %', '@y{0.00}')
    ]
    data = pd.read_csv("./dashboard/static/datasets/Taxes on goods and services (percentage of revenue).csv")
    x = data["Year"].tolist()
    y1 = data["India"].tolist()
    data = pd.read_csv("./dashboard/static/datasets/Taxes on income, profits and capital gains (percentage of revenue).csv")
    y2 = data["India"].tolist()
    data = pd.read_csv("./dashboard/static/datasets/Taxes on international trade (percentage of revenue).csv")
    y3 = data["India"].tolist()
    data = pd.read_csv("./dashboard/static/datasets/Other taxes (percentage of revenue).csv")
    y4 = data["India"].tolist()

    data = dict(x=x, y1=y1, y2=y2, y3=y3, y4=y4)
    source = ColumnDataSource(data = data)
    TOOLS="crosshair,pan,box_zoom,reset,save,"
    fig = figure(
        title="Various Taxes (% of revenue)", 
        x_axis_label="Year", 
        y_axis_label="Tax Percentage (in %)", 
        max_height=300, 
        max_width=800, 
        sizing_mode='stretch_both',
        tools=TOOLS,
        tooltips=tooltips
    )
    fig.line(x, y1, line_color="red", legend_label="Taxes on goods and services")
    fig.circle(x, y1, color="red")

    fig.line(x, y2, line_color="green", legend_label="Taxes on income, profits and capital gains")
    fig.circle(x, y2, color="green")
    
    fig.line(x, y3, line_color="navy", legend_label="Taxes on international trade")
    fig.circle(x, y3, color="navy")
    
    fig.line(x, y4, line_color="orange", legend_label="Other taxes")
    fig.circle(x, y4, color="orange")
    fig.toolbar.active_drag = None
    return fig

def various_taxes_to_total_tax():
    tooltips = [
        ('Year','@x'),
        ('Tax %', '@y{0.00}')
    ]
    data = pd.read_csv("./dashboard/static/datasets/Customs and other import duties (percentage of tax revenue).csv")
    x = data["Year"].tolist()
    y1 = data["India"].tolist()
    data = pd.read_csv("./dashboard/static/datasets/Taxes on income, profits and capital gains (percentage of total taxes).csv")
    y2 = data["India"].tolist()
    data = pd.read_csv("./dashboard/static/datasets/Taxes on goods and services (percentage value added of industry and services).csv")
    y3 = data["India"].tolist()

    data = dict(x=x, y1=y1, y2=y2, y3=y3)
    source = ColumnDataSource(data = data)
    TOOLS="crosshair,pan,box_zoom,reset,save,"
    fig = figure(
        title="Various Taxes (% of total taxes)", 
        x_axis_label="Year", 
        y_axis_label="Tax Percentage (in %)", 
        max_height=300, 
        max_width=800, 
        sizing_mode='stretch_both',
        tools=TOOLS,
        tooltips=tooltips
    )
    fig.line(x, y1, line_color="red", legend_label="Customs and other import duties")
    fig.circle(x, y1, color="red")

    fig.line(x, y2, line_color="green", legend_label="Taxes on income, profits and capital gains")
    fig.circle(x, y2, color="green")
    
    fig.line(x, y3, line_color="navy", legend_label="Taxes on international trade (% VAT)")
    fig.circle(x, y3, color="navy")
    fig.toolbar.active_drag = None
    return fig

@app.route('/')
def home():
    script, html = components(tax_to_gdp_contrib())
    _tax_to_gdp_contrib = {
        "html" : html,
        "script" : script
    }
    script, html = components(gdp_per_capita())
    _gdp_per_capita = {
        "html" : html,
        "script" : script
    }
    script, html = components(gdp_growth_rate())
    _gdp_growth_rate = {
        "html" : html,
        "script" : script
    }
    script, html = components(contrib_direct_and_indirect_tax())
    _contrib_direct_and_indirect_tax = {
        "html" : html,
        "script" : script
    }
    script, html = components(annual_growth_direct_indirect_and_total_tax())
    _annual_growth_direct_indirect_and_total_tax = {
        "html" : html,
        "script" : script
    }
    script, html = components(various_taxes_to_revenue())
    _various_taxes_to_revenue = {
        "html" : html,
        "script" : script
    }
    script, html = components(various_taxes_to_total_tax())
    _various_taxes_to_total_tax = {
        "html" : html,
        "script" : script
    }
    return render_template(
        'home/home.html',
        tax_to_gdp_contrib_html=_tax_to_gdp_contrib["html"],
        tax_to_gdp_contrib_script=_tax_to_gdp_contrib["script"],
        gdp_per_capita_html=_gdp_per_capita["html"],
        gdp_per_capita_script=_gdp_per_capita["script"],
        gdp_growth_rate_html=_gdp_growth_rate["html"],
        gdp_growth_rate_script=_gdp_growth_rate["script"],
        contrib_direct_and_indirect_tax_html=_contrib_direct_and_indirect_tax["html"],
        contrib_direct_and_indirect_tax_script=_contrib_direct_and_indirect_tax["script"],
        annual_growth_direct_indirect_and_total_tax_html=_annual_growth_direct_indirect_and_total_tax["html"],
        annual_growth_direct_indirect_and_total_tax_script=_annual_growth_direct_indirect_and_total_tax["script"],
        various_taxes_to_revenue_html=_various_taxes_to_revenue["html"],
        various_taxes_to_revenue_script=_various_taxes_to_revenue["script"],
        various_taxes_to_total_tax_html=_various_taxes_to_total_tax["html"],
        various_taxes_to_total_tax_script=_various_taxes_to_total_tax["script"]
    )