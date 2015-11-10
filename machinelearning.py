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
# Standard Deviation: 0.0979925904811
# Bottom 10th Percentile:
#           0.117647058824 to 0.825. Mean: 0.705225473892
# Bottom 20th Percentile:
#           0.117647058824 to 0.887096774194. Mean: 0.78205498557
# Low Twentieth Percentile:
#           0.887096774194 to 0.944444444444. Mean: 0.919022199998
# Mid Twentieth Percentile:
#           0.944444444444 to 1.0. Mean: 0.966202037788
# High Twentieth Percentile:
#           1.0 to 1.0. Mean: 1.0
# Top Twentieth Percentile:
#           1.0 to 1.0. Mean: 1.0
# Top Tenth Percentile:
#           1.0 to 1.0. Mean: 1.0

# ACTIVE_PERCENT:
# Standard Deviation: 0.0269906086091
# Bottom 10th Percentile:
#           0.0 to 0.0366972477064. Mean: 0.0254223813509
# Bottom 20th Percentile:
#           0.0 to 0.046875. Mean: 0.0337527824403
# Low Twentieth Percentile:
#           0.046875 to 0.0595238095238. Mean: 0.0534799106274
# Mid Twentieth Percentile:
#           0.0595238095238 to 0.0710059171598. Mean: 0.0652843461424
# High Twentieth Percentile:
#           0.0710059171598 to 0.0869565217391. Mean: 0.0781610823219
# Top Twentieth Percentile:
#           0.0869565217391 to 0.393939393939. Mean: 0.107056887689
# Top Tenth Percentile:
#           0.10101010101 to 0.393939393939. Mean: 0.121111510052

# LL_MEDIAN:
# Standard Deviation: 394.995121143
# Bottom 10th Percentile:
#           4.0 to 22.5. Mean: 17.7997118156
# Bottom 20th Percentile:
#           4.0 to 27.0. Mean: 21.4341662662
# Low Twentieth Percentile:
#           27.0 to 33.5. Mean: 30.4245555022
# Mid Twentieth Percentile:
#           33.5 to 40.0. Mean: 36.4557904853
# High Twentieth Percentile:
#           40.0 to 44.0. Mean: 41.8844305622
# Top Twentieth Percentile:
#           44.0 to 15958.0. Mean: 252.08090379
# Top Tenth Percentile:
#           50.0 to 15958.0. Mean: 462.55899705

# RHYME:
# Standard Deviation: 0.85941680649
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.153846153846. Mean: 0.0507905477025
# Low Twentieth Percentile:
#           0.153846153846 to 0.375. Mean: 0.263923746258
# Mid Twentieth Percentile:
#           0.375 to 0.666666666667. Mean: 0.515118699871
# High Twentieth Percentile:
#           0.666666666667 to 1.09375. Mean: 0.864231108637
# Top Twentieth Percentile:
#           1.09375 to 16.1904761905. Mean: 1.93202589352
# Top Tenth Percentile:
#           1.57142857143 to 16.1904761905. Mean: 2.58017143068

# MALE_PERCENT:
# Standard Deviation: 0.0200324168659
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0016694490818. Mean: 3.77131202055e-05
# Mid Twentieth Percentile:
#           0.00167224080268 to 0.00956937799043. Mean: 0.00582174149919
# High Twentieth Percentile:
#           0.00956937799043 to 0.023598820059. Mean: 0.015582125828
# Top Twentieth Percentile:
#           0.023598820059 to 0.181818181818. Mean: 0.0466029462119
# Top Tenth Percentile:
#           0.0405405405405 to 0.181818181818. Mean: 0.0624860409863

