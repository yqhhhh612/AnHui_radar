import numpy as np
def map_with_radar(refarray, longitude, latitude, savepath=None, d=''):
    '''
    :param rawarray:
    :param corarray:
    :param longitude:
    :param latitude:
    :param savepath:
    :param d:
    :return:
    '''
    import numpy as np
    from matplotlib import pyplot as plt
    import matplotlib as mpl
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature
    import matplotlib.ticker as mticker
    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
    from cartopy.io.shapereader import Reader
    def recolormaps_0():
        import matplotlib.colors as colors
        cdict = ['#00BFFF',
                 '#1E90FF',
                 '#0000CD',
                 'lime',
                 'limegreen',
                 'green',
                 'yellowgreen',
                 '#FFD700',
                 '#DAA520',
                 '#FF3030',
                 '#CD3333',
                 '#8B2323',
                 '#CD2626',
                 '#FF00FF',
                 '#800080',
                 '#000000']
        return (colors.ListedColormap(cdict, "indexed"))

    def colormaps_1():
        import matplotlib.colors as colors
        cdict = [(0, 1, 1),
                 (0, 157 / 255, 1),
                 (0, 0, 1),
                 (9 / 255, 130 / 255, 175 / 255),
                 'palegreen',
                 (0, 1, 0),
                 (8 / 255, 175 / 255, 20 / 255),
                 (1, 214 / 255, 0),
                 (1, 152 / 255, 0),
                 (1, 0, 0),
                 (221 / 255, 0, 27 / 255),
                 (188 / 255, 0, 54 / 255),
                 (121 / 255, 0, 109 / 255),
                 (121 / 255, 51 / 255, 160 / 255),
                 (195 / 255, 163 / 255, 212 / 255)]
        return (colors.ListedColormap(cdict, "indexed"))

    def colormaps_16():
        import matplotlib.colors as colors
        cdict = [(0, 157 / 255, 1),
                 (0, 0, 1),
                 (9 / 255, 130 / 255, 175 / 255),
                 'palegreen',
                 (0, 1, 0),
                 (8 / 255, 175 / 255, 20 / 255),
                 '#FFFF66',
                 (1, 214 / 255, 0),
                 (1, 152 / 255, 0),
                 (1, 0, 0),
                 (221 / 255, 0, 27 / 255),
                 (188 / 255, 0, 54 / 255),
                 (121 / 255, 0, 109 / 255),
                 (121 / 255, 51 / 255, 160 / 255),
                 (195 / 255, 163 / 255, 212 / 255)]
        return (colors.ListedColormap(cdict, "indexed"))

    bartick = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70,75]

    mpl.rcParams['font.sans-serif'] = ['FangSong']
    mpl.rcParams['axes.unicode_minus'] = False
    config = {"font.family": 'Times New Roman'}
    mpl.rcParams.update(config)
    corref = refarray
    ccr_longitude = longitude
    ccr_latitude = latitude

    proj = ccrs.PlateCarree()  # 创建投影，选择cartopy的platecarree投影
    shp_path = r"F:\毕业论文图\第五章\anhuiouter.shp"
    provinces = cfeature.ShapelyFeature(Reader(shp_path).geometries(), proj, edgecolor='k',
                                        facecolor='none', alpha=0.7)
    xticks = np.arange(114.5, 120.1, 1)
    yticks = np.arange(29, 35, 0.5)
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.add_feature(provinces, linewidth=0.6, zorder=2)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linewidth=1, color='k', alpha=0.5, linestyle='--',zorder=1)
    gl.xlocator = mticker.FixedLocator(xticks)
    gl.ylocator = mticker.FixedLocator(yticks)
    ax.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax.set_xticklabels(xticks, fontsize=16)  # 设置刻度字体大小
    ax.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax.set_yticklabels(yticks, fontsize=16)  # 设置刻度字体大小
    ax.set_extent([114.5, 120.1, 29, 35])
    ax.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label=True))
    ax.yaxis.set_major_formatter(LatitudeFormatter())
    pl = ax.contourf(ccr_longitude, ccr_latitude, corref, np.arange(0, 76, 5), cmap=colormaps_16(),zorder=2)
    # ax.annotate(d, xy=(0.05, 0.9), xycoords='axes fraction', fontsize=25)
    # ax.text(0.05,0.95,'(a)',fontsize=10)
    ax.set_xlabel('longitude',fontsize=18)
    ax.set_ylabel('latitude',fontsize=18)
    gl.xlabel_style = {'size': 6}
    gl.ylabel_style = {'size': 6}
    cb = plt.colorbar(pl, shrink=0.9,pad=0.03)
    font = {'family': 'Times New Roman',
            'color': 'k',
            'weight': 'normal',
            'size': 16,
            }
    cb.ax.tick_params(labelsize=16)
    #cb.set_label('dBZ', fontdict=font)
    cb.set_ticks(bartick)
    ax4 = cb.ax
    ax4.set_title('dBZ',fontdict=font)
    plt.tight_layout()
    if savepath:
        plt.savefig(savepath, dpi=400)
    plt.show()
