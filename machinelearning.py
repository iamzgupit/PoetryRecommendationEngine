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
    met_dict = {"wl_mean": sorted([m.wl_mean for m in metrics]),
                "wl_median": sorted([m.wl_median for m in metrics]),
                "wl_mode": sorted([m.wl_mode for m in metrics]),
                "wl_range": sorted([m.wl_range for m in metrics]),
                "ll_mean": sorted([m.ll_mean for m in metrics]),
                "ll_median": sorted([m.ll_median for m in metrics]),
                "ll_mode": sorted([m.ll_mode for m in metrics]),
                "ll_range": sorted([m.ll_range for m in metrics]),
                "pl_char": sorted([m.pl_char for m in metrics]),
                "pl_lines": sorted([m.pl_lines for m in metrics]),
                "pl_words": sorted([m.pl_words for m in metrics]),
                "lex_div": sorted([m.lex_div for m in metrics]),
                "the_freq": sorted([m.the_freq for m in metrics]),
                "i_freq": sorted([m.i_freq for m in metrics]),
                "you_freq": sorted([m.you_freq for m in metrics]),
                "is_freq": sorted([m.is_freq for m in metrics]),
                "a_freq": sorted([m.a_freq for m in metrics]),
                "common_percent": sorted([m.common_percent for m in metrics]),
                "poem_percent": sorted([m.poem_percent for m in metrics]),
                "object_percent": sorted([m.object_percent for m in metrics]),
                "abs_percent": sorted([m.abs_percent for m in metrics]),
                "male_percent": sorted([m.male_percent for m in metrics]),
                "female_percent": sorted([m.female_percent for m in metrics]),
                "alliteration": sorted([m.alliteration for m in metrics]),
                "positive": sorted([m.positive for m in metrics]),
                "negative": sorted([m.negative for m in metrics]),
                "active_percent": sorted([m.active_percent for m in metrics]),
                "passive_percent": sorted([m.passive_percent for m in metrics]),
                "end_repeat": sorted([m.end_repeat for m in metrics]),
                "rhyme": sorted([m.rhyme for m in metrics]),
                "stanzas": sorted([m.stanzas for m in metrics]),
                "sl_mean": sorted([m.sl_mean for m in metrics]),
                "sl_median": sorted([m.sl_median for m in metrics]),
                "sl_mode": sorted([m.sl_mode for m in metrics]),
                "sl_range": sorted([m.sl_range for m in metrics])}

    for key in met_dict.keys():

        data = met_dict[key]

        print "\n{}:".format(key.upper())
        dev = stdev(data)
        print "Standard Deviation: {}".format(dev)

        valuemax = max(data)
        valuemin = min(data)
        valuerange = (valuemax - valuemin)
        btmten_max = valuemin + (valuerange/10)
        btmtwen_max = valuemin + (valuerange/5)
        lowtwen_max = valuemin + 2 * (valuerange/5)
        midtwen_max = valuemin + 3 * (valuerange/5)
        hightwen_max = valuemin + 4 * (valuerange/5)
        topten_min = valuemax - (valuerange/10)

        unit_bottom_ten = data[:1041]
        minimum = min(unit_bottom_ten)
        maximum = max(unit_bottom_ten)
        average = mean(unit_bottom_ten)
        print "Bottom 10th Percentile By Unit:"
        print "          {} to {}. Mean: {}".format(minimum, maximum, average)

        val_bottom_ten = [n for n in data if n < btmten_max]
        try:
            minimum = min(val_bottom_ten)
            maximum = max(val_bottom_ten)
        except ValueError:
            minimum = 0
            maximum = btmten_max
        number = len(val_bottom_ten)
        print "Bottom 10th Percentile By Value:"
        print "          {} to {}. Units: {}".format(minimum, maximum, number)

        unit_bottom_twent = data[:2081]
        minimum = min(unit_bottom_twent)
        maximum = max(unit_bottom_twent)
        average = mean(unit_bottom_twent)
        print "Bottom 20th Percentile By Unit:"
        print "          {} to {}. Mean: {}".format(minimum, maximum, average)

        val_btm_twent = [n for n in data if n >= btmten_max and n < btmtwen_max]
        try:
            minimum = min(val_btm_twent)
            maximum = max(val_btm_twent)
        except ValueError:
            minimum = btmten_max
            maximum = btmtwen_max
        number = len(val_btm_twent)
        print "Bottom 20th Percentile By Value:"
        print "          {} to {}. Units: {}".format(minimum, maximum, number)

        unit_low_twent = data[2081:4162]
        minimum = min(unit_low_twent)
        maximum = max(unit_low_twent)
        average = mean(unit_low_twent)
        print "Low Twentieth Percentile By Unit:"
        print "          {} to {}. Mean: {}".format(minimum, maximum, average)

        val_low_twen = [n for n in data if n >= btmtwen_max and n < lowtwen_max]
        try:
            minimum = min(val_low_twen)
            maximum = max(val_low_twen)
        except ValueError:
            minimum = btmtwen_max
            maximum = lowtwen_max
        number = len(val_low_twen)
        print "Low 20th Percentile By Value:"
        print "          {} to {}. Units: {}".format(minimum, maximum, number)

        unit_mid_twent = data[4162:6243]
        minimum = min(unit_mid_twent)
        maximum = max(unit_mid_twent)
        average = mean(unit_mid_twent)
        print "Mid Twentieth Percentile By Unit:"
        print "          {} to {}. Mean: {}".format(minimum, maximum, average)

        val_mid_twen = [n for n in data if n >= lowtwen_max and n < midtwen_max]
        try:
            minimum = min(val_mid_twen)
            maximum = max(val_mid_twen)
        except ValueError:
            minimum = lowtwen_max
            maximum = midtwen_max
        number = len(val_mid_twen)
        print "Mid 20th Percentile By Value:"
        print "          {} to {}. Units: {}".format(minimum, maximum, number)

        unit_high_twent = data[6243:8324]
        minimum = min(unit_high_twent)
        maximum = max(unit_high_twent)
        average = mean(unit_high_twent)
        print "High Twentieth Percentile By Unit:"
        print "          {} to {}. Mean: {}".format(minimum, maximum, average)

        val_high_twen = [n for n in data if n >= midtwen_max and n < hightwen_max]
        try:
            minimum = min(val_high_twen)
            maximum = max(val_high_twen)
        except ValueError:
            minimum = midtwen_max
            maximum = hightwen_max
        number = len(val_high_twen)
        print "High 20th Percentile By Value:"
        print "          {} to {}. Units: {}".format(minimum, maximum, number)

        unit_top_twent = data[8324:]
        minimum = min(unit_top_twent)
        maximum = max(unit_top_twent)
        average = mean(unit_top_twent)
        print "Top Twentieth Percentile By Unit:"
        print "          {} to {}. Mean: {}".format(minimum, maximum, average)

        val_top_twen = [n for n in data if n >= hightwen_max]
        try:
            minimum = min(val_top_twen)
            maximum = max(val_top_twen)
        except ValueError:
            minimum = hightwen_max
            maximum = valuemax
        number = len(val_top_twen)
        print "High 20th Percentile By Value:"
        print "          {} to {}. Units: {}".format(minimum, maximum, number)

        unit_top_ten = data[9365:]
        minimum = min(unit_top_ten)
        maximum = max(unit_top_ten)
        average = mean(unit_top_ten)
        print "Top Tenth Percentile By Unit:"
        print "          {} to {}. Mean: {}".format(minimum, maximum, average)

        val_top_ten = [n for n in data if n >= topten_min]
        try:
            minimum = min(val_top_ten)
            maximum = max(val_top_ten)
        except ValueError:
            minimum = topten_min
            maximum = valuemax
        number = len(val_top_ten)
        print "High 20th Percentile By Value:"
        print "          {} to {}. Units: {}".format(minimum, maximum, number)