# A_FREQ:
# Standard Deviation: 0.0196315788557
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0089485458613. Mean: 0.00267703950237
# Low Twentieth Percentile:
#           0.00896860986547 to 0.0174418604651. Mean: 0.0133347896458
# Mid Twentieth Percentile:
#           0.0174672489083 to 0.025826446281. Mean: 0.0215697175503
# High Twentieth Percentile:
#           0.025855513308 to 0.0372670807453. Mean: 0.0308619564197
# Top Twentieth Percentile:
#           0.0373134328358 to 0.272727272727. Mean: 0.0538863300151
# Top Tenth Percentile:
#           0.0480225988701 to 0.272727272727. Mean: 0.0659606356134

# NEGATIVE:
# Standard Deviation: 0.0221575735251
# Bottom 10th Percentile:
#           0.0 to 0.0161290322581. Mean: 0.00813804986751
# Bottom 20th Percentile:
#           0.0 to 0.0235294117647. Mean: 0.0141217512048
# Low Twentieth Percentile:
#           0.0235294117647 to 0.0333333333333. Mean: 0.0285815711402
# Mid Twentieth Percentile:
#           0.0333333333333 to 0.0428540818513. Mean: 0.0380000544679
# High Twentieth Percentile:
#           0.0428571428571 to 0.05625. Mean: 0.0488185473603
# Top Twentieth Percentile:
#           0.05625 to 0.393939393939. Mean: 0.0735128207265
# Top Tenth Percentile:
#           0.0683760683761 to 0.393939393939. Mean: 0.0857657193578

# LL_MODE:
# Standard Deviation: 417.574509705
# Bottom 10th Percentile:
#           1.0 to 22.0. Mean: 14.911623439
# Bottom 20th Percentile:
#           1.0 to 28.0. Mean: 19.824603556
# Low Twentieth Percentile:
#           28.0 to 35.0. Mean: 31.4733301297
# Mid Twentieth Percentile:
#           35.0 to 41.0. Mean: 38.3565593465
# High Twentieth Percentile:
#           41.0 to 47.0. Mean: 44.040365209
# Top Twentieth Percentile:
#           47.0 to 15958.0. Mean: 275.040816327
# Top Tenth Percentile:
#           55.0 to 15958.0. Mean: 505.038348083

# SL_MEDIAN:
# Standard Deviation: 13.7374715734
# Bottom 10th Percentile:
#           0.0 to 1.0. Mean: 0.932756964457
# Bottom 20th Percentile:
#           0.0 to 1.0. Mean: 0.966362325805
# Low Twentieth Percentile:
#           1.0 to 3.0. Mean: 2.21864488227
# Mid Twentieth Percentile:
#           3.0 to 6.0. Mean: 4.36520903412
# High Twentieth Percentile:
#           6.0 to 13.0. Mean: 8.39019702066
# Top Twentieth Percentile:
#           13.0 to 383.0. Mean: 26.3168124393
# Top Tenth Percentile:
#           20.0 to 383.0. Mean: 37.4444444444

# PL_CHAR:
# Standard Deviation: 2235.90563102
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
#           1786.0 to 45726.0. Mean: 4117.42954325
# Top Tenth Percentile:
#           2814.0 to 45726.0. Mean: 6077.89970501

# POEM_PERCENT:
# Standard Deviation: 0.0836857664727
# Bottom 10th Percentile:
#           0.0 to 0.277419354839. Mean: 0.233442470757
# Bottom 20th Percentile:
#           0.0 to 0.311111111111. Mean: 0.26446644886
# Low Twentieth Percentile:
#           0.311203319502 to 0.354166666667. Mean: 0.333889670801
# Mid Twentieth Percentile:
#           0.354166666667 to 0.391608391608. Mean: 0.372537469989
# High Twentieth Percentile:
#           0.391666666667 to 0.440633245383. Mean: 0.414532784517
# Top Twentieth Percentile:
#           0.440677966102 to 0.851851851852. Mean: 0.494764675777
# Top Tenth Percentile:
#           0.480769230769 to 0.851851851852. Mean: 0.531941639646

