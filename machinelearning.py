from Model import *
from server import app
from statistics import stdev, mean
import numpy as np
from sklearn.decomposition import RandomizedPCA


def get_ml_variance():
    raw_metrics = Metrics.query.all()
    all_metrics = []
    for m in raw_metrics:
        all_metrics.append([m.common_percent, m.poem_percent, m.object_percent,
                            m.abs_percent, m.male_percent, m.female_percent,
                            m.positive, m.negative, m.active_percent,
                            m.passive_percent])

    data = np.array(all_metrics)
    pca = RandomizedPCA(n_components=35, whiten=True)
    pca.fit(data)
    print pca.explained_variance_ratio_


# ALL_DATA = [wl_mean, wl_median, wl_mode, wl_range,
#             ll_mean, ll_median, ll_mode, ll_range,
#             pl_char, pl_lines, pl_words, lex_div,
#             the_freq, i_freq, you_freq, is_freq,
#             a_freq, common_percent, poem_percent,
#             object_percent, abs_percent, male_percent,
#             female_percent, alliteration, positive,
#             negative, active_percent, passive_percent,
#             end_repeat, rhyme, stanzas, sl_mean,
#             sl_median, sl_mode, sl_range]
#
# [  9.55859983e-01   4.02620230e-02   2.96296966e-03   3.62716787e-04
#    2.90938678e-04   1.18473649e-04   7.92189567e-05   2.95101148e-05
#    1.85388873e-05   1.38932828e-05   1.01237361e-06   4.08035174e-07
#    1.32175568e-07   9.64903773e-08   4.64330193e-08   2.49486072e-08
#    1.00339696e-08   1.32597728e-09   9.27496335e-10   8.31346992e-10
#    3.21871618e-10   1.10993395e-10   9.12709628e-11   6.69867133e-11
#    4.33404832e-11   3.73831349e-11   3.40174367e-11   3.12406615e-11
#    2.71156501e-11   2.53683078e-11   2.45387798e-11   2.12365609e-11
#    1.86070603e-11   1.53287289e-11   1.18505123e-11]
#
#
#
# MACRO_DATA = [wl_mean, wl_median, wl_mode, wl_range,
#               ll_mean, ll_median, ll_mode, ll_range,
#               pl_char, pl_lines, pl_words, lex_div,
#               stanzas, sl_mean, sl_median, sl_mode, sl_range]
#
# [  9.55860036e-01   4.02620244e-02   2.96296966e-03   3.62713961e-04
#    2.90938693e-04   1.18473595e-04   7.92184616e-05   2.95092850e-05
#    1.85387507e-05   1.38930627e-05   1.01227987e-06   4.07997388e-07
#    1.32118204e-07   9.64806050e-08   2.48617229e-08   1.00408288e-08
#    6.72140400e-10]
#
#
#
#
# MICRO_DATA = [the_freq, i_freq, you_freq, is_freq,
#               a_freq, alliteration, rhyme, end_repeat]
#
# [  9.60648786e-01   2.56594341e-02   1.09341909e-02   1.35713841e-03
#    5.09746743e-04   4.21486041e-04   2.80931632e-04   1.88286077e-04]
#
#
#
#
#
# SENTIMENT_DATA = [common_percent, poem_percent, object_percent,
#                   abs_percent, male_percent, female_percent,
#                   positive, negative, active_percent,
#                   passive_percent]
#
# [ 0.71876236  0.06852716  0.06106138  0.03105095  0.02618719  0.02459101
#   0.02024865  0.01886186  0.01786209  0.01284735]
#
#
#
#
#
#
# SENTMICRO_DATA = [the_freq, i_freq, you_freq, is_freq,
#                   a_freq, alliteration, rhyme, end_repeat,
#                   common_percent, poem_percent, object_percent,
#                   abs_percent, male_percent, female_percent,
#                   positive, negative, active_percent,
#                   passive_percent]
#
# [  9.42266609e-01   2.51875469e-02   1.38982426e-02   1.06137637e-02
#    1.68266519e-03   1.32122095e-03   9.50123890e-04   6.12235034e-04
#    5.18841396e-04   4.79550033e-04   4.38441725e-04   3.80404411e-04
#    3.54104554e-04   3.41209996e-04   3.07699842e-04   2.59482206e-04
#    2.18081676e-04   1.69777102e-04]
#
# GAVE SAME NUMBERS WHEN REVERSED
# [m.common_percent, m.poem_percent, m.object_percent,
#  m.abs_percent, m.male_percent, m.female_percent,
#  m.positive, m.negative, m.active_percent,
#  m.passive_percent, m.the_freq, m.i_freq, m.you_freq,
#  m.is_freq, m.a_freq, m.alliteration, m.rhyme,
#  m.end_repeat]
#
#


