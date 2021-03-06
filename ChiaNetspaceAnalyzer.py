import sys, time, os
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker
import numpy as np
from scipy.signal import savgol_filter
from matplotlib import gridspec
import requests
import json

# I retrieve the data from chiaexplorer.com, there is an issue providing the new users API keys, so I simply dump the json from a browser
# and I copy-paste into "netspace_data"
DATA_REQUEST_API = "https://api2.chiaexplorer.com/chart/netSpace?period=3m"

netspace_data = {
    "data": [
        32277.252393560855,
        32625.966267184485,
        32239.74718936489,
        31431.699207382106,
        31327.529322522776,
        31013.922403233857,
        31093.176297484843,
        31652.572923796604,
        32130.212656515803,
        31943.562999455993,
        31453.838688775053,
        31229.100596881875,
        30860.65337256952,
        30834.659010189276,
        31571.075186711492,
        31795.07381244658,
        30983.00971289138,
        30889.375137762767,
        30894.752441141,
        30770.606020421215,
        30505.219306780375,
        30410.038848387758,
        30527.757634947346,
        30834.250551404697,
        31145.748103829552,
        30719.808278252334,
        31222.432707880027,
        30062.795386403366,
        29754.5815267835,
        29264.66634581742,
        29348.877641021314,
        29355.951212203454,
        29713.446777405312,
        29592.264971643985,
        29104.072666222743,
        29098.413176007198,
        29535.3353808842,
        28878.15701334792,
        28926.615726978343,
        28488.316833716875,
        28665.11798548697,
        28713.842234503638,
        28838.465870869368,
        28784.521526523014,
        27707.437327434083,
        27515.1636292638,
        27346.836552263067,
        26934.38794477851,
        27806.227033689604,
        27782.002861369376,
        27340.018991618443,
        27416.60594996945,
        26903.604230277153,
        26898.698531858805,
        26838.545601446185,
        27102.004730223733,
        27222.80204821056,
        26839.482188832237,
        27202.676812522244,
        26718.036328888164,
        27105.90961873112,
        27454.86675063922,
        27846.81127317473,
        27262.82210769158,
        26734.733527674252,
        26469.151711337094,
        25777.67576495656,
        25381.36350740404,
        24718.924423536697,
        25148.41954812445,
        25335.31300807172,
        25205.304415094077,
        24585.666785664398,
        24454.129721854766,
        24323.18125387863,
        24519.754040330947,
        24834.38760484068,
        24779.78563698452,
        24622.446300075586,
        24503.265790373967,
        23971.5092581444,
        24026.063113492946,
        23314.08186706296,
        23061.725268652517,
        23220.064226127346,
        22923.06649919901,
        22812.39152824512,
        22573.825738326796,
        21742.008481235254,
        21716.343561193757,
        21756.851294964086,
        21848.492725527143,
        21205.33766454223,
        21093.58272856308,
        20749.139338112655,
        20295.462153208347,
        20160.727788034827,
        20184.173373028647,
        20525.611572804894,
        20416.66936031352,
        20138.98931828366,
        19500.83985009724,
        19432.87305265995,
        19487.23083088118,
        19381.473077117073,
        18826.44427957928,
        18598.10873686959,
        18400.208903242663,
        18413.313133984873,
        18462.893471024883,
        18127.569453961845,
        17947.62518864177,
        17671.877456050577,
        17340.771315406968,
        17013.79060732866,
        16896.718526364883,
        16833.580859414094,
        16642.270217692636,
        16364.457782274809,
        16134.375644332178,
        15963.263240511933,
        15589.83868632673,
        15533.604294277156,
        15681.882303740907,
        15591.882809923743,
        15660.825246306533,
        15425.514798747998,
        14858.378641657777,
        14685.253449486996,
        14142.602347124413,
        13822.128770350711,
        13948.690163323896,
        13935.309231428286,
        13320.6469285296,
        12825.474923027532,
        12509.638748786614,
        12299.806600348771,
        12141.795822566464,
        12088.274550231627,
        12177.255583615106,
        12329.412618503515,
        12130.3501254275,
        12014.276180645447,
        11478.695100598161,
        11174.715895443525,
        10788.475715791063,
        10642.628098528145,
        10504.487363765345,
        10520.406404113293,
        10288.237933247821,
        10020.718210681469,
        9813.518520011767,
        9575.601774597857,
        9327.891374458099,
        9010.15586561335,
        8707.672396018812,
        8660.939578018693,
        8530.954407355179,
        8203.475043829534,
        8032.094076695273,
        7789.87433152974,
        7699.376363863789,
        7273.191992218846,
        7113.368503388587,
        7144.12947045133,
        6917.188236730338,
        6771.138775893796,
        6675.79046234339,
        6525.040278222508,
        6486.978485485715,
        6457.157759808921,
        6342.264273815981,
        6217.83354028952,
        6103.595682343957,
        5965.090369780206,
        5864.524316875572,
        5758.022443510796,
        5571.74890331005,
        5391.070002083748,
        5327.240341507346,
        5133.342740365562,
        5021.788177878253,
        5032.673861650741,
        4877.777020786293,
        4783.141147076541,
        4638.4666712229,
        4545.98891232017,
        4354.534085615982,
        4286.848498953576,
        4148.297239899384,
        4114.288666283791,
        4010.134986911127,
        3954.03481309894,
        3820.95486127796,
        3686.8199288633027,
        3511.357792045685,
        3403.152037945572,
        3279.4702347112234,
        3188.5170440520565,
        2749.231472321997,
        2709.446780771417,
        2774.5583301172155,
        3001.008047785126,
        3219.636031365734,
        3209.1647108092675,
        3140.890806384099,
        3024.682019790328,
        2949.6886467675026,
        2905.7544310728204,
        2787.7069398707354,
        2747.1414689659096,
        2730.6648648653063,
        2686.834845350774,
        2669.5638616286574,
        2577.3633625033485,
        2533.4736015442118,
        2448.9878466660925,
        2398.1552064130988,
        2312.5944503742903,
        2186.773798357013,
        2165.744547093934,
        2108.025585046967,
        2074.959133249879,
        1907.1724132530956,
        1845.911030021973,
        1756.0085707466617,
        1767.1820626661654,
        1725.8829577299962,
        1708.7979820987591,
        1637.0970016637532,
        1580.3804306073314,
        1529.3605913723538,
        1504.4910722095058,
        1445.6893444914651,
        1382.4528829065737,
        1350.5095202199695,
        1331.898956382609,
        1285.497497902097,
        1249.364773450565,
        1211.9137922145546,
        1180.864438665199,
        1205.7325482976262,
        1148.8461025310082,
        1015.172236425895,
        1143.8120481376702,
        955.07673571086,
        952.9747587979228,
        980.0444379967397,
        899.61323418679,
        778.1077070450044,
        853.6915947293768,
        972.7775391918857,
        793.1586601029773,
        777.4417159408165,
        786.343888660111,
        729.44533287393,
        691.5985900231976,
        697.505761908699,
        608.6804959939057,
        710.3986805515777,
        667.7903269950259,
        576.1389616581394,
        646.2908286539883,
        558.5561252942902,
        536.3412416939908,
        582.8963199263225,
        598.495489482827,
        526.0592549959454,
        500.9011089470702,
        473.89807028982756,
        498.72256037255306,
        463.16380827596055,
        468.33701775396435,
        450.8075135396319,
        383.6691634935944,
        435.086279608251,
        386.2970201935174,
        393.02411001587257,
        409.80083595887015,
        351.91045028347975,
        407.3233243177113,
        381.8131739621773,
        390.6942925523751,
        343.3274339994536,
        369.5584673087047,
        333.00517454473396,
        363.7915124749029,
        316.74357292792365,
        373.1123235906965,
        311.48057974964166,
        309.3542334270891,
        344.59177992737557,
        322.0862493960561,
        323.7158364923876,
        295.7831092947227,
        300.7753678699554,
        346.1414964234766,
        294.2636119505798,
        277.7145660278394,
        298.03891179084917,
        289.04283413575763,
    ],
    "timestamp": [
        1626112334000,
        1626069156000,
        1626025911000,
        1626004292000,
        1625982683000,
        1625961454000,
        1625939527000,
        1625896329000,
        1625874705000,
        1625831540000,
        1625809932000,
        1625788323000,
        1625745091000,
        1625723440000,
        1625680341000,
        1625658700000,
        1625615557000,
        1625593929000,
        1625550699000,
        1625507519000,
        1625464363000,
        1625421113000,
        1625377943000,
        1625356311000,
        1625334710000,
        1625313711000,
        1625291538000,
        1625271076000,
        1625248302000,
        1625205162000,
        1625183544000,
        1625140340000,
        1625097135000,
        1625053927000,
        1625010732000,
        1624989114000,
        1624945940000,
        1624902762000,
        1624859513000,
        1624837886000,
        1624794765000,
        1624751522000,
        1624729909000,
        1624709445000,
        1624686740000,
        1624665130000,
        1624643503000,
        1624622876000,
        1624600289000,
        1624578812000,
        1624557142000,
        1624535536000,
        1624492356000,
        1624470688000,
        1624427543000,
        1624405927000,
        1624384319000,
        1624363133000,
        1624341143000,
        1624319513000,
        1624297880000,
        1624254725000,
        1624233044000,
        1624212799000,
        1624189920000,
        1624169009000,
        1624146759000,
        1624103536000,
        1624081911000,
        1624060299000,
        1624017164000,
        1623995555000,
        1623973890000,
        1623952282000,
        1623909126000,
        1623887486000,
        1623844332000,
        1623822702000,
        1623801098000,
        1623779602000,
        1623757958000,
        1623736284000,
        1623693152000,
        1623649960000,
        1623606741000,
        1623585157000,
        1623563514000,
        1623520335000,
        1623477129000,
        1623455474000,
        1623412326000,
        1623390693000,
        1623347585000,
        1623325930000,
        1623304773000,
        1623282716000,
        1623239533000,
        1623217919000,
        1623196277000,
        1623153119000,
        1623131478000,
        1623109877000,
        1623088473000,
        1623066740000,
        1623023535000,
        1623003357000,
        1622980338000,
        1622958708000,
        1622915515000,
        1622893893000,
        1622872373000,
        1622850708000,
        1622829100000,
        1622807426000,
        1622764357000,
        1622742742000,
        1622721105000,
        1622699502000,
        1622656319000,
        1622634717000,
        1622614142000,
        1622591560000,
        1622569931000,
        1622548769000,
        1622526753000,
        1622505137000,
        1622483521000,
        1622462895000,
        1622440344000,
        1622397136000,
        1622353940000,
        1622332283000,
        1622289145000,
        1622245967000,
        1622202739000,
        1622181100000,
        1622159812000,
        1622137980000,
        1622116391000,
        1622094727000,
        1622073119000,
        1622051470000,
        1622030923000,
        1622008366000,
        1621987364000,
        1621965152000,
        1621943551000,
        1621921929000,
        1621878718000,
        1621857113000,
        1621813934000,
        1621792312000,
        1621772182000,
        1621749073000,
        1621728840000,
        1621705945000,
        1621684299000,
        1621662652000,
        1621643333000,
        1621619566000,
        1621597904000,
        1621575941000,
        1621532977000,
        1621489801000,
        1621467984000,
        1621425056000,
        1621403075000,
        1621382154000,
        1621360214000,
        1621338608000,
        1621317461000,
        1621295422000,
        1621274546000,
        1621252222000,
        1621230327000,
        1621208683000,
        1621187068000,
        1621167086000,
        1621143941000,
        1621122940000,
        1621101024000,
        1621080539000,
        1621057852000,
        1621037073000,
        1621014730000,
        1620993092000,
        1620971447000,
        1620928293000,
        1620908504000,
        1620885133000,
        1620863482000,
        1620844263000,
        1620820334000,
        1620798701000,
        1620778592000,
        1620755529000,
        1620733882000,
        1620712261000,
        1620693921000,
        1620669118000,
        1620647503000,
        1620625874000,
        1620582776000,
        1620561133000,
        1620539490000,
        1620518585000,
        1620496290000,
        1620475374000,
        1620453143000,
        1620431528000,
        1620409908000,
        1620388277000,
        1620366972000,
        1620345111000,
        1620325272000,
        1620301923000,
        1620280296000,
        1620260833000,
        1620237148000,
        1620215504000,
        1620195932000,
        1620172348000,
        1620151299000,
        1620129121000,
        1620110542000,
        1620085926000,
        1620042726000,
        1620021119000,
        1619999475000,
        1619979308000,
        1619956336000,
        1619936457000,
        1619913149000,
        1619891543000,
        1619873331000,
        1619848290000,
        1619826800000,
        1619805124000,
        1619783493000,
        1619762834000,
        1619740335000,
        1619718734000,
        1619699461000,
        1619675573000,
        1619653913000,
        1619637036000,
        1619610769000,
        1619578972000,
        1619545943000,
        1619524335000,
        1619481162000,
        1619460478000,
        1619437932000,
        1619416321000,
        1619397425000,
        1619373109000,
        1619353596000,
        1619329906000,
        1619308305000,
        1619287474000,
        1619265149000,
        1619245385000,
        1619221963000,
        1619200342000,
        1619178720000,
        1619160021000,
        1619135560000,
        1619113921000,
        1619092315000,
        1619049134000,
        1619030429000,
        1619005950000,
        1618986228000,
        1618962746000,
        1618942543000,
        1618919520000,
        1618899589000,
        1618876351000,
        1618854683000,
        1618833619000,
        1618811516000,
        1618790925000,
        1618768337000,
        1618746713000,
        1618725980000,
        1618703540000,
        1618660370000,
        1618638662000,
        1618617533000,
        1618595546000,
        1618573937000,
        1618552292000,
        1618531376000,
        1618509125000,
        1618487518000,
        1618466939000,
        1618444349000,
        1618422705000,
        1618379565000,
        1618358294000,
        1618336347000,
    ],
}