# FEMALE_PERCENT:
# Standard Deviation: 0.0176758613144
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0. Mean: 0.0
# Mid Twentieth Percentile:
#           0.0 to 0.00412912912913. Mean: 0.00103224878297
# High Twentieth Percentile:
#           0.00413223140496 to 0.0145695364238. Mean: 0.00833965411112
# Top Twentieth Percentile:
#           0.014598540146 to 0.169811320755. Mean: 0.0372714782134
# Top Tenth Percentile:
#           0.0298507462687 to 0.169811320755. Mean: 0.0539656792494

# IS_FREQ:
# Standard Deviation: 0.0126965760437
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.00304414003044. Mean: 0.000340675431445
# Mid Twentieth Percentile:
#           0.0030487804878 to 0.00884955752212. Mean: 0.00612340718674
# High Twentieth Percentile:
#           0.00885826771654 to 0.0165745856354. Mean: 0.0121732872782
# Top Twentieth Percentile:
#           0.0165745856354 to 0.25. Mean: 0.0288525358342
# Top Tenth Percentile:
#           0.0245901639344 to 0.25. Mean: 0.0380460129288

# LL_MEAN:
# Standard Deviation: 396.832045433
# Bottom 10th Percentile:
#           4.27272727273 to 23.0. Mean: 18.3196430913
# Bottom 20th Percentile:
#           4.27272727273 to 27.4756097561. Mean: 21.8836467704
# Low Twentieth Percentile:
#           27.4761904762 to 33.3125. Mean: 30.4727562006
# Mid Twentieth Percentile:
#           33.3125 to 39.2666666667. Mean: 36.1512377915
# High Twentieth Percentile:
#           39.2666666667 to 43.8888888889. Mean: 41.623586093
# Top Twentieth Percentile:
#           43.8918918919 to 15958.0. Mean: 255.850913259
# Top Tenth Percentile:
#           50.027027027 to 15958.0. Mean: 470.444855471

# ABS_PERCENT:
# Standard Deviation: 0.0154605217225
# Bottom 10th Percentile:
#           0.0 to 0.00452488687783. Mean: 0.000388773446333
# Bottom 20th Percentile:
#           0.0 to 0.00952380952381. Mean: 0.00390305864059
# Low Twentieth Percentile:
#           0.00952380952381 to 0.0161943319838. Mean: 0.0130496753455
# Mid Twentieth Percentile:
#           0.0162119414788 to 0.0225. Mean: 0.0193042735842
# High Twentieth Percentile:
#           0.0225225225225 to 0.03125. Mean: 0.0264237471785
# Top Twentieth Percentile:
#           0.03125 to 0.25. Mean: 0.0443509598232
# Top Tenth Percentile:
#           0.04 to 0.25. Mean: 0.0537644973705

# PL_LINES:
# Standard Deviation: 55.1454028022
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
#           48.0 to 893.0. Mean: 106.856656948
# Top Tenth Percentile:
#           75.0 to 893.0. Mean: 155.683382498

# WL_MODE:
# Standard Deviation: 1.26897057158
# Bottom 10th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Low Twentieth Percentile:
#           1.0 to 3.0. Mean: 2.48726573763
# Mid Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# High Twentieth Percentile:
#           3.0 to 4.0. Mean: 3.49303219606
# Top Twentieth Percentile:
#           4.0 to 55.0. Mean: 4.2055393586
# Top Tenth Percentile:
#           4.0 to 55.0. Mean: 4.41592920354

# WL_RANGE:
# Standard Deviation: 2.33532210916
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
#           12.0 to 126.0. Mean: 13.20505345
# Top Tenth Percentile:
#           13.0 to 126.0. Mean: 14.2586037365

