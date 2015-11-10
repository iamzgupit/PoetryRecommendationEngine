from Model import *
from server import app
from statistics import stdev, mean
import numpy as np
from sklearn.decomposition import RandomizedPCA


def get_ml_variance():
    raw_metrics = Metrics.query.all()
    all_metrics = []
    for m in raw_metrics:
        all_metrics.append([m.passive_percent, m.common_percent, m.poem_percent,
                            m.object_percent, m.abs_percent, m.male_percent,
                            m.female_percent, m.positive, m.negative, m.active_percent])

    print len(all_metrics)
    data = np.array(all_metrics)
    pca = RandomizedPCA(n_components=10, whiten=True)
    pca.fit(data)
    print pca.explained_variance_ratio_

    return pca


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
# Standard Deviation: 0.098068600398
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
# Standard Deviation: 0.027017727425
# Bottom 10th Percentile:
#           0.0 to 0.0366972477064. Mean: 0.0254223813509
# Bottom 20th Percentile:
#           0.0 to 0.046875. Mean: 0.0337545401333
# Low Twentieth Percentile:
#           0.046875 to 0.0595238095238. Mean: 0.0535184009218
# Mid Twentieth Percentile:
#           0.0595238095238 to 0.0711610486891. Mean: 0.065384567915
# High Twentieth Percentile:
#           0.071186440678 to 0.0873015873016. Mean: 0.0783607664635
# Top Twentieth Percentile:
#           0.0873015873016 to 0.393939393939. Mean: 0.107332316188
# Top Tenth Percentile:
#           0.101694915254 to 0.393939393939. Mean: 0.121711066502

# LL_MEDIAN:
# Standard Deviation: 211.785127484
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
#           44.0 to 3817.0. Mean: 177.836538462
# Top Tenth Percentile:
#           50.0 to 3817.0. Mean: 316.405775076

# RHYME:
# Standard Deviation: 0.859779282966
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.16. Mean: 0.053044674017
# Low Twentieth Percentile:
#           0.16 to 0.380952380952. Mean: 0.267136341233
# Mid Twentieth Percentile:
#           0.380952380952 to 0.666666666667. Mean: 0.519262742637
# High Twentieth Percentile:
#           0.666666666667 to 1.10344827586. Mean: 0.870452542971
# Top Twentieth Percentile:
#           1.10416666667 to 16.1904761905. Mean: 1.94436019922
# Top Tenth Percentile:
#           1.58823529412 to 16.1904761905. Mean: 2.61072380886

# MALE_PERCENT:
# Standard Deviation: 0.0200436382321
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0017667844523. Mean: 4.29271317664e-05
# Mid Twentieth Percentile:
#           0.0017667844523 to 0.00961538461538. Mean: 0.00588099144154
# High Twentieth Percentile:
#           0.00961538461538 to 0.0238095238095. Mean: 0.0157535813688
# Top Twentieth Percentile:
#           0.0238365493757 to 0.181818181818. Mean: 0.0469105444502
# Top Tenth Percentile:
#           0.0412844036697 to 0.181818181818. Mean: 0.0631000988783

# A_FREQ:
# Standard Deviation: 0.0196459687614
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0089485458613. Mean: 0.00267703950237
# Low Twentieth Percentile:
#           0.00896860986547 to 0.0174927113703. Mean: 0.0133388925748
# Mid Twentieth Percentile:
#           0.0174966352624 to 0.0258823529412. Mean: 0.0215987918382
# High Twentieth Percentile:
#           0.0259067357513 to 0.0375. Mean: 0.0309792704726
# Top Twentieth Percentile:
#           0.0375 to 0.272727272727. Mean: 0.0540897988091
# Top Tenth Percentile:
#           0.0483870967742 to 0.272727272727. Mean: 0.0664644846026