timestamps = netspace_data["timestamp"]
netspace = netspace_data["data"]

timestamps.reverse()
netspace.reverse()

timestamps_datetime = []

for timestamp in timestamps:
    timestamps_datetime.append(datetime.datetime.fromtimestamp(timestamp / 1000))

delta_increment = [0]
for i in range(len(netspace) - 1):
    delta_increment.append(netspace[i + 1] - netspace[i])

delta_increment_smooth = savgol_filter(
    delta_increment, 51, 2
)  # window size 51, polynomial order 2

daily_increase = []
increase_percentage_daily = []
for i in range(len(netspace)):
    how_many_entries = 0
    for j in range(i, len(netspace)):
        if timestamps_datetime[j] < (
            timestamps_datetime[i] + datetime.timedelta(days=1)
        ):
            how_many_entries += 1
        else:
            break
    daily_increase.append(netspace[j] - netspace[i])
    increase_percentage_daily.append(((netspace[j] - netspace[i]) / netspace[i]) * 100)

increase_percentage_daily_smooth = savgol_filter(
    increase_percentage_daily, 51, 2
)  # window size 51, polynomial order 3

daily_increase_smooth = savgol_filter(
    daily_increase, 51, 2
)  # window size 51, polynomial order 2

valid_increase_index = 0
while timestamps_datetime[valid_increase_index] < (
    timestamps_datetime[-1] - datetime.timedelta(days=1)
):
    valid_increase_index += 1