# WL_MEDIAN:
# Standard Deviation: 0.52544930663
# Bottom 10th Percentile:
#           1.0 to 3.0. Mean: 2.96061479347
# Bottom 20th Percentile:
#           1.0 to 3.0. Mean: 2.98029793369
# Low Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# Mid Twentieth Percentile:
#           3.0 to 4.0. Mean: 3.85679961557
# High Twentieth Percentile:
#           4.0 to 4.0. Mean: 4.0
# Top Twentieth Percentile:
#           4.0 to 7.0. Mean: 4.05247813411
# Top Tenth Percentile:
#           4.0 to 7.0. Mean: 4.10619469027

# POSITIVE:
# Standard Deviation: 0.0247032407919
# Bottom 10th Percentile:
#           0.0 to 0.0190839694656. Mean: 0.0108047531475
# Bottom 20th Percentile:
#           0.0 to 0.026455026455. Mean: 0.0169847272297
# Low Twentieth Percentile:
#           0.026455026455 to 0.0373626373626. Mean: 0.032176872349
# Mid Twentieth Percentile:
#           0.0373692077728 to 0.047619047619. Mean: 0.0424653061236
# High Twentieth Percentile:
#           0.047619047619 to 0.0625. Mean: 0.0545061729062
# Top Twentieth Percentile:
#           0.0625 to 0.262247838617. Mean: 0.0832302742083
# Top Tenth Percentile:
#           0.0769230769231 to 0.262247838617. Mean: 0.0980860837316

# PL_WORDS:
# Standard Deviation: 480.817308743
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
#           383.0 to 9301.0. Mean: 885.375607386
# Top Tenth Percentile:
#           603.0 to 9301.0. Mean: 1306.06981318

# OBJECT_PERCENT:
# Standard Deviation: 0.0191627452151
# Bottom 10th Percentile:
#           0.0 to 0.0106382978723. Mean: 0.00448982316819
# Bottom 20th Percentile:
#           0.0 to 0.0167597765363. Mean: 0.00927612284957
# Low Twentieth Percentile:
#           0.0167597765363 to 0.0253164556962. Mean: 0.0212909825323
# Mid Twentieth Percentile:
#           0.0253164556962 to 0.0333333333333. Mean: 0.0292208800568
# High Twentieth Percentile:
#           0.0333333333333 to 0.044776119403. Mean: 0.0385016566216
# Top Twentieth Percentile:
#           0.044776119403 to 0.272727272727. Mean: 0.0606845562716
# Top Tenth Percentile:
#           0.0555555555556 to 0.272727272727. Mean: 0.0717875040416

# YOU_FREQ:
# Standard Deviation: 0.0157287859518
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0. Mean: 0.0
# Mid Twentieth Percentile:
#           0.0 to 0.00262467191601. Mean: 0.000220611952423
# High Twentieth Percentile:
#           0.00263157894737 to 0.0140845070423. Mean: 0.00770998751968
# Top Twentieth Percentile:
#           0.0140845070423 to 0.238095238095. Mean: 0.0334724000898
# Top Tenth Percentile:
#           0.0277777777778 to 0.238095238095. Mean: 0.0473766224211

# WL_MEAN:
# Standard Deviation: 0.49642951962
# Bottom 10th Percentile:
#           2.0 to 3.0. Mean: 2.96541786744
# Bottom 20th Percentile:
#           2.0 to 3.0. Mean: 2.9827006247
# Low Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# Mid Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# High Twentieth Percentile:
#           3.0 to 4.0. Mean: 3.57952907256
# Top Twentieth Percentile:
#           4.0 to 15.0. Mean: 4.0286686103
# Top Tenth Percentile:
#           4.0 to 15.0. Mean: 4.05801376598