# NEGATIVE:
# Standard Deviation: 0.0221821617927
# Bottom 10th Percentile:
#           0.0 to 0.0161290322581. Mean: 0.00813804986751
# Bottom 20th Percentile:
#           0.0 to 0.0235294117647. Mean: 0.0141245203192
# Low Twentieth Percentile:
#           0.0235525024534 to 0.0334346504559. Mean: 0.0286233814033
# Mid Twentieth Percentile:
#           0.0334346504559 to 0.0429184549356. Mean: 0.03809765579
# High Twentieth Percentile:
#           0.0429252782194 to 0.0565217391304. Mean: 0.049003524114
# Top Twentieth Percentile:
#           0.0565217391304 to 0.393939393939. Mean: 0.0737657337424
# Top Tenth Percentile:
#           0.0689655172414 to 0.393939393939. Mean: 0.0862864765626

# LL_MODE:
# Standard Deviation: 249.347590188
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
#           47.0 to 7314.0. Mean: 199.732741617
# Top Tenth Percentile:
#           55.0 to 7314.0. Mean: 357.292806484

# SL_MEDIAN:
# Standard Deviation: 13.7515599589
# Bottom 10th Percentile:
#           0.0 to 1.0. Mean: 0.932756964457
# Bottom 20th Percentile:
#           0.0 to 1.0. Mean: 0.966362325805
# Low Twentieth Percentile:
#           1.0 to 4.0. Mean: 2.25708793849
# Mid Twentieth Percentile:
#           4.0 to 6.0. Mean: 4.39884670831
# High Twentieth Percentile:
#           6.0 to 13.0. Mean: 8.49111004325
# Top Twentieth Percentile:
#           13.0 to 383.0. Mean: 26.5138067061
# Top Tenth Percentile:
#           21.0 to 383.0. Mean: 37.9574468085

# PL_CHAR:
# Standard Deviation: 2222.05127405
# Bottom 10th Percentile:
#           16.0 to 352.0. Mean: 231.13832853
# Bottom 20th Percentile:
#           16.0 to 505.0. Mean: 331.808745795
# Low Twentieth Percentile:
#           505.0 to 696.0. Mean: 599.091302259
# Mid Twentieth Percentile:
#           696.0 to 1048.0. Mean: 861.388274868
# High Twentieth Percentile:
#           1048.0 to 1788.0. Mean: 1353.05189813
# Top Twentieth Percentile:
#           1788.0 to 45726.0. Mean: 4097.77613412
# Top Tenth Percentile:
#           2821.0 to 45726.0. Mean: 6092.19554205

# POEM_PERCENT:
# Standard Deviation: 0.083696050997
# Bottom 10th Percentile:
#           0.0 to 0.277456647399. Mean: 0.233448421424
# Bottom 20th Percentile:
#           0.0 to 0.311463590483. Mean: 0.264532997609
# Low Twentieth Percentile:
#           0.311475409836 to 0.354392892399. Mean: 0.334097986516
# Mid Twentieth Percentile:
#           0.354430379747 to 0.392045454545. Mean: 0.372854688381
# High Twentieth Percentile:
#           0.392045454545 to 0.441340782123. Mean: 0.415072438599
# Top Twentieth Percentile:
#           0.441358024691 to 0.851851851852. Mean: 0.495394425146
# Top Tenth Percentile:
#           0.481927710843 to 0.851851851852. Mean: 0.533285428408

# FEMALE_PERCENT:
# Standard Deviation: 0.0176761701517
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0. Mean: 0.0
# Mid Twentieth Percentile:
#           0.0 to 0.00418410041841. Mean: 0.00104977486555
# High Twentieth Percentile:
#           0.00418410041841 to 0.0147601476015. Mean: 0.00842878175625
# Top Twentieth Percentile:
#           0.0147783251232 to 0.169811320755. Mean: 0.0375332288788
# Top Tenth Percentile:
#           0.0304182509506 to 0.169811320755. Mean: 0.0546107337705