fig = plt.figure()
# set height ratios for subplots
gs = gridspec.GridSpec(2, 1, height_ratios=[1, 1])

# the first subplot
ax0 = plt.subplot(gs[0])
(line0,) = ax0.plot(timestamps_datetime, netspace, color="tab:red")
plt.gcf().autofmt_xdate()
plt.grid()
plt.ylabel("Netspace (PiB)", color="tab:red")
plt.tick_params(axis="y", labelcolor="tab:red")

# the second subplot
# shared axis X
# ax1 = plt.subplot(gs[1], sharex=ax0)
ax1 = ax0.twinx()
(line2,) = ax1.plot(
    timestamps_datetime[:valid_increase_index],
    daily_increase[:valid_increase_index],
    color="gainsboro",
)

(line1,) = ax1.plot(
    timestamps_datetime[:valid_increase_index],
    daily_increase_smooth[:valid_increase_index],
    color="tab:green",
)

nticks = 7
ax0.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(nticks))
ax1.yaxis.set_major_locator(matplotlib.ticker.LinearLocator(nticks))

# (line2,) = ax1.plot(timestamps_datetime, delta_increment, color="g")
plt.setp(ax1.get_xticklabels(), visible=False)
plt.grid()
plt.ylabel("Daily increase (PiB)", color="tab:green")
plt.tick_params(axis="y", labelcolor="tab:green")
# remove last tick label for the second subplot
yticks = ax1.yaxis.get_major_ticks()
yticks[-1].label1.set_visible(False)

