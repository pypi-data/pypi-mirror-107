import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.figure import Figure
import seaborn as sns
import numpy as np
import scipy as sp

class Mineralogy(object):
    def __init__(self,name,feq_name,feq,seq,colors='blue', alpha=.1, linewidths=.75):
        self.name=name
        self.feq_name=feq_name
        self.feq=feq
        self.seq=seq
        self.colors=colors
        self.alpha=alpha
        self.linewidths=0.75


fluid_horita2014 = lambda d18Os,temp: (d18Os * 1.03086 + 30.86) - 3.140 * 10 ** 6. / (temp + 273.15) ** 2 + 3.14
solid_horita2014 = lambda d18Of,temp:(d18Of + 3.140 * 10 ** 6 / (temp + 273.15) ** 2 - 3.14 - 30.86) / 1.03086
fluid_kim1997 = lambda d18Os,temp: (d18Os * 1.03086 + 30.86) - 18.03 * 10 ** 3. / (temp + 273.15) + 32.42
solid_kim1997 = lambda d18Of,temp: (d18Of - 32.42 + 18.03 * 10 ** 3 / (temp + 273.15) - 30.86) / 1.03086
fluid_kim2007 = lambda d18Os,temp: (d18Os * 1.03086 + 30.86) - 17.88 * 10 ** 3. / (temp + 273.15) + 31.14
solid_kim2007 = lambda d18Of,temp: (d18Of + 17.88 * 10 ** 3. / (temp + 273.15) - 31.14 - 30.86) / 1.03086
fluid_mavromatis2012 = lambda d18Os,temp: (d18Os * 1.03086 + 30.86) - 18.03 / (
                temp + 273.15) + 32.42 - (6 * 10 ** 8 / (
                temp + 273.15) ** 3 - 5.47E6 / (temp + 273.15) ** 2 + 16.780 / (
                temp + 273.15) - 17.21) * 0.05
solid_mavromatis2012 = lambda d18Of,temp: (d18Of + 18.03 / (temp + 273.15) - 32.42 + (
            6 * 10 ** 8 / (temp + 273.15) ** 3 + 5.47 * 10 ** 6 / (temp + 273.15) ** 2 - 16.780 / (
            temp + 273.15) + 17.21) * 0.05 - 30.86) / 1.03086


mineral_dic = {'Dolomite': Mineralogy('Dolomite', 'Horita 2014', fluid_horita2014, solid_horita2014, colors='red', alpha=.1, linewidths=0.5),
            'Calcite': Mineralogy('Calcite','Kim and O.Neil 1997', fluid_kim1997, solid_kim1997,colors='blue', alpha=.1, linewidths=.75),
            'Aragonite': Mineralogy('Aragonite','Kim et al 2007', fluid_kim2007,solid_kim2007,colors='gray', alpha=.1, linewidths=0.5),
            'Mg-Calcite': Mineralogy('Mg-Calcite','Mavromatis et al 2012', fluid_mavromatis2012,solid_mavromatis2012,colors='blue', alpha=.1, linewidths=.75),
               }

