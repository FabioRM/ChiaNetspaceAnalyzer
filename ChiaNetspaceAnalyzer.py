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
        318.02349677504566,
        298.4630881959869,
        323.7620017660785,
        281.0575469898744,
        272.44616233854015,
        245.23100115625434,
        287.3891414732488,
        259.7967979558775,
        255.70644615764243,
        280.2134090540314,
        281.2560727959075,
        249.96923232727138,
        245.8905658555583,
        274.97462514058975,
        257.1903668953533,
        243.48174908623892,
        256.99640476895524,
        229.74906452835032,
        235.99640393978646,
        221.78738822923629,
        243.9709002874626,
        211.98341496431416,
        243.80574403062676,
        196.99469391520864,
        225.11355794918578,
        218.37122347508821,
        183.58391164183928,
        205.73228279232106,
        199.38244081055603,
        194.19608378705524,
        204.0843799409051,
        243.67865592781462,
        183.72679473218088,
        208.3804327004985,
        190.56839820330327,
        185.89516761347787,
        175.41044288865248,
        167.75592492685752,
        201.98306246596684,
        190.25325136315863,
        198.30229944076265,
        182.29796877285804,
        183.44350638684747,
        175.04596025150798,
        169.65613117168303,
        168.96031389237694,
        161.89193031711312,
        166.45754579389123,
        173.29542124589523,
        166.94296388832578,
        161.34197398721292,
        168.56016974415326,
        160.7533744344109,
        169.72431903881088,
        153.83171452410963,
        155.6649078594473,
        149.11241313965283,
        144.6769903949693,
        149.2722549069959,
        153.5145180255023,
        153.9232399375241,
        132.98641036959214,
        149.56066653097537,
        138.95379108572197,
        147.91901729319721,
        126.8202529038104,
        129.98825128999368,
        150.53943404605553,
        130.49364617201192,
        132.0295939162696,
        133.57318770301208,
        129.67926022121853,
        141.8226087435112,
        135.06395129057947,
        124.76175882410284,
        114.1688805479072,
    ],
    "timestamp": [
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
        1618293101000,
        1618271463000,
        1618228359000,
        1618208004000,
        1618185156000,
        1618164180000,
        1618141900000,
        1618098712000,
        1618077111000,
        1618033930000,
        1618012757000,
        1617990730000,
        1617969085000,
        1617949019000,
        1617925913000,
        1617905074000,
        1617882742000,
        1617861096000,
        1617817956000,
        1617796293000,
        1617778057000,
        1617753137000,
        1617731508000,
        1617688351000,
        1617645128000,
        1617624900000,
        1617601961000,
        1617581835000,
        1617558755000,
        1617537087000,
        1617515469000,
        1617496949000,
        1617472333000,
        1617451144000,
        1617429174000,
        1617407514000,
        1617364338000,
        1617342688000,
        1617299568000,
        1617278324000,
        1617256341000,
        1617234719000,
        1617213073000,
        1617192475000,
        1617169965000,
        1617148652000,
        1617126746000,
        1617105107000,
        1617084468000,
        1617061908000,
        1617018737000,
        1616975546000,
        1616943336000,
        1616923011000,
        1616902596000,
        1616882020000,
        1616845933000,
        1616824459000,
        1616802776000,
        1616759548000,
        1616739054000,
        1616716314000,
        1616696070000,
        1616673107000,
        1616652864000,
        1616629932000,
        1616608251000,
        1616565143000,
        1616543518000,
        1616521891000,
        1616500290000,
        1616478798000,
        1616457159000,
        1616435529000,
        1616413914000,
        1616393470000,
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