# END_REPEAT:
# Standard Deviation: 0.098068600398
# Bottom 10th Percentile By Unit:
#           0.117647058824 to 0.825. Mean: 0.705225473892
# Bottom 10th Percentile By Value:
#           0.117647058824 to 0.205128205128. Units: 9
# Bottom 20th Percentile By Unit:
#           0.117647058824 to 0.887096774194. Mean: 0.78205498557
# Bottom 20th Percentile By Value:
#           0.214285714286 to 0.285714285714. Units: 16
# Low Twentieth Percentile By Unit:
#           0.887096774194 to 0.944444444444. Mean: 0.919022199998
# Low 20th Percentile By Value:
#           0.3 to 0.469387755102. Units: 38
# Mid Twentieth Percentile By Unit:
#           0.944444444444 to 1.0. Mean: 0.966202037788
# Mid 20th Percentile By Value:
#           0.476635514019 to 0.64406779661. Units: 156
# High Twentieth Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# High 20th Percentile By Value:
#           0.647058823529 to 0.823076923077. Units: 802
# Top Twentieth Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# High 20th Percentile By Value:
#           0.823529411765 to 1.0. Units: 9331
# Top Tenth Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# High 20th Percentile By Value:
#           0.911764705882 to 1.0. Units: 7597

# ACTIVE_PERCENT:
# Standard Deviation: 0.027017727425
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0366972477064. Mean: 0.0254223813509
# Bottom 10th Percentile By Value:
#           0.0 to 0.0393700787402. Units: 1282
# Bottom 20th Percentile By Unit:
#           0.0 to 0.046875. Mean: 0.0337545401333
# Bottom 20th Percentile By Value:
#           0.0393939393939 to 0.0787401574803. Units: 6098
# Low Twentieth Percentile By Unit:
#           0.046875 to 0.0595238095238. Mean: 0.0535184009218
# Low 20th Percentile By Value:
#           0.0787878787879 to 0.157534246575. Units: 2908
# Mid Twentieth Percentile By Unit:
#           0.0595238095238 to 0.0711610486891. Mean: 0.065384567915
# Mid 20th Percentile By Value:
#           0.157894736842 to 0.235294117647. Units: 60
# High Twentieth Percentile By Unit:
#           0.071186440678 to 0.0873015873016. Mean: 0.0783607664635
# High 20th Percentile By Value:
#           0.24 to 0.285714285714. Units: 3
# Top Twentieth Percentile By Unit:
#           0.0873015873016 to 0.393939393939. Mean: 0.107332316188
# High 20th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1
# Top Tenth Percentile By Unit:
#           0.101694915254 to 0.393939393939. Mean: 0.121711066502
# High 20th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1

# LL_MEDIAN:
# Standard Deviation: 211.785127484
# Bottom 10th Percentile By Unit:
#           4.0 to 22.5. Mean: 17.7997118156
# Bottom 10th Percentile By Value:
#           4.0 to 384.0. Units: 10160
# Bottom 20th Percentile By Unit:
#           4.0 to 27.0. Mean: 21.4341662662
# Bottom 20th Percentile By Value:
#           392.0 to 759.0. Units: 61
# Low Twentieth Percentile By Unit:
#           27.0 to 33.5. Mean: 30.4245555022
# Low 20th Percentile By Value:
#           769.0 to 1529.0. Units: 64
# Mid Twentieth Percentile By Unit:
#           33.5 to 40.0. Mean: 36.4557904853
# Mid 20th Percentile By Value:
#           1538.0 to 2288.0. Units: 36
# High Twentieth Percentile By Unit:
#           40.0 to 44.0. Mean: 41.8844305622
# High 20th Percentile By Value:
#           2312.0 to 2911.0. Units: 19
# Top Twentieth Percentile By Unit:
#           44.0 to 3817.0. Mean: 177.836538462
# High 20th Percentile By Value:
#           3129.0 to 3817.0. Units: 12
# Top Tenth Percentile By Unit:
#           50.0 to 3817.0. Mean: 316.405775076
# High 20th Percentile By Value:
#           3469.0 to 3817.0. Units: 6

# RHYME:
# Standard Deviation: 0.859779282966
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 1.6170212766. Units: 9403
# Bottom 20th Percentile By Unit:
#           0.0 to 0.16. Mean: 0.053044674017
# Bottom 20th Percentile By Value:
#           1.61904761905 to 3.2050209205. Units: 775
# Low Twentieth Percentile By Unit:
#           0.16 to 0.380952380952. Mean: 0.267136341233
# Low 20th Percentile By Value:
#           3.24834437086 to 6.41290322581. Units: 155
# Mid Twentieth Percentile By Unit:
#           0.380952380952 to 0.666666666667. Mean: 0.519262742637
# Mid 20th Percentile By Value:
#           6.63636363636 to 9.53757961783. Units: 8
# High Twentieth Percentile By Unit:
#           0.666666666667 to 1.10344827586. Mean: 0.870452542971
# High 20th Percentile By Value:
#           9.77654320988 to 12.2142857143. Units: 7
# Top Twentieth Percentile By Unit:
#           1.10416666667 to 16.1904761905. Mean: 1.94436019922
# High 20th Percentile By Value:
#           13.2361111111 to 16.1904761905. Units: 4
# Top Tenth Percentile By Unit:
#           1.58823529412 to 16.1904761905. Mean: 2.61072380886
# High 20th Percentile By Value:
#           16.1904761905 to 16.1904761905. Units: 1

# MALE_PERCENT:
# Standard Deviation: 0.0200436382321
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.018166804294. Units: 7690
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.0181818181818 to 0.0362694300518. Units: 1443
# Low Twentieth Percentile By Unit:
#           0.0 to 0.0017667844523. Mean: 4.29271317664e-05
# Low 20th Percentile By Value:
#           0.0364145658263 to 0.0726643598616. Units: 982
# Mid Twentieth Percentile By Unit:
#           0.0017667844523 to 0.00961538461538. Mean: 0.00588099144154
# Mid 20th Percentile By Value:
#           0.0727272727273 to 0.107843137255. Units: 196
# High Twentieth Percentile By Unit:
#           0.00961538461538 to 0.0238095238095. Mean: 0.0157535813688
# High 20th Percentile By Value:
#           0.109375 to 0.142857142857. Units: 34
# Top Twentieth Percentile By Unit:
#           0.0238365493757 to 0.181818181818. Mean: 0.0469105444502
# High 20th Percentile By Value:
#           0.147058823529 to 0.181818181818. Units: 7
# Top Tenth Percentile By Unit:
#           0.0412844036697 to 0.181818181818. Mean: 0.0631000988783
# High 20th Percentile By Value:
#           0.175182481752 to 0.181818181818. Units: 2