def interpret(raw_data,drop_D48=True):
    replicates = raw_data[raw_data['Identifier_1'].notna()]
    samples_groups = replicates.groupby(replicates['Easotope Name'])
    samples = samples_groups.mean()
    n = samples_groups.count()
    samples['n'] = n['D47 CDES (Final)']
    features = ['D48 CDES (Final)', 'd13C VPDB (Final)', 'd18O VPDB (Final)', 'D47 CDES (Final)']
    
    for feature in features:
        samples[feature + ' SD'] = samples_groups[feature].std()
        samples[feature + ' SE'] = samples[feature + ' SD'] / samples['n'] ** .5
        samples[feature + ' @95CL'] = samples[feature + ' SE'] * sp.stats.t.ppf(1 - 0.025, samples['n'] - 1)
    dataR1=raw_data[raw_data.iloc[:,0]=='R1']
    samples['Mineralogy'] = dataR1['Sample Type'].values
    samples['Sample name'] = dataR1['Easotope Name'].values
    
    features = ['Sample name','Mineralogy','n','D48 CDES (Final)', 'D48 CDES (Final) SD', 'D48 CDES (Final) SE', 'D48 CDES (Final) @95CL',
                'd13C VPDB (Final)', 'd13C VPDB (Final) SD', 'd13C VPDB (Final) SE', 'd13C VPDB (Final) @95CL',
                'd18O VPDB (Final)', 'd18O VPDB (Final) SD', 'd18O VPDB (Final) SE', 'd18O VPDB (Final) @95CL',
                'D47 CDES (Final)', 'D47 CDES (Final) SD', 'D47 CDES (Final) SE', 'D47 CDES (Final) @95CL']
    samples = samples[features]
    new_columns = ['Sample name','Mineralogy','Nb replicates','D48 I-CDES', 'D48 I-CDES (SD)', 'D48 I-CDES (SE)', 'D48 I-CDES (@95CI)',
                   'd13C VPDB', 'd13C VPDB (SD)', 'd13C VPDB (SE)', 'd13C VPDB (@95CI)',
                   'd18O VPDB (Final)', 'd18O VPDB (SD)', 'd18O VPDB (SE)', 'd18O VPDB (@95CI)',
                   'D47 I-CDES', 'D47 I-CDES (SD)', 'D47 I-CDES (SE)', 'D47 I-CDES (@95CI)']
    samples.columns = new_columns
    if (drop_D48):
        samples.drop(['D48 I-CDES', 'D48 I-CDES (SD)', 'D48 I-CDES (SE)', 'D48 I-CDES (@95CI)'],axis=1,inplace=True)

    samples=calculate_temperature(samples)
    samples = calculate_fluid(samples)
    return samples.drop(['F_eq'], axis=1)

def to_temperature(D47):
    return (0.0391E6/(D47-0.154))**.5-273.15

def calculate_temperature(samples):
    samples['Temperature (˚C)'] = [int(to_temperature(D47)) for D47 in samples['D47 I-CDES']]
    samples['Tmin [+1SE]'] = [int(to_temperature(D47)) for D47 in samples['D47 I-CDES'] + samples['D47 I-CDES (SE)']]
    samples['Tmax [-1SE]'] = [int(to_temperature(D47)) for D47 in samples['D47 I-CDES'] - samples['D47 I-CDES (SE)']]
    samples['Tmin [+95%CI]'] = [int(to_temperature(D47)) for D47 in samples['D47 I-CDES'] + samples['D47 I-CDES (@95CI)']]
    samples['Tmax [-95%CI]'] = [int(to_temperature(D47)) for D47 in samples['D47 I-CDES'] - samples['D47 I-CDES (@95CI)']]
    return samples

def calculate_fluid(samples):
    samples['Fluid equation']= [mineral_dic[mineralogy].feq_name for mineralogy in samples['Mineralogy']]
    samples['F_eq']= [mineral_dic[mineralogy].feq for mineralogy in samples['Mineralogy']]
    rows = [samples[samples['Sample name']==row] for row in samples.index]
    samples['Calculate d18O fluid [VSMOW]']= pd.concat([row['F_eq'][0](row['d18O VPDB (Final)'],row['Temperature (˚C)']) for row in rows])
    samples['d18Omin [±1SE]']= pd.concat([row['F_eq'][0](row['d18O VPDB (Final)']-row['d18O VPDB (SE)'],row['Tmin [+1SE]']) for row in rows])
    samples['d18Omax [±1SE]']= pd.concat([row['F_eq'][0](row['d18O VPDB (Final)']+row['d18O VPDB (SE)'],row['Tmax [-1SE]']) for row in rows])
    samples['d18Omin [±95%CI]']= pd.concat([row['F_eq'][0](row['d18O VPDB (Final)']+row['d18O VPDB (@95CI)'],row['Tmin [+95%CI]']) for row in rows])
    samples['d18Omax [±95%CI]']= pd.concat([row['F_eq'][0](row['d18O VPDB (Final)']-row['d18O VPDB (@95CI)'],row['Tmax [-95%CI]']) for row in rows])
    return samples