def get_metrics_dist():
    metrics = Metrics.query.all()
    met_dict = {
        "wl_mean": {"all": sorted([m.wl_mean for m in metrics])},
        "wl_median": {"all": sorted([m.wl_median for m in metrics])},
        "wl_mode": {"all": sorted([m.wl_mode for m in metrics])},
        "wl_range": {"all": sorted([m.wl_range for m in metrics])},
        "ll_mean": {"all": sorted([m.ll_mean for m in metrics])},
        "ll_median": {"all": sorted([m.ll_median for m in metrics])},
        "ll_mode": {"all": sorted([m.ll_mode for m in metrics])},
        "ll_range": {"all": sorted([m.ll_range for m in metrics])},
        "pl_char": {"all": sorted([m.pl_char for m in metrics])},
        "pl_lines": {"all": sorted([m.pl_lines for m in metrics])},
        "pl_words": {"all": sorted([m.pl_words for m in metrics])},
        "lex_div": {"all": sorted([m.lex_div for m in metrics])},
        "the_freq": {"all": sorted([m.the_freq for m in metrics])},
        "i_freq": {"all": sorted([m.i_freq for m in metrics])},
        "you_freq": {"all": sorted([m.you_freq for m in metrics])},
        "is_freq": {"all": sorted([m.is_freq for m in metrics])},
        "a_freq": {"all": sorted([m.a_freq for m in metrics])},
        "common_percent": {"all": sorted([m.common_percent for m in metrics])},
        "poem_percent": {"all": sorted([m.poem_percent for m in metrics])},
        "object_percent": {"all": sorted([m.object_percent for m in metrics])},
        "abs_percent": {"all": sorted([m.abs_percent for m in metrics])},
        "male_percent": {"all": sorted([m.male_percent for m in metrics])},
        "female_percent": {"all": sorted([m.female_percent for m in metrics])},
        "alliteration": {"all": sorted([m.alliteration for m in metrics])},
        "positive": {"all": sorted([m.positive for m in metrics])},
        "negative": {"all": sorted([m.negative for m in metrics])},
        "active_percent": {"all": sorted([m.active_percent for m in metrics])},
        "passive_percent": {"all": sorted([m.passive_percent for m in metrics])},
        "end_repeat": {"all": sorted([m.end_repeat for m in metrics])},
        "rhyme": {"all": sorted([m.rhyme for m in metrics])},
        "stanzas": {"all": sorted([m.stanzas for m in metrics])},
        "sl_mean": {"all": sorted([m.sl_mean for m in metrics])},
        "sl_median": {"all": sorted([m.sl_median for m in metrics])},
        "sl_mode": {"all": sorted([m.sl_mode for m in metrics])},
        "sl_range": {"all": sorted([m.sl_range for m in metrics])}
    }

    for key in met_dict.keys():
        print "\n{}:".format(key.upper())
        met_dict[key]["st_dev"] = stdev(met_dict[key]["all"])
        dev = met_dict[key]["st_dev"]
        print "Standard Deviation: {}".format(dev)

        met_dict[key]["bottom_ten"] = {}
        met_dict[key]["bottom_ten"]["all"] = met_dict[key]["all"][:1041]
        met_dict[key]["bottom_ten"]["min"] = min(met_dict[key]["bottom_ten"]["all"])
        mini = met_dict[key]["bottom_ten"]["min"]
        met_dict[key]["bottom_ten"]["max"] = max(met_dict[key]["bottom_ten"]["all"])
        maxi = met_dict[key]["bottom_ten"]["max"]
        ave = mean(met_dict[key]["bottom_ten"]["all"])
        print "Bottom 10th Percentile:"
        print "          {} to {}. Mean: {}".format(mini, maxi, ave)

        met_dict[key]["bottom_twent"] = {}
        met_dict[key]["bottom_twent"]["all"] = met_dict[key]["all"][:2081]
        met_dict[key]["bottom_twent"]["min"] = min(met_dict[key]["bottom_twent"]["all"])
        mini = met_dict[key]["bottom_twent"]["min"]
        met_dict[key]["bottom_twent"]["max"] = max(met_dict[key]["bottom_twent"]["all"])
        maxi = met_dict[key]["bottom_twent"]["max"]
        ave = mean(met_dict[key]["bottom_twent"]["all"])
        print "Bottom 20th Percentile:"
        print "          {} to {}. Mean: {}".format(mini, maxi, ave)

        met_dict[key]["low_twent"] = {}
        met_dict[key]["low_twent"]["all"] = met_dict[key]["all"][2081:4162]
        met_dict[key]["low_twent"]["min"] = min(met_dict[key]["low_twent"]["all"])
        mini = met_dict[key]["low_twent"]["min"]
        met_dict[key]["low_twent"]["max"] = max(met_dict[key]["low_twent"]["all"])
        maxi = met_dict[key]["low_twent"]["max"]
        ave = mean(met_dict[key]["low_twent"]["all"])
        print "Low Twentieth Percentile:"
        print "          {} to {}. Mean: {}".format(mini, maxi, ave)

        met_dict[key]["mid_twent"] = {}
        met_dict[key]["mid_twent"]["all"] = met_dict[key]["all"][4162:6243]
        met_dict[key]["mid_twent"]["min"] = min(met_dict[key]["mid_twent"]["all"])
        mini = met_dict[key]["mid_twent"]["min"]
        met_dict[key]["mid_twent"]["max"] = max(met_dict[key]["mid_twent"]["all"])
        maxi = met_dict[key]["mid_twent"]["max"]
        ave = mean(met_dict[key]["mid_twent"]["all"])
        print "Mid Twentieth Percentile:"
        print "          {} to {}. Mean: {}".format(mini, maxi, ave)

        met_dict[key]["high_twent"] = {}
        met_dict[key]["high_twent"]["all"] = met_dict[key]["all"][6243:8324]
        met_dict[key]["high_twent"]["min"] = min(met_dict[key]["high_twent"]["all"])
        mini = met_dict[key]["high_twent"]["min"]
        met_dict[key]["high_twent"]["max"] = max(met_dict[key]["high_twent"]["all"])
        maxi = met_dict[key]["high_twent"]["max"]
        ave = mean(met_dict[key]["high_twent"]["all"])
        print "High Twentieth Percentile:"
        print "          {} to {}. Mean: {}".format(mini, maxi, ave)

        met_dict[key]["top_twent"] = {}
        met_dict[key]["top_twent"]["all"] = met_dict[key]["all"][8324:]
        met_dict[key]["top_twent"]["min"] = min(met_dict[key]["top_twent"]["all"])
        mini = met_dict[key]["top_twent"]["min"]
        met_dict[key]["top_twent"]["max"] = max(met_dict[key]["top_twent"]["all"])
        maxi = met_dict[key]["top_twent"]["max"]
        ave = mean(met_dict[key]["top_twent"]["all"])
        print "Top Twentieth Percentile:"
        print "          {} to {}. Mean: {}".format(mini, maxi, ave)

        met_dict[key]["top_ten"] = {}
        met_dict[key]["top_ten"]["all"] = met_dict[key]["all"][9365:]
        met_dict[key]["top_ten"]["min"] = min(met_dict[key]["top_ten"]["all"])
        mini = met_dict[key]["top_ten"]["min"]
        met_dict[key]["top_ten"]["max"] = max(met_dict[key]["top_ten"]["all"])
        maxi = met_dict[key]["top_ten"]["max"]
        ave = mean(met_dict[key]["top_ten"]["all"])
        print "Top Tenth Percentile:"
        print "          {} to {}. Mean: {}".format(mini, maxi, ave)