# A_FREQ:
# Standard Deviation: 0.0196459687614
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0272614622057. Units: 6547
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0089485458613. Mean: 0.00267703950237
# Bottom 20th Percentile By Value:
#           0.0272727272727 to 0.0544747081712. Units: 3139
# Low Twentieth Percentile By Unit:
#           0.00896860986547 to 0.0174927113703. Mean: 0.0133388925748
# Low 20th Percentile By Value:
#           0.0545454545455 to 0.108108108108. Units: 626
# Mid Twentieth Percentile By Unit:
#           0.0174966352624 to 0.0258823529412. Mean: 0.0215987918382
# Mid 20th Percentile By Value:
#           0.109090909091 to 0.157894736842. Units: 30
# High Twentieth Percentile By Unit:
#           0.0259067357513 to 0.0375. Mean: 0.0309792704726
# High 20th Percentile By Value:
#           0.166666666667 to 0.203703703704. Units: 7
# Top Twentieth Percentile By Unit:
#           0.0375 to 0.272727272727. Mean: 0.0540897988091
# High 20th Percentile By Value:
#           0.222222222222 to 0.272727272727. Units: 3
# Top Tenth Percentile By Unit:
#           0.0483870967742 to 0.272727272727. Mean: 0.0664644846026
# High 20th Percentile By Value:
#           0.272727272727 to 0.272727272727. Units: 1

# NEGATIVE:
# Standard Deviation: 0.0221821617927
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0161290322581. Mean: 0.00813804986751
# Bottom 10th Percentile By Value:
#           0.0 to 0.0393928442356. Units: 5496
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0235294117647. Mean: 0.0141245203192
# Bottom 20th Percentile By Value:
#           0.0393939393939 to 0.0787401574803. Units: 4316
# Low Twentieth Percentile By Unit:
#           0.0235525024534 to 0.0334346504559. Mean: 0.0286233814033
# Low 20th Percentile By Value:
#           0.0788177339901 to 0.154471544715. Units: 533
# Mid Twentieth Percentile By Unit:
#           0.0334346504559 to 0.0429184549356. Mean: 0.03809765579
# Mid 20th Percentile By Value:
#           0.165048543689 to 0.181818181818. Units: 4
# High Twentieth Percentile By Unit:
#           0.0429252782194 to 0.0565217391304. Mean: 0.049003524114
# High 20th Percentile By Value:
#           0.25 to 0.285714285714. Units: 2
# Top Twentieth Percentile By Unit:
#           0.0565217391304 to 0.393939393939. Mean: 0.0737657337424
# High 20th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1
# Top Tenth Percentile By Unit:
#           0.0689655172414 to 0.393939393939. Mean: 0.0862864765626
# High 20th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1

# LL_MODE:
# Standard Deviation: 249.347590188
# Bottom 10th Percentile By Unit:
#           1.0 to 22.0. Mean: 14.911623439
# Bottom 10th Percentile By Value:
#           1.0 to 720.0. Units: 10207
# Bottom 20th Percentile By Unit:
#           1.0 to 28.0. Mean: 19.824603556
# Bottom 20th Percentile By Value:
#           734.0 to 1453.0. Units: 68
# Low Twentieth Percentile By Unit:
#           28.0 to 35.0. Mean: 31.4733301297
# Low 20th Percentile By Value:
#           1489.0 to 2911.0. Units: 62
# Mid Twentieth Percentile By Unit:
#           35.0 to 41.0. Mean: 38.3565593465
# Mid 20th Percentile By Value:
#           3129.0 to 4191.0. Units: 11
# High Twentieth Percentile By Unit:
#           41.0 to 47.0. Mean: 44.040365209
# High 20th Percentile By Value:
#           4388.8 to 5851.4. Units: 0
# Top Twentieth Percentile By Unit:
#           47.0 to 7314.0. Mean: 199.732741617
# High 20th Percentile By Value:
#           6037.0 to 7314.0. Units: 4
# Top Tenth Percentile By Unit:
#           55.0 to 7314.0. Mean: 357.292806484
# High 20th Percentile By Value:
#           7314.0 to 7314.0. Units: 1

# SL_MEDIAN:
# Standard Deviation: 13.7515599589
# Bottom 10th Percentile By Unit:
#           0.0 to 1.0. Mean: 0.932756964457
# Bottom 10th Percentile By Value:
#           0.0 to 38.0. Units: 10078
# Bottom 20th Percentile By Unit:
#           0.0 to 1.0. Mean: 0.966362325805
# Bottom 20th Percentile By Value:
#           39.0 to 76.0. Units: 213
# Low Twentieth Percentile By Unit:
#           1.0 to 4.0. Mean: 2.25708793849
# Low 20th Percentile By Value:
#           78.0 to 152.0. Units: 49
# Mid Twentieth Percentile By Unit:
#           4.0 to 6.0. Mean: 4.39884670831
# Mid 20th Percentile By Value:
#           155.0 to 210.0. Units: 9
# High Twentieth Percentile By Unit:
#           6.0 to 13.0. Mean: 8.49111004325
# High 20th Percentile By Value:
#           301.0 to 301.0. Units: 1
# Top Twentieth Percentile By Unit:
#           13.0 to 383.0. Mean: 26.5138067061
# High 20th Percentile By Value:
#           347.0 to 383.0. Units: 2
# Top Tenth Percentile By Unit:
#           21.0 to 383.0. Mean: 37.9574468085
# High 20th Percentile By Value:
#           347.0 to 383.0. Units: 2

# PL_CHAR:
# Standard Deviation: 2222.05127405
# Bottom 10th Percentile By Unit:
#           16.0 to 352.0. Mean: 231.13832853
# Bottom 10th Percentile By Value:
#           16.0 to 4567.0. Units: 9895
# Bottom 20th Percentile By Unit:
#           16.0 to 505.0. Mean: 331.808745795
# Bottom 20th Percentile By Value:
#           4587.0 to 9108.0. Units: 325
# Low Twentieth Percentile By Unit:
#           505.0 to 696.0. Mean: 599.091302259
# Low 20th Percentile By Value:
#           9167.0 to 17907.0. Units: 94
# Mid Twentieth Percentile By Unit:
#           696.0 to 1048.0. Mean: 861.388274868
# Mid 20th Percentile By Value:
#           18321.0 to 27002.0. Units: 28
# High Twentieth Percentile By Unit:
#           1048.0 to 1788.0. Mean: 1353.05189813
# High 20th Percentile By Value:
#           30119.0 to 34838.0. Units: 7
# Top Twentieth Percentile By Unit:
#           1788.0 to 45726.0. Mean: 4097.77613412
# High 20th Percentile By Value:
#           38971.0 to 45726.0. Units: 3
# Top Tenth Percentile By Unit:
#           2821.0 to 45726.0. Mean: 6092.19554205
# High 20th Percentile By Value:
#           42287.0 to 45726.0. Units: 2