def area_builder(Xmin, Xmax, Ymin, Ymax, nb_points=5,function=None):
    Y = np.full((1, nb_points), Ymin)
    Y = np.append(Y, np.linspace(Ymin, Ymax, nb_points))
    Y = np.append(Y, np.full((1, nb_points), Ymax))
    Y = np.append(Y, np.linspace(Ymax, Ymin, nb_points))
    X = np.linspace(Xmin, Xmax, nb_points)
    X = np.append(X, np.full((1, nb_points), Xmax))
    X = np.append(X, np.linspace(Xmax, Xmin, nb_points))
    X = np.append(X, np.full((1, nb_points), Xmin))
    if(function!=None):
        X = function(X, Y)
    points = np.reshape(np.vstack((X, Y)), (2, len(X))).T

    return Polygon(points, closed=True)


def isoplot(data=[], isolines=None, plot_title='Isoplot', x_title='X axis',y_title='Y axis', fig_size=(5, 5),axis=None,
            markers=None,marker_size=5,colors=None,group_names=None):
    if (len(data) > 2):
        if (str(type(data[2][0][0])) == "<class 'matplotlib.patches.Polygon'>"):
            draw_area = True
            error_groups = data[2]
            all_xy = np.concatenate([np.concatenate([value.get_xy() for value in group]) for group in error_groups]).T
            Xmin = all_xy[0].min()
            Xmax = all_xy[0].max()
            Ymin = all_xy[1].min()
            Ymax = all_xy[1].max()
    else:
        draw_area = False
        print("WARNING: No valid error area (matplotlib polygon) found in data. Reverting to no error plot")
        all_x = np.concatenate([[value for value in group] for group in data[0]]).T
        all_y = np.concatenate([[value for value in group] for group in data[1]]).T
        Xmin = all_x.min()
        Xmax = all_x.max()
        Ymin = all_y.min()
        Ymax = all_y.max()

    if(colors==None):
        colors=plt.rcParams['axes.prop_cycle'].by_key()['color']
    if(markers==None):
        symbols=list(range(1,len(data[0])+1))
    else:
        symbols=markers
    if(group_names==None):
        group_names = [f"Group {num}" for num,value in enumerate(data)]

    # First set values for the axis limits and for plotting the isolines to ±5% of the range of expected errors
    XRange = abs(Xmax - Xmin)  # Total range of the X axis
    YRange = abs(Ymax - Ymin)  # Total range of the Y axis
    x_axis_min = Xmin - XRange * 0.05
    x_axis_max = Xmax + XRange * 0.05
    y_axis_min = Ymin - YRange * 0.05
    y_axis_max = Ymax + YRange * 0.05

    if(axis==None):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=fig_size)
    else:
        ax=axis

    ax.set_xlabel(x_title)
    ax.xaxis.set_label_position('top')
    ax.xaxis.tick_top()
    ax.set_ylabel(y_title)
    ax.set_title(plot_title, y=1.2)
    ax.set_xlim(x_axis_min, x_axis_max)
    ax.set_ylim(y_axis_min, y_axis_max)

    x = np.linspace(x_axis_min, x_axis_max, 50)
    y = np.linspace(y_axis_min, y_axis_max, 50)
    X, Y = np.meshgrid(x, y)

    matplotlib.rcParams['contour.negative_linestyle'] = 'solid'
    if(isolines!=None):
        for isoline in isolines:
            Z = isoline(X, Y)
            CSa = ax.contour(X, Y, Z, 6,
                            linewidths=0.5,
                            linestyles='dashed',
                            colors='k', )
            plt.clabel(CSa, inline=1, fontsize=8, fmt='%1.1f')

    if (draw_area):
        plot_data = list(zip(colors,markers,group_names,data[0], data[1], data[2]))
    else:
        plot_data = list(zip(colors,markers,group_names,data[0], data[1]))

    for group in plot_data:
        # First plot error areas as patches
        if (draw_area):
            patches = [item for item in group[5]]
            p = PatchCollection(patches, facecolors=(group[0],), edgecolors=('black',), linewidths=(.25,))
            p.set_alpha(0.2)
            ax.add_collection(p)
        ax.plot(group[3], group[4], marker=group[1], color=group[0],linestyle='None',markersize=marker_size,label=group[2])
        handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, frameon=True, loc=2)
    return ax