# END_REPEAT:
# Standard Deviation: 0.0987644888348
# Bottom 10th Percentile:
#           0.117647058824 to 0.821951219512. Mean: 0.701745524487
# Bottom 20th Percentile:
#           0.117647058824 to 0.885714285714. Mean: 0.779620893416
# Low Twentieth Percentile:
#           0.885964912281 to 0.942857142857. Mean: 0.918395941376
# Mid Twentieth Percentile:
#           0.942857142857 to 1.0. Mean: 0.965574412318
# High Twentieth Percentile:
#           1.0 to 1.0. Mean: 1.0
# Top Twentieth Percentile:
#           1.0 to 1.0. Mean: 1.0
# Top Tenth Percentile:
#           1.0 to 1.0. Mean: 1.0

# ACTIVE_PERCENT:
# Standard Deviation: 0.0269684563303
# Bottom 10th Percentile:
#           0.0 to 0.0366972477064. Mean: 0.0253931924471
# Bottom 20th Percentile:
#           0.0 to 0.046875. Mean: 0.0337332901763
# Low Twentieth Percentile:
#           0.046875 to 0.0594900849858. Mean: 0.0534713293778
# Mid Twentieth Percentile:
#           0.0594965675057 to 0.0708955223881. Mean: 0.0652113044239
# High Twentieth Percentile:
#           0.0709010339734 to 0.0867052023121. Mean: 0.0779868531001
# Top Twentieth Percentile:
#           0.0867052023121 to 0.393939393939. Mean: 0.106834070547
# Top Tenth Percentile:
#           0.10067114094 to 0.393939393939. Mean: 0.120662809039

