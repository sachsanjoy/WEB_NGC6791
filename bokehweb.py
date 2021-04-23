import numpy as np
import matplotlib.pyplot as plt
from bokeh.io import output_file, show
from bokeh.models.annotations import Title
from bokeh.layouts import gridplot
from bokeh.layouts import column
from bokeh.layouts import row
from bokeh.models import ColumnDataSource, OpenURL, TapTool
from bokeh.models import ColumnDataSource
from bokeh.models import TapTool
from bokeh.models import DataTable
from bokeh.models import TableColumn
from bokeh.models.markers import Circle
from bokeh.plotting import figure
from bokeh.models import Arrow, OpenHead, NormalHead, VeeHead
from bokeh.models import Range1d
from bokeh.models import ColumnDataSource, Range1d, LabelSet, Label
import wget

#dataframes
import pandas as pd
# Bokeh Library
from bokeh.models import HoverTool

#Output file
output_file("ngc6791web/index.html")

import modules.read_mist_models as read_mist_models

#MIST isochrones input
isocmd = read_mist_models.ISOCMD('data/MIST_v1.2_vvcrit0.0_UBVRIplus/MIST_v1.2_feh_p0.25_afe_p0.0_vvcrit0.0_UBVRIplus.iso.cmd')

print ('version: ', isocmd.version)
print ('photometric system: ', isocmd.photo_sys)
print ('abundances: ', isocmd.abun)
print ('rotation: ', isocmd.rot)
print ('ages: ', [round(x,2) for x in isocmd.ages])
print ('number of ages: ', isocmd.num_ages)
print ('available columns: ', isocmd.hdr_list)
print ('Av extinction: ', isocmd.Av_extinction)

# Input age returns the index for the desired age
age = 9.95
age_ind = isocmd.age_index(age) 
G = isocmd.isocmds[age_ind]['Gaia_G_DR2Rev']
BP = isocmd.isocmds[age_ind]['Gaia_BP_DR2Rev']
RP = isocmd.isocmds[age_ind]['Gaia_RP_DR2Rev']
BB = isocmd.isocmds[age_ind]['Bessell_B']
BV = isocmd.isocmds[age_ind]['Bessell_V']

# loading data
dfov = pd.read_csv('data/6791_GEDR3_GMM_ACM_CM_PM.csv')
dv = pd.read_csv('data/NGC6791.csv')
dfov.ra = dfov.ra.astype(float)
dfov.dec = dfov.dec.astype(float)
dfov.bp_rp = dfov.bp_rp.astype(float)
dfov.phot_g_mean_mag = dfov.phot_g_mean_mag.astype(float)

dv.ra = dv.ra.astype(float)
dv.dec = dv.dec.astype(float)
dv.BP_RP = dv.BP_RP.astype(float)
dv.GMAG = dv.GMAG.astype(float)
#choosing acm members with p>0.5
pt = 0.5 
print('Almost certain members : ', len(dfov[dfov.ACM>=pt]))
print('Certain members : ', len(dfov[dfov.CM>=pt]))
print('Probable members : ', len(dfov[dfov.PM>=pt]))
print('Almost certain variable members : ', len(dv[dv.ACM>=pt]))
dngc = dfov[dfov.ACM>=pt]
dvngc = dv[dv.ACM>=pt]
dvfield = dv[dv.ACM<pt]
Av = 0.33 # extintion
#mM = 13.45 # 13.35 Antony Twarog 2006
#distance modulus from parallax of 4200 and extintion
mM = 5*np.log10(4200)-5+Av
ex = 0.19 # 0.09
dfov['bp_rp_abs'] = dfov.bp_rp-ex
dngc['bp_rp_abs'] = dngc.bp_rp-ex
dvngc['BP_RP_abs'] = dvngc.BP_RP-ex
dvfield['BP_RP_abs'] = dvfield.BP_RP-ex

dfov['phot_g_mean_mag_abs'] = dfov.phot_g_mean_mag-mM
dngc['phot_g_mean_mag_abs'] = dngc.phot_g_mean_mag-mM
dvngc['GMAG_abs'] = dvngc.GMAG-mM
dvfield['GMAG_abs'] = dvfield.GMAG-mM
#Bokeh plots
sample1 = dfov.sample(np.shape(dfov)[0]) #FOV
source1 = ColumnDataSource(sample1)

sample2 = dngc.sample(np.shape(dngc)[0]) #almost certain members
source2 = ColumnDataSource(sample2)

sample3 = dvngc.sample(np.shape(dvngc)[0]) #variable almost certain members
source3 = ColumnDataSource(sample3)