# the third plot
# increase_percentage = []
# for i in range(len(netspace)):
#     increase_percentage.append((delta_increment_smooth[i] / netspace[i]) * 100)

# increase_percentage_smooth = savgol_filter(
#     increase_percentage, 51, 2
# )  # window size 51, polynomial order 3

# # shared axis X
# ax2 = plt.subplot(gs[2], sharex=ax0)
# (line3,) = ax2.plot(timestamps_datetime, increase_percentage_smooth, color="y")
# # (line4,) = ax2.plot(timestamps_datetime, increase_percentage, color="c")
# plt.setp(ax0.get_xticklabels(), visible=True)
# plt.grid()
# plt.ylabel("Increase percentage smooth")
# # remove last tick label for the second subplot
# yticks = ax2.yaxis.get_major_ticks()
# yticks[-1].label1.set_visible(True)

# the fourth plot


# shared axis X
ax3 = plt.subplot(gs[1], sharex=ax0)

(line4,) = ax3.plot(
    timestamps_datetime[:valid_increase_index],
    increase_percentage_daily[:valid_increase_index],
    color="gainsboro",
)
(line3,) = ax3.plot(
    timestamps_datetime[:valid_increase_index],
    increase_percentage_daily_smooth[:valid_increase_index],
    color="tab:olive",
)