# LL_MEDIAN:
# Standard Deviation: 394.561662788
# Bottom 10th Percentile:
#           4.0 to 22.5. Mean: 17.7997118156
# Bottom 20th Percentile:
#           4.0 to 27.0. Mean: 21.4341662662
# Low Twentieth Percentile:
#           27.0 to 33.5. Mean: 30.4238346949
# Mid Twentieth Percentile:
#           33.5 to 40.0. Mean: 36.4493032196
# High Twentieth Percentile:
#           40.0 to 44.0. Mean: 41.8570398847
# Top Twentieth Percentile:
#           44.0 to 15958.0. Mean: 249.78880346
# Top Tenth Percentile:
#           50.0 to 15958.0. Mean: 453.444711538

# RHYME:
# Standard Deviation: 0.899185045666
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.153846153846. Mean: 0.0507554302876
# Low Twentieth Percentile:
#           0.153846153846 to 0.375. Mean: 0.263817473386
# Mid Twentieth Percentile:
#           0.375 to 0.666666666667. Mean: 0.514978542895
# High Twentieth Percentile:
#           0.666666666667 to 1.09375. Mean: 0.864025878779
# Top Twentieth Percentile:
#           1.09375 to 16.4474522293. Mean: 1.96270477627
# Top Tenth Percentile:
#           1.57142857143 to 16.4474522293. Mean: 2.62768401356

# MALE_PERCENT:
# Standard Deviation: 0.0200289903426
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0016694490818. Mean: 3.77131202055e-05
# Mid Twentieth Percentile:
#           0.00167224080268 to 0.00956937799043. Mean: 0.00582174149919
# High Twentieth Percentile:
#           0.00956937799043 to 0.0235294117647. Mean: 0.0155605902144
# Top Twentieth Percentile:
#           0.0235294117647 to 0.181818181818. Mean: 0.0464290084347
# Top Tenth Percentile:
#           0.04 to 0.181818181818. Mean: 0.0620103850526

# A_FREQ:
# Standard Deviation: 0.0196237246468
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.00892857142857. Mean: 0.00265934694315
# Low Twentieth Percentile:
#           0.00892857142857 to 0.0173913043478. Mean: 0.0132617680668
# Mid Twentieth Percentile:
#           0.0173913043478 to 0.025641025641. Mean: 0.0214851003315
# High Twentieth Percentile:
#           0.025641025641 to 0.037037037037. Mean: 0.030738306091
# Top Twentieth Percentile:
#           0.037037037037 to 0.272727272727. Mean: 0.0537009231142
# Top Tenth Percentile:
#           0.047619047619 to 0.272727272727. Mean: 0.0655574949211

# NEGATIVE:
# Standard Deviation: 0.0221423291689
# Bottom 10th Percentile:
#           0.0 to 0.0161290322581. Mean: 0.00812777960127
# Bottom 20th Percentile:
#           0.0 to 0.0235294117647. Mean: 0.014113057439
# Low Twentieth Percentile:
#           0.0235294117647 to 0.0333333333333. Mean: 0.0285688825762
# Mid Twentieth Percentile:
#           0.0333333333333 to 0.0427553444181. Mean: 0.0379612046296
# High Twentieth Percentile:
#           0.0427631578947 to 0.0560747663551. Mean: 0.0487106514418
# Top Twentieth Percentile:
#           0.0560747663551 to 0.393939393939. Mean: 0.0733319569079
# Top Tenth Percentile:
#           0.0681818181818 to 0.393939393939. Mean: 0.0853830461547

# LL_MODE:
# Standard Deviation: 417.117510935
# Bottom 10th Percentile:
#           1.0 to 22.0. Mean: 14.8924111431
# Bottom 20th Percentile:
#           1.0 to 28.0. Mean: 19.8121095627
# Low Twentieth Percentile:
#           28.0 to 35.0. Mean: 31.4680442095
# Mid Twentieth Percentile:
#           35.0 to 41.0. Mean: 38.345987506
# High Twentieth Percentile:
#           41.0 to 47.0. Mean: 43.9855838539
# Top Twentieth Percentile:
#           47.0 to 15958.0. Mean: 272.520422874
# Top Tenth Percentile:
#           55.0 to 15958.0. Mean: 495.085576923

# SL_MEDIAN:
# Standard Deviation: 38.7135956302
# Bottom 10th Percentile:
#           0.0 to 1.0. Mean: 0.932756964457
# Bottom 20th Percentile:
#           0.0 to 1.0. Mean: 0.966362325805
# Low Twentieth Percentile:
#           1.0 to 3.0. Mean: 2.21672272946
# Mid Twentieth Percentile:
#           3.0 to 6.0. Mean: 4.35896203748
# High Twentieth Percentile:
#           6.0 to 13.0. Mean: 8.37337818357
# Top Twentieth Percentile:
#           13.0 to 3182.0. Mean: 29.4863046612
# Top Tenth Percentile:
#           20.0 to 3182.0. Mean: 43.5884615385