# PASSIVE_PERCENT:
# Standard Deviation: 0.023402230311
# Bottom 10th Percentile:
#           0.0 to 0.0230769230769. Mean: 0.013606382269
# Bottom 20th Percentile:
#           0.0 to 0.0309278350515. Mean: 0.020444226883
# Low Twentieth Percentile:
#           0.0309278350515 to 0.0414746543779. Mean: 0.0364639008931
# Mid Twentieth Percentile:
#           0.0414746543779 to 0.0513833992095. Mean: 0.0463513548164
# High Twentieth Percentile:
#           0.0513833992095 to 0.065306122449. Mean: 0.0575335857237
# Top Twentieth Percentile:
#           0.0653266331658 to 0.393939393939. Mean: 0.0836374302865
# Top Tenth Percentile:
#           0.078125 to 0.393939393939. Mean: 0.0966150892697

# STANZAS:
# Standard Deviation: 34.0816983955
# Bottom 10th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Low Twentieth Percentile:
#           1.0 to 4.0. Mean: 2.52042287362
# Mid Twentieth Percentile:
#           4.0 to 7.0. Mean: 5.3109082172
# High Twentieth Percentile:
#           7.0 to 17.0. Mean: 11.2244113407
# Top Twentieth Percentile:
#           17.0 to 954.0. Mean: 51.5208940719
# Top Tenth Percentile:
#           33.0 to 954.0. Mean: 80.1435594887

# SL_MODE:
# Standard Deviation: 15.8050954111
# Bottom 10th Percentile:
#           0.0 to 1.0. Mean: 0.85590778098
# Bottom 20th Percentile:
#           0.0 to 1.0. Mean: 0.927919269582
# Low Twentieth Percentile:
#           1.0 to 4.0. Mean: 2.14368092263
# Mid Twentieth Percentile:
#           4.0 to 6.0. Mean: 4.50600672753
# High Twentieth Percentile:
#           6.0 to 14.0. Mean: 9.66170110524
# Top Twentieth Percentile:
#           14.0 to 383.0. Mean: 29.9008746356
# Top Tenth Percentile:
#           23.0 to 383.0. Mean: 42.610619469

# LEX_DIV:
# Standard Deviation: 0.112642103912
# Bottom 10th Percentile:
#           0.1 to 0.459595959596. Mean: 0.397395692594
# Bottom 20th Percentile:
#           0.1 to 0.512096774194. Mean: 0.443465536628
# Low Twentieth Percentile:
#           0.51214953271 to 0.579545454545. Mean: 0.547709654342
# Mid Twentieth Percentile:
#           0.579545454545 to 0.632352941176. Mean: 0.60613823569
# High Twentieth Percentile:
#           0.632352941176 to 0.691011235955. Mean: 0.659958895743
# Top Twentieth Percentile:
#           0.691056910569 to 1.0. Mean: 0.755504140733
# Top Tenth Percentile:
#           0.735632183908 to 1.0. Mean: 0.801288779479

# I_FREQ:
# Standard Deviation: 0.0207606764781
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.00401606425703. Mean: 0.000450434283336
# Mid Twentieth Percentile:
#           0.00403225806452 to 0.015037593985. Mean: 0.00939783138308
# High Twentieth Percentile:
#           0.015037593985 to 0.0304449648712. Mean: 0.0220391710395
# Top Twentieth Percentile:
#           0.0304568527919 to 0.260869565217. Mean: 0.0499104612673
# Top Tenth Percentile:
#           0.0446428571429 to 0.260869565217. Mean: 0.0633888950901

# ALLITERATION:
# Standard Deviation: 0.147257104015
# Bottom 10th Percentile:
#           0.0 to 0.15873015873. Mean: 0.105614230318
# Bottom 20th Percentile:
#           0.0 to 0.200617283951. Mean: 0.143512181091
# Low Twentieth Percentile:
#           0.200716845878 to 0.257042253521. Mean: 0.230654056385
# Mid Twentieth Percentile:
#           0.257042253521 to 0.304964539007. Mean: 0.280802245665
# High Twentieth Percentile:
#           0.305019305019 to 0.364452423698. Mean: 0.332546242362
# Top Twentieth Percentile:
#           0.364485981308 to 1.0. Mean: 0.499729729195
# Top Tenth Percentile:
#           0.423558897243 to 1.0. Mean: 0.612036959145