# POEM_PERCENT:
# Standard Deviation: 0.083696050997
# Bottom 10th Percentile By Unit:
#           0.0 to 0.277456647399. Mean: 0.233448421424
# Bottom 10th Percentile By Value:
#           0.0 to 0.08. Units: 13
# Bottom 20th Percentile By Unit:
#           0.0 to 0.311463590483. Mean: 0.264532997609
# Bottom 20th Percentile By Value:
#           0.0922509225092 to 0.170212765957. Units: 72
# Low Twentieth Percentile By Unit:
#           0.311475409836 to 0.354392892399. Mean: 0.334097986516
# Low 20th Percentile By Value:
#           0.171171171171 to 0.340707964602. Units: 3362
# Mid Twentieth Percentile By Unit:
#           0.354430379747 to 0.392045454545. Mean: 0.372854688381
# Mid 20th Percentile By Value:
#           0.340740740741 to 0.51103843009. Units: 6367
# High Twentieth Percentile By Unit:
#           0.392045454545 to 0.441340782123. Mean: 0.415072438599
# High 20th Percentile By Value:
#           0.511111111111 to 0.68. Units: 511
# Top Twentieth Percentile By Unit:
#           0.441358024691 to 0.851851851852. Mean: 0.495394425146
# High 20th Percentile By Value:
#           0.68438538206 to 0.851851851852. Units: 27
# Top Tenth Percentile By Unit:
#           0.481927710843 to 0.851851851852. Mean: 0.533285428408
# High 20th Percentile By Value:
#           0.766666666667 to 0.851851851852. Units: 8

# FEMALE_PERCENT:
# Standard Deviation: 0.0176761701517
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0169779286927. Units: 8569
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.0169851380042 to 0.0338983050847. Units: 922
# Low Twentieth Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Low 20th Percentile By Value:
#           0.034 to 0.0677966101695. Units: 632
# Mid Twentieth Percentile By Unit:
#           0.0 to 0.00418410041841. Mean: 0.00104977486555
# Mid 20th Percentile By Value:
#           0.0679245283019 to 0.101851851852. Units: 186
# High Twentieth Percentile By Unit:
#           0.00418410041841 to 0.0147601476015. Mean: 0.00842878175625
# High 20th Percentile By Value:
#           0.102272727273 to 0.134078212291. Units: 34
# Top Twentieth Percentile By Unit:
#           0.0147783251232 to 0.169811320755. Mean: 0.0375332288788
# High 20th Percentile By Value:
#           0.137931034483 to 0.169811320755. Units: 9
# Top Tenth Percentile By Unit:
#           0.0304182509506 to 0.169811320755. Mean: 0.0546107337705
# High 20th Percentile By Value:
#           0.157894736842 to 0.169811320755. Units: 3

# IS_FREQ:
# Standard Deviation: 0.0127069145259
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0249221183801. Units: 9371
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.025 to 0.0495867768595. Units: 831
# Low Twentieth Percentile By Unit:
#           0.0 to 0.00307692307692. Mean: 0.000348380055275
# Low 20th Percentile By Value:
#           0.05 to 0.0958904109589. Units: 142
# Mid Twentieth Percentile By Unit:
#           0.00308641975309 to 0.00892857142857. Mean: 0.00615425143906
# Mid 20th Percentile By Value:
#           0.103773584906 to 0.146341463415. Units: 4
# High Twentieth Percentile By Unit:
#           0.00892857142857 to 0.0166666666667. Mean: 0.0122444574531
# High 20th Percentile By Value:
#           0.153846153846 to 0.181818181818. Units: 3
# Top Twentieth Percentile By Unit:
#           0.0166666666667 to 0.25. Mean: 0.0290138805556
# High 20th Percentile By Value:
#           0.25 to 0.25. Units: 1
# Top Tenth Percentile By Unit:
#           0.0248447204969 to 0.25. Mean: 0.0384402804989
# High 20th Percentile By Value:
#           0.25 to 0.25. Units: 1

# LL_MEAN:
# Standard Deviation: 215.252967282
# Bottom 10th Percentile By Unit:
#           4.27272727273 to 23.0. Mean: 18.3196430913
# Bottom 10th Percentile By Value:
#           4.27272727273 to 384.0. Units: 10157
# Bottom 20th Percentile By Unit:
#           4.27272727273 to 27.4756097561. Mean: 21.8836467704
# Bottom 20th Percentile By Value:
#           396.0 to 759.0. Units: 60
# Low Twentieth Percentile By Unit:
#           27.4761904762 to 33.3125. Mean: 30.4727562006
# Low 20th Percentile By Value:
#           769.0 to 1529.0. Units: 65
# Mid Twentieth Percentile By Unit:
#           33.3125 to 39.2666666667. Mean: 36.1512377915
# Mid 20th Percentile By Value:
#           1538.0 to 2288.0. Units: 38
# High Twentieth Percentile By Unit:
#           39.2666666667 to 43.8888888889. Mean: 41.623586093
# High 20th Percentile By Value:
#           2312.0 to 2911.0. Units: 20
# Top Twentieth Percentile By Unit:
#           43.8918918919 to 3817.0. Mean: 181.662317301
# High 20th Percentile By Value:
#           3129.0 to 3817.0. Units: 12
# Top Tenth Percentile By Unit:
#           50.027027027 to 3817.0. Mean: 324.531325242
# High 20th Percentile By Value:
#           3469.0 to 3817.0. Units: 6

# ABS_PERCENT:
# Standard Deviation: 0.0154775422153
# Bottom 10th Percentile By Unit:
#           0.0 to 0.00452488687783. Mean: 0.000388773446333
# Bottom 10th Percentile By Value:
#           0.0 to 0.0249433106576. Units: 6969
# Bottom 20th Percentile By Unit:
#           0.0 to 0.00952380952381. Mean: 0.00390523790826
# Bottom 20th Percentile By Value:
#           0.025 to 0.0497512437811. Units: 2907
# Low Twentieth Percentile By Unit:
#           0.00952380952381 to 0.0162412993039. Mean: 0.0130655411158
# Low 20th Percentile By Value:
#           0.05 to 0.0967741935484. Units: 457
# Mid Twentieth Percentile By Unit:
#           0.0162412993039 to 0.0225563909774. Mean: 0.0193393668897
# Mid 20th Percentile By Value:
#           0.1 to 0.146341463415. Units: 12
# High Twentieth Percentile By Unit:
#           0.0225563909774 to 0.0314465408805. Mean: 0.0265161109766
# High 20th Percentile By Value:
#           0.153846153846 to 0.176470588235. Units: 6
# Top Twentieth Percentile By Unit:
#           0.0314606741573 to 0.25. Mean: 0.0445395841317
# High 20th Percentile By Value:
#           0.25 to 0.25. Units: 1
# Top Tenth Percentile By Unit:
#           0.0403225806452 to 0.25. Mean: 0.0541793529521
# High 20th Percentile By Value:
#           0.25 to 0.25. Units: 1