# PL_CHAR:
# Standard Deviation: 3293.41346789
# Bottom 10th Percentile:
#           16.0 to 352.0. Mean: 231.126801153
# Bottom 20th Percentile:
#           16.0 to 505.0. Mean: 331.729456992
# Low Twentieth Percentile:
#           505.0 to 696.0. Mean: 598.999519462
# Mid Twentieth Percentile:
#           696.0 to 1047.0. Mean: 861.21912542
# High Twentieth Percentile:
#           1048.0 to 1785.0. Mean: 1352.36328688
# Top Twentieth Percentile:
#           1786.0 to 126897.0. Mean: 4571.29841422
# Top Tenth Percentile:
#           2814.0 to 126897.0. Mean: 6942.71730769

# POEM_PERCENT:
# Standard Deviation: 0.0837572190393
# Bottom 10th Percentile:
#           0.0 to 0.277419354839. Mean: 0.233442470757
# Bottom 20th Percentile:
#           0.0 to 0.311111111111. Mean: 0.26446644886
# Low Twentieth Percentile:
#           0.311203319502 to 0.354166666667. Mean: 0.333881407721
# Mid Twentieth Percentile:
#           0.354166666667 to 0.39156626506. Mean: 0.372505174662
# High Twentieth Percentile:
#           0.39156626506 to 0.440217391304. Mean: 0.414286623937
# Top Twentieth Percentile:
#           0.440233236152 to 0.866582512016. Mean: 0.49437601853
# Top Tenth Percentile:
#           0.479452054795 to 0.866582512016. Mean: 0.531168487083

# FEMALE_PERCENT:
# Standard Deviation: 0.0176589307293
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0. Mean: 0.0
# Mid Twentieth Percentile:
#           0.0 to 0.00409836065574. Mean: 0.00102295089553
# High Twentieth Percentile:
#           0.00409836065574 to 0.0144032921811. Mean: 0.00824936931982
# Top Twentieth Percentile:
#           0.014409221902 to 0.169811320755. Mean: 0.0370256649898
# Top Tenth Percentile:
#           0.0294117647059 to 0.169811320755. Mean: 0.053427401626

# IS_FREQ:
# Standard Deviation: 0.0126854921505
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.00294985250737. Mean: 0.000337715951233
# Mid Twentieth Percentile:
#           0.00294985250737 to 0.00882352941176. Mean: 0.00607546889226
# High Twentieth Percentile:
#           0.00884303610906 to 0.0164533820841. Mean: 0.0120939816765
# Top Twentieth Percentile:
#           0.016458569807 to 0.25. Mean: 0.0287161803562
# Top Tenth Percentile:
#           0.0243902439024 to 0.25. Mean: 0.0377454416947

# LL_MEAN:
# Standard Deviation: 396.396687051
# Bottom 10th Percentile:
#           4.27272727273 to 23.0. Mean: 18.3196430913
# Bottom 20th Percentile:
#           4.27272727273 to 27.4756097561. Mean: 21.8836467704
# Low Twentieth Percentile:
#           27.4761904762 to 33.3125. Mean: 30.4719062517
# Mid Twentieth Percentile:
#           33.3125 to 39.25. Mean: 36.1455528863
# High Twentieth Percentile:
#           39.2631578947 to 43.8344370861. Mean: 41.5966493966
# Top Twentieth Percentile:
#           43.84 to 15958.0. Mean: 253.515964882
# Top Tenth Percentile:
#           49.7586206897 to 15958.0. Mean: 461.153846596

# ABS_PERCENT:
# Standard Deviation: 0.0154456638056
# Bottom 10th Percentile:
#           0.0 to 0.00452488687783. Mean: 0.000384613327371
# Bottom 20th Percentile:
#           0.0 to 0.00949367088608. Mean: 0.00389857540826
# Low Twentieth Percentile:
#           0.00952380952381 to 0.0161943319838. Mean: 0.0130440536831
# Mid Twentieth Percentile:
#           0.0161943319838 to 0.0224719101124. Mean: 0.0192726246972
# High Twentieth Percentile:
#           0.0224719101124 to 0.0311942959002. Mean: 0.0263313982783
# Top Twentieth Percentile:
#           0.0312109862672 to 0.25. Mean: 0.0442061443068
# Top Tenth Percentile:
#           0.0396825396825 to 0.25. Mean: 0.0534565073416