def plot_fluid_vs_temperature(samples,use_CI=False, axis=None, groups='Mineralogy',markers=None,marker_size=5,colors=None):
    rows=[samples.loc[index,:] for index in samples.index]
    if (use_CI):
        plot_title = 'Temperature vs Fluid (±95%CI)'
        samples['errorArea'] = [
            area_builder(row['d18O VPDB (Final)']-row['d18O VPDB (@95CI)'],
                         row['d18O VPDB (Final)']+row['d18O VPDB (@95CI)'],
                         row['Tmin [+95%CI]'],row['Tmax [-95%CI]'],
                         function=mineral_dic[row['Mineralogy']].feq) for row in rows]
    else:
        plot_title = 'Temperature vs Fluid (±1SE)'
        samples['errorArea'] = [
            area_builder(row['d18O VPDB (Final)'] - row['d18O VPDB (SE)'],
                         row['d18O VPDB (Final)'] + row['d18O VPDB (SE)'],
                         row['Tmin [+1SE]'], row['Tmax [-1SE]'],
                         function=mineral_dic[row['Mineralogy']].feq) for row in rows]

    groupedData = samples.groupby(groups)
    error_groups = [[value for value in group.values] for name, group in groupedData['errorArea']]
    group_names = [name for name, group in groupedData]
    X = [[value for value in group.values] for name, group in groupedData['Calculate d18O fluid [VSMOW]']]
    Y = [[value for value in group.values] for name, group in groupedData['Temperature (˚C)']]
    lines = [mineral_dic[name].seq for name in samples['Mineralogy'].unique()]
    data = [X, Y, error_groups]
    return isoplot(data=data, isolines=lines, plot_title=plot_title, x_title='$\delta^{18}O_{Water\>VSMOW\>[‰]}$',
                   y_title='Temperature [˚C]', fig_size=(6, 6),axis=axis,markers=markers,marker_size=marker_size,
                   colors=colors,group_names=group_names)

def plot_bulk(samples,use_CI=False, axis=None, groups='Mineralogy',markers=None,marker_size=5,colors=None):
    rows = [samples.loc[index, :] for index in samples.index]
    if (use_CI):
        plot_title = '$\delta^{18}O_{Mineral} vs \delta^{13}C_{Mineral}$ (±95%CI)'
        samples['errorArea'] = [
            area_builder(row['d18O VPDB (Final)'] - row['d18O VPDB (@95CI)'],
                         row['d18O VPDB (Final)'] + row['d18O VPDB (@95CI)'],
                         row['d13C VPDB'] - row['d13C VPDB (@95CI)'],
                         row['d13C VPDB'] + row['d13C VPDB (@95CI)']) for row in rows]

    else:
        plot_title = '$\delta^{18}O_{Mineral} vs \delta^{13}C_{Mineral}$ (±1SD)'
        samples['errorArea'] = [
            area_builder(row['d18O VPDB (Final)'] - row['d18O VPDB (SD)'],
                         row['d18O VPDB (Final)'] + row['d18O VPDB (SD)'],
                         row['d13C VPDB'] - row['d13C VPDB (SD)'],
                         row['d13C VPDB'] + row['d13C VPDB (SD)']) for row in rows]

    groupedData = samples.groupby(groups)
    error_groups = [[value for value in group.values] for name, group in groupedData['errorArea']]
    group_names = [name for name, group in groupedData]
    X = [[value for value in group.values] for name, group in groupedData['d18O VPDB (Final)']]
    Y = [[value for value in group.values] for name, group in groupedData['d13C VPDB']]
    data = [X, Y, error_groups]
    return isoplot(data=data, plot_title=plot_title, x_title='$\delta^{18}O_{Mineral\>VPDB\>[‰]}$',
                   y_title='$\delta^{13}C_{Mineral\>VPDB\>[‰]}$', fig_size=(6, 6), axis=axis, markers=markers, marker_size=marker_size,
                   colors=colors, group_names=group_names)