# IS_FREQ:
# Standard Deviation: 0.0127069145259
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.00307692307692. Mean: 0.000348380055275
# Mid Twentieth Percentile:
#           0.00308641975309 to 0.00892857142857. Mean: 0.00615425143906
# High Twentieth Percentile:
#           0.00892857142857 to 0.0166666666667. Mean: 0.0122444574531
# Top Twentieth Percentile:
#           0.0166666666667 to 0.25. Mean: 0.0290138805556
# Top Tenth Percentile:
#           0.0248447204969 to 0.25. Mean: 0.0384402804989

# LL_MEAN:
# Standard Deviation: 215.252967282
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
#           43.8918918919 to 3817.0. Mean: 181.662317301
# Top Tenth Percentile:
#           50.027027027 to 3817.0. Mean: 324.531325242

# ABS_PERCENT:
# Standard Deviation: 0.0154775422153
# Bottom 10th Percentile:
#           0.0 to 0.00452488687783. Mean: 0.000388773446333
# Bottom 20th Percentile:
#           0.0 to 0.00952380952381. Mean: 0.00390523790826
# Low Twentieth Percentile:
#           0.00952380952381 to 0.0162412993039. Mean: 0.0130655411158
# Mid Twentieth Percentile:
#           0.0162412993039 to 0.0225563909774. Mean: 0.0193393668897
# High Twentieth Percentile:
#           0.0225563909774 to 0.0314465408805. Mean: 0.0265161109766
# Top Twentieth Percentile:
#           0.0314606741573 to 0.25. Mean: 0.0445395841317
# Top Tenth Percentile:
#           0.0403225806452 to 0.25. Mean: 0.0541793529521

# PL_LINES:
# Standard Deviation: 55.1884394942
# Bottom 10th Percentile:
#           1.0 to 11.0. Mean: 6.10374639769
# Bottom 20th Percentile:
#           1.0 to 14.0. Mean: 9.47669389716
# Low Twentieth Percentile:
#           14.0 to 20.0. Mean: 16.5420470927
# Mid Twentieth Percentile:
#           20.0 to 29.0. Mean: 24.037962518
# High Twentieth Percentile:
#           29.0 to 48.0. Mean: 37.0019221528
# Top Twentieth Percentile:
#           48.0 to 893.0. Mean: 107.727317554
# Top Tenth Percentile:
#           77.0 to 893.0. Mean: 158.106382979

# WL_MODE:
# Standard Deviation: 1.26912772704
# Bottom 10th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Low Twentieth Percentile:
#           1.0 to 3.0. Mean: 2.49687650168
# Mid Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# High Twentieth Percentile:
#           3.0 to 4.0. Mean: 3.50312349832
# Top Twentieth Percentile:
#           4.0 to 55.0. Mean: 4.20857988166
# Top Tenth Percentile:
#           4.0 to 55.0. Mean: 4.42857142857

# WL_RANGE:
# Standard Deviation: 2.33004529284
# Bottom 10th Percentile:
#           3.0 to 8.0. Mean: 7.30451488953
# Bottom 20th Percentile:
#           3.0 to 9.0. Mean: 7.90485343585
# Low Twentieth Percentile:
#           9.0 to 10.0. Mean: 9.2931283037
# Mid Twentieth Percentile:
#           10.0 to 11.0. Mean: 10.2359442576
# High Twentieth Percentile:
#           11.0 to 12.0. Mean: 11.2839980778
# Top Twentieth Percentile:
#           12.0 to 126.0. Mean: 13.2036489152
# Top Tenth Percentile:
#           13.0 to 126.0. Mean: 14.2725430598

# WL_MEDIAN:
# Standard Deviation: 0.525349379794
# Bottom 10th Percentile:
#           1.0 to 3.0. Mean: 2.96061479347
# Bottom 20th Percentile:
#           1.0 to 3.0. Mean: 2.98029793369
# Low Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# Mid Twentieth Percentile:
#           3.0 to 4.0. Mean: 3.86352715041
# High Twentieth Percentile:
#           4.0 to 4.0. Mean: 4.0
# Top Twentieth Percentile:
#           4.0 to 7.0. Mean: 4.05276134122
# Top Tenth Percentile:
#           4.0 to 7.0. Mean: 4.10840932118