# PL_LINES:
# Standard Deviation: 81.6423764634
# Bottom 10th Percentile:
#           1.0 to 10.0. Mean: 5.82228626321
# Bottom 20th Percentile:
#           1.0 to 14.0. Mean: 9.29072561269
# Low Twentieth Percentile:
#           14.0 to 20.0. Mean: 16.4555502162
# Mid Twentieth Percentile:
#           20.0 to 29.0. Mean: 23.9082172033
# High Twentieth Percentile:
#           29.0 to 48.0. Mean: 36.7280153772
# Top Twentieth Percentile:
#           48.0 to 3182.0. Mean: 117.869774147
# Top Tenth Percentile:
#           75.0 to 3182.0. Mean: 176.640384615

# WL_MODE:
# Standard Deviation: 1.26819725069
# Bottom 10th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Low Twentieth Percentile:
#           1.0 to 3.0. Mean: 2.48534358481
# Mid Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# High Twentieth Percentile:
#           3.0 to 4.0. Mean: 3.48534358481
# Top Twentieth Percentile:
#           4.0 to 55.0. Mean: 4.20326765978
# Top Tenth Percentile:
#           4.0 to 55.0. Mean: 4.40673076923

# WL_RANGE:
# Standard Deviation: 2.33984467016
# Bottom 10th Percentile:
#           3.0 to 8.0. Mean: 7.30451488953
# Bottom 20th Percentile:
#           3.0 to 9.0. Mean: 7.90485343585
# Low Twentieth Percentile:
#           9.0 to 10.0. Mean: 9.2931283037
# Mid Twentieth Percentile:
#           10.0 to 11.0. Mean: 10.234502643
# High Twentieth Percentile:
#           11.0 to 12.0. Mean: 11.2801537722
# Top Twentieth Percentile:
#           12.0 to 126.0. Mean: 13.2143200384
# Top Tenth Percentile:
#           13.0 to 126.0. Mean: 14.2557692308

# WL_MEDIAN:
# Standard Deviation: 0.525455662853
# Bottom 10th Percentile:
#           1.0 to 3.0. Mean: 2.96061479347
# Bottom 20th Percentile:
#           1.0 to 3.0. Mean: 2.98029793369
# Low Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# Mid Twentieth Percentile:
#           3.0 to 4.0. Mean: 3.85535800096
# High Twentieth Percentile:
#           4.0 to 4.0. Mean: 4.0
# Top Twentieth Percentile:
#           4.0 to 7.0. Mean: 4.0523786641
# Top Tenth Percentile:
#           4.0 to 7.0. Mean: 4.10480769231

# POSITIVE:
# Standard Deviation: 0.0246851697491
# Bottom 10th Percentile:
#           0.0 to 0.0190476190476. Mean: 0.0107892657574
# Bottom 20th Percentile:
#           0.0 to 0.0264317180617. Mean: 0.016973437739
# Low Twentieth Percentile:
#           0.026455026455 to 0.0373563218391. Mean: 0.0321716308252
# Mid Twentieth Percentile:
#           0.0373626373626 to 0.047619047619. Mean: 0.0424455824094
# High Twentieth Percentile:
#           0.047619047619 to 0.0623306233062. Mean: 0.0544117102632
# Top Twentieth Percentile:
#           0.0623591284748 to 0.262247838617. Mean: 0.0830075244313
# Top Tenth Percentile:
#           0.0763358778626 to 0.262247838617. Mean: 0.0976102082378

# PL_WORDS:
# Standard Deviation: 696.87057056
# Bottom 10th Percentile:
#           4.0 to 78.0. Mean: 51.6330451489
# Bottom 20th Percentile:
#           4.0 to 110.0. Mean: 73.1883709755
# Low Twentieth Percentile:
#           110.0 to 152.0. Mean: 130.554541086
# Mid Twentieth Percentile:
#           152.0 to 227.0. Mean: 186.615569438
# High Twentieth Percentile:
#           227.0 to 383.0. Mean: 292.538683325
# Top Twentieth Percentile:
#           383.0 to 27925.0. Mean: 979.815953868
# Top Tenth Percentile:
#           603.0 to 27925.0. Mean: 1485.7375

# OBJECT_PERCENT:
# Standard Deviation: 0.019149065265
# Bottom 10th Percentile:
#           0.0 to 0.0106382978723. Mean: 0.00448356814102
# Bottom 20th Percentile:
#           0.0 to 0.0167464114833. Mean: 0.00926974313618
# Low Twentieth Percentile:
#           0.0167597765363 to 0.0252525252525. Mean: 0.0212489302532
# Mid Twentieth Percentile:
#           0.0252525252525 to 0.0331491712707. Mean: 0.0291443987957
# High Twentieth Percentile:
#           0.0331491712707 to 0.0446428571429. Mean: 0.0383744043017
# Top Twentieth Percentile:
#           0.0446428571429 to 0.272727272727. Mean: 0.0605083465188
# Top Tenth Percentile:
#           0.0552995391705 to 0.272727272727. Mean: 0.0714272920909