sample4 = dvfield.sample(np.shape(dvfield)[0]) #variable almost certain members
source4 = ColumnDataSource(sample4)

TOOLS = "pan,wheel_zoom,box_zoom,reset,tap"

#MAP
s1 = figure(plot_width=500, plot_height=500,background_fill_color="#000000",tools=TOOLS)
#ngcfov = s1.circle('ra','dec', source=source1, size=2, color="#6063FF", alpha=0.8,name='ngcfov',legend_label='*FOV')
ngc_memb = s1.circle('ra','dec', source=source2, size=2, color="#6063FF", alpha=0.8,name='ngc',legend_label='*6791')
ngc_vstar = s1.circle('ra','dec', source=source3, size=2, color="#FF002A", alpha=0.8,legend_label='V*6791')
ngc_vfield = s1.circle('ra','dec', source=source4, size=2, color="#00eb00", alpha=0.8,legend_label='V*FIELD')

#ngcfov.visible = False
ngc_memb.visible = True
ngc_vstar.visible = True
ngc_vfield.visible = False
s1.legend.location = "top_left"
s1.legend.click_policy="hide"
s1.legend.background_fill_alpha=0
s1.legend.border_line_alpha=0
s1.legend.label_text_color = "white"

core = Circle(x= 290.2208333333 ,y= 37.7716666667 ,radius=0.055, line_color = 'yellow',fill_alpha=0,radius_dimension='max',radius_units='data')
tide =Circle(x= 290.2208333333 ,y= 37.7716666667 ,radius=0.38, line_color = 'navy',fill_alpha=0,radius_dimension='max',radius_units='data')
s1.add_glyph(core)
s1.add_glyph(tide)
tooltips1 = [('index','@index'),('GAIA_ID','@designation')]
s1.add_tools(HoverTool(names=['ngc'],tooltips=tooltips1))
s1.xaxis.axis_label = 'ra'
s1.yaxis.axis_label = 'dec'
t1 = Title()
t1.text = 'MAP - Rc = 3.28 arcmin (yellow), Rt = 23 arcmin (blue)'
s1.title = t1

#CMD
s2 = figure(plot_width=500, plot_height=500,background_fill_color="#000000",tools=TOOLS)
ngc_vstar = s2.circle('BP_RP','GMAG', source=source3, size=4, color="#FF002A", alpha=1.0,legend_label='V*6791')
ngc_vfield = s2.circle('BP_RP','GMAG', source=source4, size=4, color="#00eb00", alpha=1.0,legend_label='V*FIELD') 
ngc_memb = s2.circle('bp_rp','phot_g_mean_mag', source=source2, size=5, color="#6063FF", alpha=0.5,name='ngc',legend_label='*6791')
#ngcfov = s2.circle('bp_rp','phot_g_mean_mag', source=source1, size=5, color="#6063FF", alpha=0.5,name='ngcfov',legend_label='*FOV')

#ngcfov.visible = False
ngc_memb.visible = True
ngc_vstar.visible = True
ngc_vfield.visible = False
s2.legend.location = "top_left"
s2.legend.click_policy="hide"
s2.legend.background_fill_alpha=0
s2.legend.border_line_alpha=0
s2.legend.label_text_color = "white"

s2.xaxis.axis_label = 'BP-RP'
s2.yaxis.axis_label = 'G'
t2 = Title()
t2.text = 'CMD - Linked to Aladin lite'
s2.title = t2
s2.y_range.flipped = True
tooltips1 = [('Index','@index'),('Gaia_ID','@designation')]
s2.add_tools(HoverTool(names=['ngc'],tooltips=tooltips1))
url = "http://aladin.u-strasbg.fr/AladinLite/?target=@ra%20@dec"
taptool = s2.select(type=TapTool)
taptool.callback = OpenURL(url=url)

#ISOCHRONES
s3 = figure(plot_width=500, plot_height=500, background_fill_color="#000000",tools=TOOLS)
#ngcfov = s3.circle('bp_rp_abs','phot_g_mean_mag_abs', source=source1, size=5, color="#6063FF", alpha=0.5,legend_label='*FOV')
ngc_memb = s3.circle('bp_rp_abs','phot_g_mean_mag_abs', source=source2, size=5, color="#6063FF", alpha=0.5,legend_label='*6791')
ngc_vstar = s3.circle('BP_RP_abs','GMAG_abs', source=source3, size=4, color="#FF002A", alpha=1.0,name='ngc',legend_label='V*6791')
ngc_vfield = s3.circle('BP_RP_abs','GMAG_abs', source=source4, size=4, color="#00eb00", alpha=1.0,name='field',legend_label='V*FIELD') 