# POSITIVE:
# Standard Deviation: 0.0247248075374
# Bottom 10th Percentile:
#           0.0 to 0.0191082802548. Mean: 0.0108054231067
# Bottom 20th Percentile:
#           0.0 to 0.0265060240964. Mean: 0.0169969191088
# Low Twentieth Percentile:
#           0.026512013256 to 0.0374414976599. Mean: 0.0322387297404
# Mid Twentieth Percentile:
#           0.0374531835206 to 0.0478260869565. Mean: 0.0425723792903
# High Twentieth Percentile:
#           0.0478260869565 to 0.0625. Mean: 0.0546982644912
# Top Twentieth Percentile:
#           0.0625 to 0.262247838617. Mean: 0.0835296629853
# Top Tenth Percentile:
#           0.0774647887324 to 0.262247838617. Mean: 0.0987259726828

# PL_WORDS:
# Standard Deviation: 478.667245826
# Bottom 10th Percentile:
#           4.0 to 78.0. Mean: 51.6407300672
# Bottom 20th Percentile:
#           4.0 to 110.0. Mean: 73.2075925036
# Low Twentieth Percentile:
#           110.0 to 152.0. Mean: 130.574723691
# Mid Twentieth Percentile:
#           152.0 to 227.0. Mean: 186.651609803
# High Twentieth Percentile:
#           227.0 to 383.0. Mean: 292.701105238
# Top Twentieth Percentile:
#           383.0 to 9301.0. Mean: 882.442800789
# Top Tenth Percentile:
#           608.0 to 9301.0. Mean: 1311.63931104

# OBJECT_PERCENT:
# Standard Deviation: 0.0191788607923
# Bottom 10th Percentile:
#           0.0 to 0.0106951871658. Mean: 0.00449078884032
# Bottom 20th Percentile:
#           0.0 to 0.0167785234899. Mean: 0.00928366290955
# Low Twentieth Percentile:
#           0.0167785234899 to 0.0253807106599. Mean: 0.0213141730085
# Mid Twentieth Percentile:
#           0.0253807106599 to 0.0333333333333. Mean: 0.0292731923675
# High Twentieth Percentile:
#           0.0333333333333 to 0.045045045045. Mean: 0.0386321218443
# Top Twentieth Percentile:
#           0.045045045045 to 0.272727272727. Mean: 0.0608963144996
# Top Tenth Percentile:
#           0.056 to 0.272727272727. Mean: 0.0722701651813

# YOU_FREQ:
# Standard Deviation: 0.0157465747403
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0. Mean: 0.0
# Mid Twentieth Percentile:
#           0.0 to 0.00267379679144. Mean: 0.000232596017869
# High Twentieth Percentile:
#           0.00268096514745 to 0.0143198090692. Mean: 0.00782187060264
# Top Twentieth Percentile:
#           0.0143426294821 to 0.238095238095. Mean: 0.0337435292852
# Top Tenth Percentile:
#           0.0285714285714 to 0.238095238095. Mean: 0.0479587849638

# WL_MEAN:
# Standard Deviation: 0.496233318681
# Bottom 10th Percentile:
#           2.0 to 3.0. Mean: 2.96541786744
# Bottom 20th Percentile:
#           2.0 to 3.0. Mean: 2.9827006247
# Low Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# Mid Twentieth Percentile:
#           3.0 to 3.0. Mean: 3.0
# High Twentieth Percentile:
#           3.0 to 4.0. Mean: 3.58865929841
# Top Twentieth Percentile:
#           4.0 to 15.0. Mean: 4.02859960552
# Top Tenth Percentile:
#           4.0 to 15.0. Mean: 4.0587639311