# YOU_FREQ:
# Standard Deviation: 0.0157153088779
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0. Mean: 0.0
# Mid Twentieth Percentile:
#           0.0 to 0.00254777070064. Mean: 0.000199181351961
# High Twentieth Percentile:
#           0.00254885301614 to 0.0138888888889. Mean: 0.00759534282952
# Top Twentieth Percentile:
#           0.0138888888889 to 0.238095238095. Mean: 0.0332574345461
# Top Tenth Percentile:
#           0.027397260274 to 0.238095238095. Mean: 0.0469398646216

# WL_MEAN:
# Standard Deviation: 0.496671349737
# Bottom 10th Percentile:
#           2.0 to 3.0. Mean: 2.96541786744
# Bottom 20th Percentile:
#           2.0 to 3.0. Mean: 2.9827006247
# Low Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# Mid Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# High Twentieth Percentile:
#           3.0 to 4.0. Mean: 3.57616530514
# Top Twentieth Percentile:
#           4.0 to 15.0. Mean: 4.02835175396
# Top Tenth Percentile:
#           4.0 to 15.0. Mean: 4.05673076923

# PASSIVE_PERCENT:
# Standard Deviation: 0.023384565277
# Bottom 10th Percentile:
#           0.0 to 0.0230547550432. Mean: 0.0135876654901
# Bottom 20th Percentile:
#           0.0 to 0.0309278350515. Mean: 0.0204287447008
# Low Twentieth Percentile:
#           0.0309278350515 to 0.0414364640884. Mean: 0.0364387666556
# Mid Twentieth Percentile:
#           0.0414364640884 to 0.0512820512821. Mean: 0.0462590344029
# High Twentieth Percentile:
#           0.0512820512821 to 0.0651340996169. Mean: 0.0573798738135
# Top Twentieth Percentile:
#           0.0651685393258 to 0.393939393939. Mean: 0.0834339378413
# Top Tenth Percentile:
#           0.0777777777778 to 0.393939393939. Mean: 0.0962013915843

# STANZAS:
# Standard Deviation: 36.141883826
# Bottom 10th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Low Twentieth Percentile:
#           1.0 to 4.0. Mean: 2.51225372417
# Mid Twentieth Percentile:
#           4.0 to 7.0. Mean: 5.30225852955
# High Twentieth Percentile:
#           7.0 to 17.0. Mean: 11.1931763575
# Top Twentieth Percentile:
#           17.0 to 1049.0. Mean: 52.350792888
# Top Tenth Percentile:
#           33.0 to 1049.0. Mean: 81.3490384615

# SL_MODE:
# Standard Deviation: 42.0724635356
# Bottom 10th Percentile:
#           0.0 to 1.0. Mean: 0.85590778098
# Bottom 20th Percentile:
#           0.0 to 1.0. Mean: 0.927919269582
# Low Twentieth Percentile:
#           1.0 to 4.0. Mean: 2.13935607881
# Mid Twentieth Percentile:
#           4.0 to 6.0. Mean: 4.50120134551
# High Twentieth Percentile:
#           6.0 to 14.0. Mean: 9.63671311869
# Top Twentieth Percentile:
#           14.0 to 3182.0. Mean: 33.3786641038
# Top Tenth Percentile:
#           23.0 to 3182.0. Mean: 49.3692307692

# LEX_DIV:
# Standard Deviation: 0.113531517535
# Bottom 10th Percentile:
#           0.1 to 0.457760314342. Mean: 0.393504856849
# Bottom 20th Percentile:
#           0.1 to 0.511461318052. Mean: 0.440931284253
# Low Twentieth Percentile:
#           0.511482254697 to 0.578723404255. Mean: 0.546965650083
# Mid Twentieth Percentile:
#           0.578754578755 to 0.63184079602. Mean: 0.605552573738
# High Twentieth Percentile:
#           0.631868131868 to 0.690217391304. Mean: 0.659312642018
# Top Twentieth Percentile:
#           0.690217391304 to 1.0. Mean: 0.754786580787
# Top Tenth Percentile:
#           0.734375 to 1.0. Mean: 0.799823442896

# I_FREQ:
# Standard Deviation: 0.0207427169688
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.00395256916996. Mean: 0.000446137935532
# Mid Twentieth Percentile:
#           0.00396825396825 to 0.0149253731343. Mean: 0.00933298611317
# High Twentieth Percentile:
#           0.0149253731343 to 0.030303030303. Mean: 0.021886496902
# Top Twentieth Percentile:
#           0.030303030303 to 0.260869565217. Mean: 0.0496945344174
# Top Tenth Percentile:
#           0.0442477876106 to 0.260869565217. Mean: 0.0629703600074