#ngcfov.visible = False
ngc_memb.visible = True
ngc_vstar.visible = True
ngc_vfield.visible = False
s3.legend.location = "top_left"
s3.legend.click_policy="hide"
s3.legend.background_fill_alpha=0
s3.legend.border_line_alpha=0
s3.legend.label_text_color = "white"

s3.line(BP-RP,G,color='snow')
s3.xaxis.axis_label = 'BP-RP'
s3.yaxis.axis_label = 'MG'
#text labels

s3.add_layout(Label(x=-0.4,y=4.6,text='EHB',text_font_size='10px',text_color='#2e7bff'))
s3.add_layout(Label(x=0,y=12.0,text='WD',text_font_size='10px',text_color='#b3dfff'))
s3.add_layout(Label(x=0.5,y=1.8,text='BHB',text_font_size='10px',text_color='#2e7bff'))
s3.add_layout(Label(x=0.6,y=2.4,text='BS',text_font_size='10px',text_color='#2e62ff'))
s3.add_layout(Label(x=0.75,y=1.0,text='HB',text_font_size='10px',text_color='#66bfff'))
s3.add_layout(Label(x=0.8,y=-4.5,text='SG',text_font_size='10px',text_color='#7badf9'))
s3.add_layout(Label(x=1.3,y=-1.5,text='VRC',text_font_size='10px',text_color='#fa8e8e'))
s3.add_layout(Label(x=3.4,y=-2.5,text='post-AGB',text_font_size='10px',text_color='#fa0000'))
s3.add_layout(Label(x=3.6,y=-1,text='AGB',text_font_size='10px',text_color='#ff330f'))
s3.add_layout(Label(x=1.8,y=-0.2,text='AGB-Bump',text_font_size='10px',text_color='#ff5533'))
s3.add_layout(Label(x=1.3,y=0.7,text='RC',text_font_size='10px',text_color='#ff7733'))
s3.add_layout(Label(x=1.4,y=1.4,text='RGB-Bump',text_font_size='10px',text_color='#ffb833'))
s3.add_layout(Label(x=1.35,y=1.0,text='SRC',text_font_size='10px',text_color='#ffb800'))

s3.add_layout(Label(x=1.3,y=2.4,text='RGB',text_font_size='10px',text_color='#ff9233'))
s3.add_layout(Label(x=1.1,y=3.7,text='SGB',text_font_size='10px',text_color='#ffcc33'))
s3.add_layout(Label(x=0.92,y=3.65,text='MSTO',text_font_size='10px',text_color='#ffe524'))
s3.add_layout(Label(x=0.88,y=4.2,text='MS',text_font_size='10px',text_color='#ffb833'))
s3.add_layout(Label(x=0.78,y=3.25,text='MS',text_font_size='10px',text_color='#339cff'))
s3.add_layout(Label(x=1.02,y=5.4,text='MS',text_font_size='10px',text_color='#339cff'))

s3.add_layout(Label(x=1.38,y=6.8,text='sub-Dwarfs',text_font_size='10px',text_color='#ffcb0f'))

s3.add_layout(Label(x=1.2,y=8.0,text='MS+WD',text_font_size='10px',text_color='#ffcb0f'))
s3.add_layout(Label(x=2.0,y=8.7,text='Dwarfs',text_font_size='10px',text_color='#c76300'))


tooltips1 = [('ID','@ID')]
s3.add_tools(HoverTool(names=['ngc','field'],tooltips=tooltips1))
t3 = Title()
t3.text = 'MIST-CMD Fe/H = +0.25, Age = '+str(age)+' Gyr, (m-M)G = '+str(np.round(mM-Av,decimals=3))+', Av = '+str(Av) 
s3.title = t3
s3.y_range.flipped = True


#sourceTableSummary = ColumnDataSource(dngc)
#Columns = [TableColumn(field=colIndex, title=colIndex) for colIndex in dngc.columns] 
#data_table = DataTable(columns=Columns, source=sourceTableSummary, index_position = 0, width=500, height=500,fit_columns=False) 

sourceTableSummary1 = ColumnDataSource(dv)
Columns1 = [TableColumn(field=colIndex, title=colIndex) for colIndex in dvngc.columns] 
data_table1 = DataTable(columns=Columns1, source=sourceTableSummary1, index_position = 0, width=500, height=500,fit_columns=False) 

grid = gridplot([[s1, s2, s3],[data_table1]], sizing_mode='fixed')
#grid = gridplot([[s1, s2, s3],[data_table]])#, plot_width=800, plot_height=800)
show(grid)