# SL_RANGE:
# Standard Deviation: 11.3647465346
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0. Mean: 0.0
# Mid Twentieth Percentile:
#           0.0 to 1.0. Mean: 0.661701105238
# High Twentieth Percentile:
#           1.0 to 5.0. Mean: 2.73666506487
# Top Twentieth Percentile:
#           5.0 to 268.0. Mean: 17.7405247813
# Top Tenth Percentile:
#           12.0 to 268.0. Mean: 27.5860373648

# SL_MEAN:
# Standard Deviation: 13.8025399685
# Bottom 10th Percentile:
#           0.203883495146 to 0.914285714286. Mean: 0.804204232859
# Bottom 20th Percentile:
#           0.203883495146 to 1.0. Mean: 0.893324945219
# Low Twentieth Percentile:
#           1.0 to 3.8. Mean: 2.56572467901
# Mid Twentieth Percentile:
#           3.8 to 6.0. Mean: 4.55353902605
# High Twentieth Percentile:
#           6.0 to 13.0. Mean: 8.68806315931
# Top Twentieth Percentile:
#           13.0833333333 to 383.0. Mean: 26.62809587
# Top Tenth Percentile:
#           21.0 to 383.0. Mean: 37.7774814674

# THE_FREQ:
# Standard Deviation: 0.0334374590689
# Bottom 10th Percentile:
#           0.0 to 0.0243902439024. Mean: 0.0120536044573
# Bottom 20th Percentile:
#           0.0 to 0.0375335120643. Mean: 0.0217891850659
# Low Twentieth Percentile:
#           0.037558685446 to 0.0551378446115. Mean: 0.0468336650878
# Mid Twentieth Percentile:
#           0.0551724137931 to 0.0701754385965. Mean: 0.0624823627011
# High Twentieth Percentile:
#           0.0701754385965 to 0.0901639344262. Mean: 0.0795070905581
# Top Twentieth Percentile:
#           0.0901639344262 to 0.5. Mean: 0.113729778097
# Top Tenth Percentile:
#           0.106796116505 to 0.5. Mean: 0.130025135523

# LL_RANGE:
# Standard Deviation: 183.703137865
# Bottom 10th Percentile:
#           0.0 to 12.0. Mean: 7.38520653218
# Bottom 20th Percentile:
#           0.0 to 15.0. Mean: 10.5728015377
# Low Twentieth Percentile:
#           15.0 to 22.0. Mean: 18.5415665545
# Mid Twentieth Percentile:
#           22.0 to 32.0. Mean: 26.5598270062
# High Twentieth Percentile:
#           32.0 to 45.0. Mean: 37.6410379625
# Top Twentieth Percentile:
#           45.0 to 8979.0. Mean: 124.672983479
# Top Tenth Percentile:
#           58.0 to 8979.0. Mean: 200.268436578

# COMMON_PERCENT:
# Standard Deviation: 0.0761024239026
# Bottom 10th Percentile:
#           0.140221402214 to 0.359355638166. Mean: 0.318082840078
# Bottom 20th Percentile:
#           0.140221402214 to 0.388692579505. Mean: 0.346832322679
# Low Twentieth Percentile:
#           0.388704318937 to 0.428571428571. Mean: 0.409433432313
# Mid Twentieth Percentile:
#           0.428571428571 to 0.463235294118. Mean: 0.445372829558
# High Twentieth Percentile:
#           0.463235294118 to 0.505518763797. Mean: 0.48270885957
# Top Twentieth Percentile:
#           0.505617977528 to 0.887372013652. Mean: 0.555164643029
# Top Tenth Percentile:
#           0.540178571429 to 0.887372013652. Mean: 0.589846977951

if __name__ == "__main__" or __name__ == "__console__":

    connect_to_db(app)
    print "Connected to DB."