# ALLITERATION:
# Standard Deviation: 0.14713015662
# Bottom 10th Percentile:
#           0.0 to 0.15873015873. Mean: 0.105614230318
# Bottom 20th Percentile:
#           0.0 to 0.200617283951. Mean: 0.143512181091
# Low Twentieth Percentile:
#           0.200716845878 to 0.257042253521. Mean: 0.230654056385
# Mid Twentieth Percentile:
#           0.257042253521 to 0.304597701149. Mean: 0.280700377684
# High Twentieth Percentile:
#           0.304597701149 to 0.363636363636. Mean: 0.331993660454
# Top Twentieth Percentile:
#           0.363834422658 to 1.0. Mean: 0.498406569265
# Top Tenth Percentile:
#           0.421568627451 to 1.0. Mean: 0.608030952433

# SL_RANGE:
# Standard Deviation: 16.9337628777
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0. Mean: 0.0
# Mid Twentieth Percentile:
#           0.0 to 1.0. Mean: 0.659298414224
# High Twentieth Percentile:
#           1.0 to 5.0. Mean: 2.72513214801
# Top Twentieth Percentile:
#           5.0 to 1170.0. Mean: 19.0168188371
# Top Tenth Percentile:
#           12.0 to 1170.0. Mean: 29.9682692308

# SL_MEAN:
# Standard Deviation: 38.7393859809
# Bottom 10th Percentile:
#           0.203883495146 to 0.914285714286. Mean: 0.804204232859
# Bottom 20th Percentile:
#           0.203883495146 to 1.0. Mean: 0.893316699568
# Low Twentieth Percentile:
#           1.0 to 3.78571428571. Mean: 2.56345827548
# Mid Twentieth Percentile:
#           3.78571428571 to 6.0. Mean: 4.54928842371
# High Twentieth Percentile:
#           6.0 to 13.0. Mean: 8.67124432222
# Top Twentieth Percentile:
#           13.0 to 3182.0. Mean: 29.8500892092
# Top Tenth Percentile:
#           21.0 to 3182.0. Mean: 44.0174163427

# THE_FREQ:
# Standard Deviation: 0.0334260492709
# Bottom 10th Percentile:
#           0.0 to 0.0243902439024. Mean: 0.0120373069766
# Bottom 20th Percentile:
#           0.0 to 0.0374331550802. Mean: 0.0217510647761
# Low Twentieth Percentile:
#           0.0374331550802 to 0.0550458715596. Mean: 0.0466983011069
# Mid Twentieth Percentile:
#           0.0550458715596 to 0.07. Mean: 0.0623347666284
# High Twentieth Percentile:
#           0.07 to 0.0899470899471. Mean: 0.0792944626779
# Top Twentieth Percentile:
#           0.0899653979239 to 0.5. Mean: 0.113468257561
# Top Tenth Percentile:
#           0.106422018349 to 0.5. Mean: 0.129508316709

# LL_RANGE:
# Standard Deviation: 183.507907773
# Bottom 10th Percentile:
#           0.0 to 12.0. Mean: 7.38520653218
# Bottom 20th Percentile:
#           0.0 to 15.0. Mean: 10.5728015377
# Low Twentieth Percentile:
#           15.0 to 22.0. Mean: 18.5415665545
# Mid Twentieth Percentile:
#           22.0 to 31.0. Mean: 26.5290725613
# High Twentieth Percentile:
#           31.0 to 45.0. Mean: 37.5358000961
# Top Twentieth Percentile:
#           45.0 to 8979.0. Mean: 123.942335416
# Top Tenth Percentile:
#           58.0 to 8979.0. Mean: 197.347115385

# COMMON_PERCENT:
# Standard Deviation: 0.0761767095041
# Bottom 10th Percentile:
#           0.140221402214 to 0.359355638166. Mean: 0.318082840078
# Bottom 20th Percentile:
#           0.140221402214 to 0.388692579505. Mean: 0.346832322679
# Low Twentieth Percentile:
#           0.388704318937 to 0.428571428571. Mean: 0.409427423269
# Mid Twentieth Percentile:
#           0.428571428571 to 0.463157894737. Mean: 0.445343685687
# High Twentieth Percentile:
#           0.463235294118 to 0.504918032787. Mean: 0.482494046905
# Top Twentieth Percentile:
#           0.50495049505 to 0.90848181774. Mean: 0.554820987389
# Top Tenth Percentile:
#           0.539215686275 to 0.90848181774. Mean: 0.589092607648


if __name__ == "__main__" or __name__ == "__console__":

    connect_to_db(app)
    print "Connected to DB."