# PL_LINES:
# Standard Deviation: 55.1884394942
# Bottom 10th Percentile By Unit:
#           1.0 to 11.0. Mean: 6.10374639769
# Bottom 10th Percentile By Value:
#           1.0 to 90.0. Units: 9594
# Bottom 20th Percentile By Unit:
#           1.0 to 14.0. Mean: 9.47669389716
# Bottom 20th Percentile By Value:
#           91.0 to 179.0. Units: 534
# Low Twentieth Percentile By Unit:
#           14.0 to 20.0. Mean: 16.5420470927
# Low 20th Percentile By Value:
#           180.0 to 356.0. Units: 156
# Mid Twentieth Percentile By Unit:
#           20.0 to 29.0. Mean: 24.037962518
# Mid 20th Percentile By Value:
#           359.0 to 534.0. Units: 46
# High Twentieth Percentile By Unit:
#           29.0 to 48.0. Mean: 37.0019221528
# High 20th Percentile By Value:
#           548.0 to 688.0. Units: 13
# Top Twentieth Percentile By Unit:
#           48.0 to 893.0. Mean: 107.727317554
# High 20th Percentile By Value:
#           728.0 to 893.0. Units: 9
# Top Tenth Percentile By Unit:
#           77.0 to 893.0. Mean: 158.106382979
# High 20th Percentile By Value:
#           810.0 to 893.0. Units: 4

# WL_MODE:
# Standard Deviation: 1.26912772704
# Bottom 10th Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# Bottom 10th Percentile By Value:
#           1.0 to 6.0. Units: 10339
# Bottom 20th Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile By Value:
#           7.0 to 9.0. Units: 12
# Low Twentieth Percentile By Unit:
#           1.0 to 3.0. Mean: 2.49687650168
# Low 20th Percentile By Value:
#           11.8 to 22.6. Units: 0
# Mid Twentieth Percentile By Unit:
#           3.0 to 3.0. Mean: 3.0
# Mid 20th Percentile By Value:
#           22.6 to 33.4. Units: 0
# High Twentieth Percentile By Unit:
#           3.0 to 4.0. Mean: 3.50312349832
# High 20th Percentile By Value:
#           33.4 to 44.2. Units: 0
# Top Twentieth Percentile By Unit:
#           4.0 to 55.0. Mean: 4.20857988166
# High 20th Percentile By Value:
#           55.0 to 55.0. Units: 1
# Top Tenth Percentile By Unit:
#           4.0 to 55.0. Mean: 4.42857142857
# High 20th Percentile By Value:
#           55.0 to 55.0. Units: 1

# WL_RANGE:
# Standard Deviation: 2.33004529284
# Bottom 10th Percentile By Unit:
#           3.0 to 8.0. Mean: 7.30451488953
# Bottom 10th Percentile By Value:
#           3.0 to 15.0. Units: 10226
# Bottom 20th Percentile By Unit:
#           3.0 to 9.0. Mean: 7.90485343585
# Bottom 20th Percentile By Value:
#           16.0 to 27.0. Units: 123
# Low Twentieth Percentile By Unit:
#           9.0 to 10.0. Mean: 9.2931283037
# Low 20th Percentile By Value:
#           34.0 to 34.0. Units: 1
# Mid Twentieth Percentile By Unit:
#           10.0 to 11.0. Mean: 10.2359442576
# Mid 20th Percentile By Value:
#           54.0 to 54.0. Units: 1
# High Twentieth Percentile By Unit:
#           11.0 to 12.0. Mean: 11.2839980778
# High 20th Percentile By Value:
#           76.8 to 101.4. Units: 0
# Top Twentieth Percentile By Unit:
#           12.0 to 126.0. Mean: 13.2036489152
# High 20th Percentile By Value:
#           126.0 to 126.0. Units: 1
# Top Tenth Percentile By Unit:
#           13.0 to 126.0. Mean: 14.2725430598
# High 20th Percentile By Value:
#           126.0 to 126.0. Units: 1

# WL_MEDIAN:
# Standard Deviation: 0.525349379794
# Bottom 10th Percentile By Unit:
#           1.0 to 3.0. Mean: 2.96061479347
# Bottom 10th Percentile By Value:
#           1.0 to 1.0. Units: 6
# Bottom 20th Percentile By Unit:
#           1.0 to 3.0. Mean: 2.98029793369
# Bottom 20th Percentile By Value:
#           2.0 to 2.0. Units: 29
# Low Twentieth Percentile By Unit:
#           3.0 to 3.0. Mean: 3.0
# Low 20th Percentile By Value:
#           3.0 to 3.0. Units: 4411
# Mid Twentieth Percentile By Unit:
#           3.0 to 4.0. Mean: 3.86352715041
# Mid 20th Percentile By Value:
#           4.0 to 4.0. Units: 5808
# High Twentieth Percentile By Unit:
#           4.0 to 4.0. Mean: 4.0
# High 20th Percentile By Value:
#           5.0 to 5.0. Units: 91
# Top Twentieth Percentile By Unit:
#           4.0 to 7.0. Mean: 4.05276134122
# High 20th Percentile By Value:
#           6.0 to 7.0. Units: 7
# Top Tenth Percentile By Unit:
#           4.0 to 7.0. Mean: 4.10840932118
# High 20th Percentile By Value:
#           7.0 to 7.0. Units: 2

# POSITIVE:
# Standard Deviation: 0.0247248075374
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0191082802548. Mean: 0.0108054231067
# Bottom 10th Percentile By Value:
#           0.0 to 0.0262172284644. Units: 2027
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0265060240964. Mean: 0.0169969191088
# Bottom 20th Percentile By Value:
#           0.0262295081967 to 0.0524412296564. Units: 4947
# Low Twentieth Percentile By Unit:
#           0.026512013256 to 0.0374414976599. Mean: 0.0322387297404
# Low 20th Percentile By Value:
#           0.0524590163934 to 0.104895104895. Units: 3111
# Mid Twentieth Percentile By Unit:
#           0.0374531835206 to 0.0478260869565. Mean: 0.0425723792903
# Mid 20th Percentile By Value:
#           0.104938271605 to 0.156626506024. Units: 246
# High Twentieth Percentile By Unit:
#           0.0478260869565 to 0.0625. Mean: 0.0546982644912
# High 20th Percentile By Value:
#           0.157894736842 to 0.2. Units: 15
# Top Twentieth Percentile By Unit:
#           0.0625 to 0.262247838617. Mean: 0.0835296629853
# High 20th Percentile By Value:
#           0.214285714286 to 0.262247838617. Units: 6
# Top Tenth Percentile By Unit:
#           0.0774647887324 to 0.262247838617. Mean: 0.0987259726828
# High 20th Percentile By Value:
#           0.236842105263 to 0.262247838617. Units: 3