plt.setp(ax0.get_xticklabels(), visible=False)
plt.grid()
plt.ylabel("Daily increase (%)")
# remove last tick label for the second subplot
yticks = ax3.yaxis.get_major_ticks()


# Major ticks every 6 months.
fmt_half_year = mdates.DayLocator(interval=7)
ax3.xaxis.set_major_locator(fmt_half_year)

# Minor ticks every day.
fmt_month = mdates.DayLocator()
ax3.xaxis.set_minor_locator(fmt_month)

yticks[-1].label1.set_visible(True)

# put legend on first subplot
# ax0.legend(
#     (line0, line1, line3, line4),  # , line4),
#     (
#         "Netspace",
#         "Daily increase",
#         "Increase percentage",
#         "Increase percentage daily",
#     ),
#     loc="lower left",
# )

# remove vertical gap between subplots
plt.subplots_adjust(hspace=0.0)

# Rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them.
fig.autofmt_xdate()

fig.suptitle("Chia network analysis", fontsize=16)
fig.tight_layout()
plt.show()

# plot
# plt.plot(timestamps_datetime, netspace)
# beautify the x-labels
# plt.gcf().autofmt_xdate()
# plt.show()


# plot
# plt.plot(delta_increment)
# plt.plot(delta_increment_smooth)

# plt.show()