# PASSIVE_PERCENT:
# Standard Deviation: 0.0234176407862
# Bottom 10th Percentile:
#           0.0 to 0.0230769230769. Mean: 0.0136145878783
# Bottom 20th Percentile:
#           0.0 to 0.0309734513274. Mean: 0.0204558899623
# Low Twentieth Percentile:
#           0.0309917355372 to 0.04158004158. Mean: 0.0365050430908
# Mid Twentieth Percentile:
#           0.0415913200723 to 0.0514705882353. Mean: 0.046423542321
# High Twentieth Percentile:
#           0.0514874141876 to 0.0655737704918. Mean: 0.057707596971
# Top Twentieth Percentile:
#           0.0656167979003 to 0.393939393939. Mean: 0.083880654695
# Top Tenth Percentile:
#           0.0786026200873 to 0.393939393939. Mean: 0.09713410682

# STANZAS:
# Standard Deviation: 34.1237029611
# Bottom 10th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile:
#           1.0 to 1.0. Mean: 1.0
# Low Twentieth Percentile:
#           1.0 to 4.0. Mean: 2.56222969726
# Mid Twentieth Percentile:
#           4.0 to 7.0. Mean: 5.35415665545
# High Twentieth Percentile:
#           7.0 to 17.0. Mean: 11.3685728015
# Top Twentieth Percentile:
#           17.0 to 954.0. Mean: 52.0315581854
# Top Tenth Percentile:
#           34.0 to 954.0. Mean: 81.5552178318

# SL_MODE:
# Standard Deviation: 15.8215290724
# Bottom 10th Percentile:
#           0.0 to 1.0. Mean: 0.85590778098
# Bottom 20th Percentile:
#           0.0 to 1.0. Mean: 0.927919269582
# Low Twentieth Percentile:
#           1.0 to 4.0. Mean: 2.18692936088
# Mid Twentieth Percentile:
#           4.0 to 6.0. Mean: 4.5348390197
# High Twentieth Percentile:
#           6.0 to 14.0. Mean: 9.77703027391
# Top Twentieth Percentile:
#           14.0 to 383.0. Mean: 30.1360946746
# Top Tenth Percentile:
#           24.0 to 383.0. Mean: 43.2006079027

# LEX_DIV:
# Standard Deviation: 0.112350844628
# Bottom 10th Percentile:
#           0.1 to 0.461340206186. Mean: 0.398775544905
# Bottom 20th Percentile:
#           0.1 to 0.51269035533. Mean: 0.44470720605
# Low Twentieth Percentile:
#           0.512727272727 to 0.580152671756. Mean: 0.548541338318
# Mid Twentieth Percentile:
#           0.580152671756 to 0.63309352518. Mean: 0.606864629068
# High Twentieth Percentile:
#           0.63309352518 to 0.691729323308. Mean: 0.660775502642
# Top Twentieth Percentile:
#           0.691780821918 to 1.0. Mean: 0.75644833758
# Top Tenth Percentile:
#           0.7375 to 1.0. Mean: 0.803261592629

# I_FREQ:
# Standard Deviation: 0.0207707308261
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.00406504065041. Mean: 0.000461579030066
# Mid Twentieth Percentile:
#           0.00406504065041 to 0.0151515151515. Mean: 0.00944830248207
# High Twentieth Percentile:
#           0.0151515151515 to 0.0307692307692. Mean: 0.0221608439511
# Top Twentieth Percentile:
#           0.0307692307692 to 0.260869565217. Mean: 0.0501495188874
# Top Tenth Percentile:
#           0.0451612903226 to 0.260869565217. Mean: 0.0639369450694

# ALLITERATION:
# Standard Deviation: 0.142645871008
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
#           0.364485981308 to 1.0. Mean: 0.492469944367
# Top Tenth Percentile:
#           0.423558897243 to 1.0. Mean: 0.600533791229