# PL_WORDS:
# Standard Deviation: 478.667245826
# Bottom 10th Percentile By Unit:
#           4.0 to 78.0. Mean: 51.6407300672
# Bottom 10th Percentile By Value:
#           4.0 to 933.0. Units: 9857
# Bottom 20th Percentile By Unit:
#           4.0 to 110.0. Mean: 73.2075925036
# Bottom 20th Percentile By Value:
#           937.0 to 1861.0. Units: 351
# Low Twentieth Percentile By Unit:
#           110.0 to 152.0. Mean: 130.574723691
# Low 20th Percentile By Value:
#           1864.0 to 3712.0. Units: 101
# Mid Twentieth Percentile By Unit:
#           152.0 to 227.0. Mean: 186.651609803
# Mid 20th Percentile By Value:
#           3734.0 to 5427.0. Units: 32
# High Twentieth Percentile By Unit:
#           227.0 to 383.0. Mean: 292.701105238
# High 20th Percentile By Value:
#           5654.0 to 7241.0. Units: 6
# Top Twentieth Percentile By Unit:
#           383.0 to 9301.0. Mean: 882.442800789
# High 20th Percentile By Value:
#           7527.0 to 9301.0. Units: 5
# Top Tenth Percentile By Unit:
#           608.0 to 9301.0. Mean: 1311.63931104
# High 20th Percentile By Value:
#           8968.0 to 9301.0. Units: 2

# OBJECT_PERCENT:
# Standard Deviation: 0.0191788607923
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0106951871658. Mean: 0.00449078884032
# Bottom 10th Percentile By Value:
#           0.0 to 0.027266530334. Units: 4661
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0167785234899. Mean: 0.00928366290955
# Bottom 20th Percentile By Value:
#           0.0272727272727 to 0.0544217687075. Units: 4597
# Low Twentieth Percentile By Unit:
#           0.0167785234899 to 0.0253807106599. Mean: 0.0213141730085
# Low 20th Percentile By Value:
#           0.0545454545455 to 0.108108108108. Units: 1048
# Mid Twentieth Percentile By Unit:
#           0.0253807106599 to 0.0333333333333. Mean: 0.0292731923675
# Mid 20th Percentile By Value:
#           0.109375 to 0.158536585366. Units: 42
# High Twentieth Percentile By Unit:
#           0.0333333333333 to 0.045045045045. Mean: 0.0386321218443
# High 20th Percentile By Value:
#           0.16393442623 to 0.183908045977. Units: 3
# Top Twentieth Percentile By Unit:
#           0.045045045045 to 0.272727272727. Mean: 0.0608963144996
# High 20th Percentile By Value:
#           0.272727272727 to 0.272727272727. Units: 1
# Top Tenth Percentile By Unit:
#           0.056 to 0.272727272727. Mean: 0.0722701651813
# High 20th Percentile By Value:
#           0.272727272727 to 0.272727272727. Units: 1

# YOU_FREQ:
# Standard Deviation: 0.0157465747403
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0236842105263. Units: 9112
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.0238095238095 to 0.0474308300395. Units: 863
# Low Twentieth Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Low 20th Percentile By Value:
#           0.047619047619 to 0.0945945945946. Units: 345
# Mid Twentieth Percentile By Unit:
#           0.0 to 0.00267379679144. Mean: 0.000232596017869
# Mid 20th Percentile By Value:
#           0.0952380952381 to 0.141304347826. Units: 28
# High Twentieth Percentile By Unit:
#           0.00268096514745 to 0.0143198090692. Mean: 0.00782187060264
# High 20th Percentile By Value:
#           0.142857142857 to 0.153846153846. Units: 3
# Top Twentieth Percentile By Unit:
#           0.0143426294821 to 0.238095238095. Mean: 0.0337435292852
# High 20th Percentile By Value:
#           0.238095238095 to 0.238095238095. Units: 1
# Top Tenth Percentile By Unit:
#           0.0285714285714 to 0.238095238095. Mean: 0.0479587849638
# High 20th Percentile By Value:
#           0.238095238095 to 0.238095238095. Units: 1

# WL_MEAN:
# Standard Deviation: 0.496233318681
# Bottom 10th Percentile By Unit:
#           2.0 to 3.0. Mean: 2.96541786744
# Bottom 10th Percentile By Value:
#           2.0 to 3.0. Units: 7099
# Bottom 20th Percentile By Unit:
#           2.0 to 3.0. Mean: 2.9827006247
# Bottom 20th Percentile By Value:
#           4.0 to 4.0. Units: 3210
# Low Twentieth Percentile By Unit:
#           3.0 to 3.0. Mean: 3.0
# Low 20th Percentile By Value:
#           5.0 to 7.0. Units: 42
# Mid Twentieth Percentile By Unit:
#           3.0 to 3.0. Mean: 3.0
# Mid 20th Percentile By Value:
#           7.2 to 9.8. Units: 0
# High Twentieth Percentile By Unit:
#           3.0 to 4.0. Mean: 3.58865929841
# High 20th Percentile By Value:
#           9.8 to 12.4. Units: 0
# Top Twentieth Percentile By Unit:
#           4.0 to 15.0. Mean: 4.02859960552
# High 20th Percentile By Value:
#           15.0 to 15.0. Units: 1
# Top Tenth Percentile By Unit:
#           4.0 to 15.0. Mean: 4.0587639311
# High 20th Percentile By Value:
#           15.0 to 15.0. Units: 1

# PASSIVE_PERCENT:
# Standard Deviation: 0.0234176407862
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0230769230769. Mean: 0.0136145878783
# Bottom 10th Percentile By Value:
#           0.0 to 0.0393700787402. Units: 3693
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0309734513274. Mean: 0.0204558899623
# Bottom 20th Percentile By Value:
#           0.0393939393939 to 0.0787401574803. Units: 5679
# Low Twentieth Percentile By Unit:
#           0.0309917355372 to 0.04158004158. Mean: 0.0365050430908
# Low 20th Percentile By Value:
#           0.0787878787879 to 0.157142857143. Units: 967
# Mid Twentieth Percentile By Unit:
#           0.0415913200723 to 0.0514705882353. Mean: 0.046423542321
# Mid 20th Percentile By Value:
#           0.16 to 0.222222222222. Units: 11
# High Twentieth Percentile By Unit:
#           0.0514874141876 to 0.0655737704918. Mean: 0.057707596971
# High 20th Percentile By Value:
#           0.25 to 0.25. Units: 1
# Top Twentieth Percentile By Unit:
#           0.0656167979003 to 0.393939393939. Mean: 0.083880654695
# High 20th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1
# Top Tenth Percentile By Unit:
#           0.0786026200873 to 0.393939393939. Mean: 0.09713410682
# High 20th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1

# STANZAS:
# Standard Deviation: 34.1237029611
# Bottom 10th Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# Bottom 10th Percentile By Value:
#           1.0 to 96.0. Units: 10158
# Bottom 20th Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile By Value:
#           97.0 to 191.0. Units: 129
# Low Twentieth Percentile By Unit:
#           1.0 to 4.0. Mean: 2.56222969726
# Low 20th Percentile By Value:
#           196.0 to 377.0. Units: 50
# Mid Twentieth Percentile By Unit:
#           4.0 to 7.0. Mean: 5.35415665545
# Mid 20th Percentile By Value:
#           390.0 to 562.0. Units: 10
# High Twentieth Percentile By Unit:
#           7.0 to 17.0. Mean: 11.3685728015
# High 20th Percentile By Value:
#           595.0 to 747.0. Units: 3
# Top Twentieth Percentile By Unit:
#           17.0 to 954.0. Mean: 52.0315581854
# High 20th Percentile By Value:
#           768.0 to 954.0. Units: 2
# Top Tenth Percentile By Unit:
#           34.0 to 954.0. Mean: 81.5552178318
# High 20th Percentile By Value:
#           954.0 to 954.0. Units: 1

# SL_MODE:
# Standard Deviation: 15.8215290724
# Bottom 10th Percentile By Unit:
#           0.0 to 1.0. Mean: 0.85590778098
# Bottom 10th Percentile By Value:
#           0.0 to 38.0. Units: 9983
# Bottom 20th Percentile By Unit:
#           0.0 to 1.0. Mean: 0.927919269582
# Bottom 20th Percentile By Value:
#           39.0 to 76.0. Units: 292
# Low Twentieth Percentile By Unit:
#           1.0 to 4.0. Mean: 2.18692936088
# Low 20th Percentile By Value:
#           78.0 to 152.0. Units: 57
# Mid Twentieth Percentile By Unit:
#           4.0 to 6.0. Mean: 4.5348390197
# Mid 20th Percentile By Value:
#           154.0 to 210.0. Units: 13
# High Twentieth Percentile By Unit:
#           6.0 to 14.0. Mean: 9.77703027391
# High 20th Percentile By Value:
#           238.0 to 301.0. Units: 5
# Top Twentieth Percentile By Unit:
#           14.0 to 383.0. Mean: 30.1360946746
# High 20th Percentile By Value:
#           347.0 to 383.0. Units: 2
# Top Tenth Percentile By Unit:
#           24.0 to 383.0. Mean: 43.2006079027
# High 20th Percentile By Value:
#           347.0 to 383.0. Units: 2

# LEX_DIV:
# Standard Deviation: 0.112350844628
# Bottom 10th Percentile By Unit:
#           0.1 to 0.461340206186. Mean: 0.398775544905
# Bottom 10th Percentile By Value:
#           0.1 to 0.18740505455. Units: 8
# Bottom 20th Percentile By Unit:
#           0.1 to 0.51269035533. Mean: 0.44470720605
# Bottom 20th Percentile By Value:
#           0.193396226415 to 0.279245283019. Units: 34
# Low Twentieth Percentile By Unit:
#           0.512727272727 to 0.580152671756. Mean: 0.548541338318
# Low 20th Percentile By Value:
#           0.280343007916 to 0.459770114943. Units: 983
# Mid Twentieth Percentile By Unit:
#           0.580152671756 to 0.63309352518. Mean: 0.606864629068
# Mid 20th Percentile By Value:
#           0.460035523979 to 0.63981042654. Units: 5473
# High Twentieth Percentile By Unit:
#           0.63309352518 to 0.691729323308. Mean: 0.660775502642
# High 20th Percentile By Value:
#           0.64 to 0.819672131148. Units: 3563
# Top Twentieth Percentile By Unit:
#           0.691780821918 to 1.0. Mean: 0.75644833758
# High 20th Percentile By Value:
#           0.82 to 1.0. Units: 291
# Top Tenth Percentile By Unit:
#           0.7375 to 1.0. Mean: 0.803261592629
# High 20th Percentile By Value:
#           0.910447761194 to 1.0. Units: 64

# I_FREQ:
# Standard Deviation: 0.0207707308261
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0260586319218. Units: 7818
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.0260869565217 to 0.0520833333333. Units: 1870
# Low Twentieth Percentile By Unit:
#           0.0 to 0.00406504065041. Mean: 0.000461579030066
# Low 20th Percentile By Value:
#           0.0521739130435 to 0.103092783505. Units: 619
# Mid Twentieth Percentile By Unit:
#           0.00406504065041 to 0.0151515151515. Mean: 0.00944830248207
# Mid 20th Percentile By Value:
#           0.104761904762 to 0.151351351351. Units: 37
# High Twentieth Percentile By Unit:
#           0.0151515151515 to 0.0307692307692. Mean: 0.0221608439511
# High 20th Percentile By Value:
#           0.161616161616 to 0.178571428571. Units: 6
# Top Twentieth Percentile By Unit:
#           0.0307692307692 to 0.260869565217. Mean: 0.0501495188874
# High 20th Percentile By Value:
#           0.25 to 0.260869565217. Units: 2
# Top Tenth Percentile By Unit:
#           0.0451612903226 to 0.260869565217. Mean: 0.0639369450694
# High 20th Percentile By Value:
#           0.25 to 0.260869565217. Units: 2

# ALLITERATION:
# Standard Deviation: 0.142645871008
# Bottom 10th Percentile By Unit:
#           0.0 to 0.15873015873. Mean: 0.105614230318
# Bottom 10th Percentile By Value:
#           0.0 to 0.0995024875622. Units: 378
# Bottom 20th Percentile By Unit:
#           0.0 to 0.200617283951. Mean: 0.143512181091
# Bottom 20th Percentile By Value:
#           0.1 to 0.199312714777. Units: 1635
# Low Twentieth Percentile By Unit:
#           0.200716845878 to 0.257042253521. Mean: 0.230654056385
# Low 20th Percentile By Value:
#           0.2 to 0.399491094148. Units: 7023
# Mid Twentieth Percentile By Unit:
#           0.257042253521 to 0.304964539007. Mean: 0.280802245665
# Mid 20th Percentile By Value:
#           0.4 to 0.6. Units: 1012
# High Twentieth Percentile By Unit:
#           0.305019305019 to 0.364452423698. Mean: 0.332546242362
# High 20th Percentile By Value:
#           0.600554785021 to 0.79792746114. Units: 85
# Top Twentieth Percentile By Unit:
#           0.364485981308 to 1.0. Mean: 0.492469944367
# High 20th Percentile By Value:
#           0.8 to 1.0. Units: 219
# Top Tenth Percentile By Unit:
#           0.423558897243 to 1.0. Mean: 0.600533791229
# High 20th Percentile By Value:
#           0.901639344262 to 1.0. Units: 200