# SL_RANGE:
# Standard Deviation: 11.3789532075
# Bottom 10th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile:
#           0.0 to 0.0. Mean: 0.0
# Low Twentieth Percentile:
#           0.0 to 0.0. Mean: 0.0
# Mid Twentieth Percentile:
#           0.0 to 1.0. Mean: 0.676117251321
# High Twentieth Percentile:
#           1.0 to 5.0. Mean: 2.79432964921
# Top Twentieth Percentile:
#           5.0 to 268.0. Mean: 17.9289940828
# Top Tenth Percentile:
#           12.0 to 268.0. Mean: 28.0597771023

# SL_MEAN:
# Standard Deviation: 13.8164113089
# Bottom 10th Percentile:
#           0.203883495146 to 0.914285714286. Mean: 0.804204232859
# Bottom 20th Percentile:
#           0.203883495146 to 1.08333333333. Mean: 0.893738837306
# Low Twentieth Percentile:
#           1.08333333333 to 3.83333333333. Mean: 2.60583518206
# Mid Twentieth Percentile:
#           3.83333333333 to 6.0. Mean: 4.58509536133
# High Twentieth Percentile:
#           6.0 to 13.5. Mean: 8.79407528123
# Top Twentieth Percentile:
#           13.5 to 383.0. Mean: 26.8244625615
# Top Tenth Percentile:
#           21.0 to 383.0. Mean: 38.2874353114

# THE_FREQ:
# Standard Deviation: 0.0334696768754
# Bottom 10th Percentile:
#           0.0 to 0.0243902439024. Mean: 0.0120679785171
# Bottom 20th Percentile:
#           0.0 to 0.037558685446. Mean: 0.0218027034887
# Low Twentieth Percentile:
#           0.0375939849624 to 0.0552147239264. Mean: 0.0468816348144
# Mid Twentieth Percentile:
#           0.0552486187845 to 0.0703296703297. Mean: 0.0626089857943
# High Twentieth Percentile:
#           0.070351758794 to 0.0905172413793. Mean: 0.0797401364269
# Top Twentieth Percentile:
#           0.0905349794239 to 0.5. Mean: 0.114068580887
# Top Tenth Percentile:
#           0.107655502392 to 0.5. Mean: 0.13071782003

# LL_RANGE:
# Standard Deviation: 179.663028337
# Bottom 10th Percentile:
#           0.0 to 12.0. Mean: 7.69644572526
# Bottom 20th Percentile:
#           0.0 to 15.0. Mean: 10.7674195099
# Low Twentieth Percentile:
#           15.0 to 22.0. Mean: 18.6323882749
# Mid Twentieth Percentile:
#           22.0 to 32.0. Mean: 26.689572321
# High Twentieth Percentile:
#           32.0 to 45.0. Mean: 37.8097068717
# Top Twentieth Percentile:
#           45.0 to 8979.0. Mean: 123.111439842
# Top Tenth Percentile:
#           59.0 to 8979.0. Mean: 198.976697062

# COMMON_PERCENT:
# Standard Deviation: 0.0761343189787
# Bottom 10th Percentile:
#           0.140221402214 to 0.359375. Mean: 0.318129568916
# Bottom 20th Percentile:
#           0.140221402214 to 0.388888888889. Mean: 0.346922907322
# Low Twentieth Percentile:
#           0.388888888889 to 0.428571428571. Mean: 0.409635428773
# Mid Twentieth Percentile:
#           0.428666224287 to 0.463636363636. Mean: 0.445704655207
# High Twentieth Percentile:
#           0.463636363636 to 0.50643776824. Mean: 0.483222007958
# Top Twentieth Percentile:
#           0.506454816286 to 0.887372013652. Mean: 0.555805924393
# Top Tenth Percentile:
#           0.541666666667 to 0.887372013652. Mean: 0.591228527168


if __name__ == "__main__" or __name__ == "__console__":

    connect_to_db(app)
    print "Connected to DB."