# SL_RANGE:
# Standard Deviation: 11.3789532075
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 26.0. Units: 10044
# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           27.0 to 53.0. Units: 225
# Low Twentieth Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Low 20th Percentile By Value:
#           54.0 to 106.0. Units: 64
# Mid Twentieth Percentile By Unit:
#           0.0 to 1.0. Mean: 0.676117251321
# Mid 20th Percentile By Value:
#           109.0 to 159.0. Units: 10
# High Twentieth Percentile By Unit:
#           1.0 to 5.0. Mean: 2.79432964921
# High 20th Percentile By Value:
#           161.0 to 193.0. Units: 5
# Top Twentieth Percentile By Unit:
#           5.0 to 268.0. Mean: 17.9289940828
# High 20th Percentile By Value:
#           237.0 to 268.0. Units: 4
# Top Tenth Percentile By Unit:
#           12.0 to 268.0. Mean: 28.0597771023
# High 20th Percentile By Value:
#           242.0 to 268.0. Units: 3

# SL_MEAN:
# Standard Deviation: 13.8164113089
# Bottom 10th Percentile By Unit:
#           0.203883495146 to 0.914285714286. Mean: 0.804204232859
# Bottom 10th Percentile By Value:
#           0.203883495146 to 38.3333333333. Units: 10072
# Bottom 20th Percentile By Unit:
#           0.203883495146 to 1.08333333333. Mean: 0.893738837306
# Bottom 20th Percentile By Value:
#           39.0 to 76.0. Units: 217
# Low Twentieth Percentile By Unit:
#           1.08333333333 to 3.83333333333. Mean: 2.60583518206
# Low 20th Percentile By Value:
#           79.0 to 152.0. Units: 51
# Mid Twentieth Percentile By Unit:
#           3.83333333333 to 6.0. Mean: 4.58509536133
# Mid 20th Percentile By Value:
#           155.0 to 210.0. Units: 9
# High Twentieth Percentile By Unit:
#           6.0 to 13.5. Mean: 8.79407528123
# High 20th Percentile By Value:
#           301.0 to 301.0. Units: 1
# Top Twentieth Percentile By Unit:
#           13.5 to 383.0. Mean: 26.8244625615
# High 20th Percentile By Value:
#           347.0 to 383.0. Units: 2
# Top Tenth Percentile By Unit:
#           21.0 to 383.0. Mean: 38.2874353114
# High 20th Percentile By Value:
#           347.0 to 383.0. Units: 2

# THE_FREQ:
# Standard Deviation: 0.0334696768754
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0243902439024. Mean: 0.0120679785171
# Bottom 10th Percentile By Value:
#           0.0 to 0.0499390986602. Units: 3456
# Bottom 20th Percentile By Unit:
#           0.0 to 0.037558685446. Mean: 0.0218027034887
# Bottom 20th Percentile By Value:
#           0.05 to 0.0996884735202. Units: 5485
# Low Twentieth Percentile By Unit:
#           0.0375939849624 to 0.0552147239264. Mean: 0.0468816348144
# Low 20th Percentile By Value:
#           0.1 to 0.197530864198. Units: 1384
# Mid Twentieth Percentile By Unit:
#           0.0552486187845 to 0.0703296703297. Mean: 0.0626089857943
# Mid 20th Percentile By Value:
#           0.2 to 0.272727272727. Units: 26
# High Twentieth Percentile By Unit:
#           0.070351758794 to 0.0905172413793. Mean: 0.0797401364269
# High 20th Percentile By Value:
#           0.3 to 0.4. Units: 0
# Top Twentieth Percentile By Unit:
#           0.0905349794239 to 0.5. Mean: 0.114068580887
# High 20th Percentile By Value:
#           0.5 to 0.5. Units: 1
# Top Tenth Percentile By Unit:
#           0.107655502392 to 0.5. Mean: 0.13071782003
# High 20th Percentile By Value:
#           0.5 to 0.5. Units: 1

# LL_RANGE:
# Standard Deviation: 179.663028337
# Bottom 10th Percentile By Unit:
#           0.0 to 12.0. Mean: 7.69644572526
# Bottom 10th Percentile By Value:
#           0.0 to 871.0. Units: 10323
# Bottom 20th Percentile By Unit:
#           0.0 to 15.0. Mean: 10.7674195099
# Bottom 20th Percentile By Value:
#           904.0 to 1719.0. Units: 19
# Low Twentieth Percentile By Unit:
#           15.0 to 22.0. Mean: 18.6323882749
# Low 20th Percentile By Value:
#           1891.0 to 3268.0. Units: 4
# Mid Twentieth Percentile By Unit:
#           22.0 to 32.0. Mean: 26.689572321
# Mid 20th Percentile By Value:
#           3840.0 to 3840.0. Units: 1
# High Twentieth Percentile By Unit:
#           32.0 to 45.0. Mean: 37.8097068717
# High 20th Percentile By Value:
#           6029.0 to 6186.0. Units: 3
# Top Twentieth Percentile By Unit:
#           45.0 to 8979.0. Mean: 123.111439842
# High 20th Percentile By Value:
#           7238.0 to 8979.0. Units: 2
# Top Tenth Percentile By Unit:
#           59.0 to 8979.0. Mean: 198.976697062
# High 20th Percentile By Value:
#           8979.0 to 8979.0. Units: 1

# COMMON_PERCENT:
# Standard Deviation: 0.0761343189787
# Bottom 10th Percentile By Unit:
#           0.140221402214 to 0.359375. Mean: 0.318129568916
# Bottom 10th Percentile By Value:
#           0.140221402214 to 0.214285714286. Units: 31
# Bottom 20th Percentile By Unit:
#           0.140221402214 to 0.388888888889. Mean: 0.346922907322
# Bottom 20th Percentile By Value:
#           0.217391304348 to 0.289473684211. Units: 176
# Low Twentieth Percentile By Unit:
#           0.388888888889 to 0.428571428571. Mean: 0.409635428773
# Low 20th Percentile By Value:
#           0.289855072464 to 0.43908045977. Units: 4611
# Mid Twentieth Percentile By Unit:
#           0.428666224287 to 0.463636363636. Mean: 0.445704655207
# Mid 20th Percentile By Value:
#           0.439093484419 to 0.588235294118. Units: 5171
# High Twentieth Percentile By Unit:
#           0.463636363636 to 0.50643776824. Mean: 0.483222007958
# High 20th Percentile By Value:
#           0.588709677419 to 0.734375. Units: 336
# Top Twentieth Percentile By Unit:
#           0.506454816286 to 0.887372013652. Mean: 0.555805924393
# High 20th Percentile By Value:
#           0.738007380074 to 0.887372013652. Units: 27
# Top Tenth Percentile By Unit:
#           0.541666666667 to 0.887372013652. Mean: 0.591228527168
# High 20th Percentile By Value:
#           0.821350762527 to 0.887372013652. Units: 7

if __name__ == "__main__" or __name__ == "__console__":

    connect_to_db(app)
    print "Connected to DB."
