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
        #Getting the indexes to find the percentiles for Unit
        unitmax = len(data)
        btmten_stop = unitmax/10
        btmtwen_stop = unitmax/5
        lowtwen_stop = 2 * btmtwen_stop
        midtwen_stop = 3 * btmtwen_stop
        hightwen_stop = 4 * btmtwen_stop
        topten_start = unitmax - btmten_stop

        #Getting the Values to find the percentiles for Value
        valuemax = max(data)
        valuemin = min(data)
        valuerange = (valuemax - valuemin)
        btmten_max = valuemin + (valuerange/10)
        btmtwen_max = valuemin + (valuerange/5)
        lowtwen_max = valuemin + 2 * (valuerange/5)
        midtwen_max = valuemin + 3 * (valuerange/5)
        hightwen_max = valuemin + 4 * (valuerange/5)
        topten_min = valuemax - (valuerange/10)

        unit_bottom_ten = data[:btmten_stop]
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

        unit_bottom_twent = data[:btmtwen_stop]
        minimum = min(unit_bottom_twent)
        maximum = max(unit_bottom_twent)
        average = mean(unit_bottom_twent)
        print "\nBottom 20th Percentile By Unit:"
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

        unit_low_twent = data[btmtwen_stop:lowtwen_stop]
        minimum = min(unit_low_twent)
        maximum = max(unit_low_twent)
        average = mean(unit_low_twent)
        print "\nLow Twentieth Percentile By Unit:"
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

        unit_mid_twent = data[lowtwen_stop:midtwen_stop]
        minimum = min(unit_mid_twent)
        maximum = max(unit_mid_twent)
        average = mean(unit_mid_twent)
        print "\nMid Twentieth Percentile By Unit:"
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

        unit_high_twent = data[midtwen_stop:hightwen_stop]
        minimum = min(unit_high_twent)
        maximum = max(unit_high_twent)
        average = mean(unit_high_twent)
        print "\nHigh Twentieth Percentile By Unit:"
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

        unit_top_twent = data[hightwen_stop:]
        minimum = min(unit_top_twent)
        maximum = max(unit_top_twent)
        average = mean(unit_top_twent)
        print "\nTop Twentieth Percentile By Unit:"
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

        unit_top_ten = data[topten_start:]
        minimum = min(unit_top_ten)
        maximum = max(unit_top_ten)
        average = mean(unit_top_ten)
        print "\nTop 10th Percentile By Unit:"
        print "          {} to {}. Mean: {}".format(minimum, maximum, average)

        val_top_ten = [n for n in data if n >= topten_min]
        try:
            minimum = min(val_top_ten)
            maximum = max(val_top_ten)
        except ValueError:
            minimum = topten_min
            maximum = valuemax
        number = len(val_top_ten)
        print "Top 10th Percentile By Value:"
        print "          {} to {}. Units: {}".format(minimum, maximum, number)


# END_REPEAT:
# Standard Deviation: 0.0976263055587
# Bottom 10th Percentile By Unit:
#           0.117647058824 to 0.825806451613. Mean: 0.706407909502
# Bottom 10th Percentile By Value:
#           0.117647058824 to 0.205128205128. Units: 9

# Bottom 20th Percentile By Unit:
#           0.117647058824 to 0.88679245283. Mean: 0.782732645812
# Bottom 20th Percentile By Value:
#           0.214285714286 to 0.285714285714. Units: 16

# Low Twentieth Percentile By Unit:
#           0.88679245283 to 0.942857142857. Mean: 0.918718593202
# Low 20th Percentile By Value:
#           0.3 to 0.469387755102. Units: 38

# Mid Twentieth Percentile By Unit:
#           0.942857142857 to 1.0. Mean: 0.965233800305
# Mid 20th Percentile By Value:
#           0.476635514019 to 0.64406779661. Units: 149

# High Twentieth Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# High 20th Percentile By Value:
#           0.647058823529 to 0.823076923077. Units: 793

# Top Twentieth Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# High 20th Percentile By Value:
#           0.823529411765 to 1.0. Units: 9296

# Top 10th Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# Top 10th Percentile By Value:
#           0.911764705882 to 1.0. Units: 7565

# ACTIVE_PERCENT:
# Standard Deviation: 0.0270604814933
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0365853658537. Mean: 0.0253225711844
# Bottom 10th Percentile By Value:
#           0.0 to 0.0393700787402. Units: 1278

# Bottom 20th Percentile By Unit:
#           0.0 to 0.046783625731. Mean: 0.0336597472905
# Bottom 20th Percentile By Value:
#           0.0393939393939 to 0.0787401574803. Units: 6053

# Low Twentieth Percentile By Unit:
#           0.0468018720749 to 0.0594059405941. Mean: 0.0534170748873
# Low 20th Percentile By Value:
#           0.0787878787879 to 0.157534246575. Units: 2906

# Mid Twentieth Percentile By Unit:
#           0.0594262295082 to 0.0710382513661. Mean: 0.0652794282976
# Mid 20th Percentile By Value:
#           0.157894736842 to 0.235294117647. Units: 60

# High Twentieth Percentile By Unit:
#           0.0710382513661 to 0.0869565217391. Mean: 0.0781587491035
# High 20th Percentile By Value:
#           0.24 to 0.285714285714. Units: 3

# Top Twentieth Percentile By Unit:
#           0.0869565217391 to 0.393939393939. Mean: 0.106997687007
# High 20th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1

# Top 10th Percentile By Unit:
#           0.100775193798 to 0.393939393939. Mean: 0.120844626102
# Top 10th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1

# LL_MEDIAN:
# Standard Deviation: 150.073286663
# Bottom 10th Percentile By Unit:
#           4.0 to 22.0. Mean: 17.7577669903
# Bottom 10th Percentile By Value:
#           4.0 to 217.0. Units: 10130

# Bottom 20th Percentile By Unit:
#           4.0 to 27.0. Mean: 21.3861650485
# Bottom 20th Percentile By Value:
#           264.0 to 490.0. Units: 26

# Low Twentieth Percentile By Unit:
#           27.0 to 33.0. Mean: 30.3453883495
# Low 20th Percentile By Value:
#           497.0 to 964.0. Units: 67

# Mid Twentieth Percentile By Unit:
#           33.0 to 39.5. Mean: 36.3145631068
# Mid 20th Percentile By Value:
#           984.0 to 1453.0. Units: 34

# High Twentieth Percentile By Unit:
#           39.5 to 44.0. Mean: 41.7580097087
# High 20th Percentile By Value:
#           1489.0 to 1907.0. Units: 30

# Top Twentieth Percentile By Unit:
#           44.0 to 2454.0. Mean: 137.072052402
# High 20th Percentile By Value:
#           2025.0 to 2454.0. Units: 14

# Top 10th Percentile By Unit:
#           49.5 to 2454.0. Mean: 228.194174757
# Top 10th Percentile By Value:
#           2241.0 to 2454.0. Units: 9

# RHYME:
# Standard Deviation: 0.839512572821
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 1.6170212766. Units: 9368

# Bottom 20th Percentile By Unit:
#           0.0 to 0.16. Mean: 0.0542844498201
# Bottom 20th Percentile By Value:
#           1.61904761905 to 3.2050209205. Units: 770

# Low Twentieth Percentile By Unit:
#           0.16 to 0.380952380952. Mean: 0.26694140657
# Low 20th Percentile By Value:
#           3.24834437086 to 6.41290322581. Units: 147

# Mid Twentieth Percentile By Unit:
#           0.380952380952 to 0.666666666667. Mean: 0.51617818825
# Mid 20th Percentile By Value:
#           6.63636363636 to 9.425. Units: 6

# High Twentieth Percentile By Unit:
#           0.666666666667 to 1.08333333333. Mean: 0.861840654701
# High 20th Percentile By Value:
#           9.84 to 12.2142857143. Units: 6

# Top Twentieth Percentile By Unit:
#           1.08421052632 to 16.1904761905. Mean: 1.90035094878
# High 20th Percentile By Value:
#           13.2361111111 to 16.1904761905. Units: 4

# Top 10th Percentile By Unit:
#           1.55238095238 to 16.1904761905. Mean: 2.51375134596
# Top 10th Percentile By Value:
#           16.1904761905 to 16.1904761905. Units: 1

# MALE_PERCENT:
# Standard Deviation: 0.0200597188672
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.018166804294. Units: 7665

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.0181818181818 to 0.0362694300518. Units: 1422

# Low Twentieth Percentile By Unit:
#           0.0 to 0.00140331181589. Mean: 1.50230865948e-05
# Low 20th Percentile By Value:
#           0.0364145658263 to 0.0726643598616. Units: 977

# Mid Twentieth Percentile By Unit:
#           0.00141743444366 to 0.00943396226415. Mean: 0.00572399302594
# Mid 20th Percentile By Value:
#           0.0727272727273 to 0.107843137255. Units: 196

# High Twentieth Percentile By Unit:
#           0.00943396226415 to 0.0233918128655. Mean: 0.0154084263611
# High 20th Percentile By Value:
#           0.109375 to 0.142857142857. Units: 34

# Top Twentieth Percentile By Unit:
#           0.0233918128655 to 0.181818181818. Mean: 0.0464403209392
# High 20th Percentile By Value:
#           0.147058823529 to 0.181818181818. Units: 7

# Top 10th Percentile By Unit:
#           0.04 to 0.181818181818. Mean: 0.0620961884159
# Top 10th Percentile By Value:
#           0.175182481752 to 0.181818181818. Units: 2

# A_FREQ:
# Standard Deviation: 0.0196834449341
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0272614622057. Units: 6516

# Bottom 20th Percentile By Unit:
#           0.0 to 0.00884955752212. Mean: 0.00261400178778
# Bottom 20th Percentile By Value:
#           0.0272727272727 to 0.0544747081712. Units: 3119

# Low Twentieth Percentile By Unit:
#           0.00884955752212 to 0.0173913043478. Mean: 0.0132313948131
# Low 20th Percentile By Value:
#           0.0545454545455 to 0.108108108108. Units: 626

# Mid Twentieth Percentile By Unit:
#           0.0173913043478 to 0.025641025641. Mean: 0.02145319725
# Mid 20th Percentile By Value:
#           0.109090909091 to 0.157894736842. Units: 30

# High Twentieth Percentile By Unit:
#           0.025641025641 to 0.037037037037. Mean: 0.0307663292436
# High 20th Percentile By Value:
#           0.166666666667 to 0.203703703704. Units: 7

# Top Twentieth Percentile By Unit:
#           0.037037037037 to 0.272727272727. Mean: 0.053807567953
# High 20th Percentile By Value:
#           0.222222222222 to 0.272727272727. Units: 3

# Top 10th Percentile By Unit:
#           0.047619047619 to 0.272727272727. Mean: 0.0656954059842
# Top 10th Percentile By Value:
#           0.272727272727 to 0.272727272727. Units: 1

# NEGATIVE:
# Standard Deviation: 0.0222196892319
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0161290322581. Mean: 0.00805923805901
# Bottom 10th Percentile By Value:
#           0.0 to 0.0393928442356. Units: 5461

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0235294117647. Mean: 0.0140450866678
# Bottom 20th Percentile By Value:
#           0.0393939393939 to 0.0787401574803. Units: 4300

# Low Twentieth Percentile By Unit:
#           0.0235294117647 to 0.0333333333333. Mean: 0.0285274469723
# Low 20th Percentile By Value:
#           0.0788177339901 to 0.154471544715. Units: 533

# Mid Twentieth Percentile By Unit:
#           0.0333333333333 to 0.0428571428571. Mean: 0.0379901716448
# Mid 20th Percentile By Value:
#           0.165048543689 to 0.181818181818. Units: 4

# High Twentieth Percentile By Unit:
#           0.0428571428571 to 0.0561797752809. Mean: 0.0488099230266
# High 20th Percentile By Value:
#           0.25 to 0.285714285714. Units: 2

# Top Twentieth Percentile By Unit:
#           0.0561797752809 to 0.393939393939. Mean: 0.0734706869063
# High 20th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1

# Top 10th Percentile By Unit:
#           0.0681818181818 to 0.393939393939. Mean: 0.0855400901129
# Top 10th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1

# LL_MODE:
# Standard Deviation: 155.0345479
# Bottom 10th Percentile By Unit:
#           1.0 to 21.0. Mean: 14.8689320388
# Bottom 10th Percentile By Value:
#           1.0 to 239.0. Units: 10117

# Bottom 20th Percentile By Unit:
#           1.0 to 27.0. Mean: 19.7689320388
# Bottom 20th Percentile By Value:
#           255.0 to 490.0. Units: 34

# Low Twentieth Percentile By Unit:
#           27.0 to 35.0. Mean: 31.3830097087
# Low 20th Percentile By Value:
#           498.0 to 964.0. Units: 65

# Mid Twentieth Percentile By Unit:
#           35.0 to 41.0. Mean: 38.2344660194
# Mid 20th Percentile By Value:
#           984.0 to 1453.0. Units: 38

# High Twentieth Percentile By Unit:
#           41.0 to 47.0. Mean: 43.8699029126
# High 20th Percentile By Value:
#           1489.0 to 1907.0. Units: 33

# Top Twentieth Percentile By Unit:
#           47.0 to 2454.0. Mean: 147.481804949
# High 20th Percentile By Value:
#           2025.0 to 2454.0. Units: 14

# Top 10th Percentile By Unit:
#           54.0 to 2454.0. Mean: 245.23592233
# Top 10th Percentile By Value:
#           2241.0 to 2454.0. Units: 9

# SL_MEDIAN:
# Standard Deviation: 13.7753169318
# Bottom 10th Percentile By Unit:
#           0.0 to 1.0. Mean: 0.932038834951
# Bottom 10th Percentile By Value:
#           0.0 to 38.0. Units: 10027

# Bottom 20th Percentile By Unit:
#           0.0 to 1.0. Mean: 0.966019417476
# Bottom 20th Percentile By Value:
#           39.0 to 76.0. Units: 213

# Low Twentieth Percentile By Unit:
#           1.0 to 4.0. Mean: 2.26359223301
# Low 20th Percentile By Value:
#           78.0 to 152.0. Units: 49

# Mid Twentieth Percentile By Unit:
#           4.0 to 6.0. Mean: 4.38058252427
# Mid 20th Percentile By Value:
#           155.0 to 210.0. Units: 9

# High Twentieth Percentile By Unit:
#           6.0 to 13.0. Mean: 8.37961165049
# High 20th Percentile By Value:
#           301.0 to 301.0. Units: 1

# Top Twentieth Percentile By Unit:
#           13.0 to 383.0. Mean: 26.2819019893
# High 20th Percentile By Value:
#           347.0 to 383.0. Units: 2

# Top 10th Percentile By Unit:
#           20.0 to 383.0. Mean: 37.2126213592
# Top 10th Percentile By Value:
#           347.0 to 383.0. Units: 2

# PL_CHAR:
# Standard Deviation: 1858.73008677
# Bottom 10th Percentile By Unit:
#           16.0 to 350.0. Mean: 229.857281553
# Bottom 10th Percentile By Value:
#           16.0 to 2484.0. Units: 9139

# Bottom 20th Percentile By Unit:
#           16.0 to 502.0. Mean: 330.056796117
# Bottom 20th Percentile By Value:
#           2487.0 to 4929.0. Units: 786

# Low Twentieth Percentile By Unit:
#           502.0 to 692.0. Mean: 596.192718447
# Low 20th Percentile By Value:
#           4954.0 to 9693.0. Units: 275

# Mid Twentieth Percentile By Unit:
#           692.0 to 1035.0. Mean: 852.466019417
# Mid 20th Percentile By Value:
#           10013.0 to 14823.0. Units: 59

# High Twentieth Percentile By Unit:
#           1035.0 to 1740.0. Mean: 1326.83592233
# High 20th Percentile By Value:
#           14947.0 to 19590.0. Units: 26

# Top Twentieth Percentile By Unit:
#           1741.0 to 24698.0. Mean: 3779.92042698
# High 20th Percentile By Value:
#           19908.0 to 24698.0. Units: 16

# Top 10th Percentile By Unit:
#           2676.0 to 24698.0. Mean: 5438.66116505
# Top 10th Percentile By Value:
#           22782.0 to 24698.0. Units: 5

# POEM_PERCENT:
# Standard Deviation: 0.0836913751278
# Bottom 10th Percentile By Unit:
#           0.0 to 0.276923076923. Mean: 0.233009413624
# Bottom 10th Percentile By Value:
#           0.0 to 0.08. Units: 13

# Bottom 20th Percentile By Unit:
#           0.0 to 0.310954063604. Mean: 0.264116257728
# Bottom 20th Percentile By Value:
#           0.0922509225092 to 0.170212765957. Units: 72

# Low Twentieth Percentile By Unit:
#           0.310975609756 to 0.353846153846. Mean: 0.333599533665
# Low 20th Percentile By Value:
#           0.171171171171 to 0.340707964602. Units: 3354

# Mid Twentieth Percentile By Unit:
#           0.353846153846 to 0.391025641026. Mean: 0.372151109045
# Mid 20th Percentile By Value:
#           0.340740740741 to 0.51103843009. Units: 6330

# High Twentieth Percentile By Unit:
#           0.391143911439 to 0.44. Mean: 0.414021699808
# High 20th Percentile By Value:
#           0.511111111111 to 0.68. Units: 505

# Top Twentieth Percentile By Unit:
#           0.440154440154 to 0.851851851852. Mean: 0.494059960719
# High 20th Percentile By Value:
#           0.68438538206 to 0.851851851852. Units: 27

# Top 10th Percentile By Unit:
#           0.479297365119 to 0.851851851852. Mean: 0.530586554104
# Top 10th Percentile By Value:
#           0.766666666667 to 0.851851851852. Units: 8

# FEMALE_PERCENT:
# Standard Deviation: 0.0177019615982
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0169779286927. Units: 8526

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.0169851380042 to 0.0338983050847. Units: 916

# Low Twentieth Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Low 20th Percentile By Value:
#           0.034 to 0.0677966101695. Units: 630

# Mid Twentieth Percentile By Unit:
#           0.0 to 0.00403225806452. Mean: 0.000962860421452
# Mid 20th Percentile By Value:
#           0.0679245283019 to 0.101851851852. Units: 186

# High Twentieth Percentile By Unit:
#           0.00403225806452 to 0.0143540669856. Mean: 0.00820579661835
# High 20th Percentile By Value:
#           0.102272727273 to 0.134078212291. Units: 34

# Top Twentieth Percentile By Unit:
#           0.0143540669856 to 0.169811320755. Mean: 0.037100721709
# High 20th Percentile By Value:
#           0.137931034483 to 0.169811320755. Units: 9

# Top 10th Percentile By Unit:
#           0.0295081967213 to 0.169811320755. Mean: 0.0535386889618
# Top 10th Percentile By Value:
#           0.157894736842 to 0.169811320755. Units: 3

# IS_FREQ:
# Standard Deviation: 0.0127257435437
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0249221183801. Units: 9324

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.025 to 0.0495867768595. Units: 827

# Low Twentieth Percentile By Unit:
#           0.0 to 0.00289855072464. Mean: 0.000298901116438
# Low 20th Percentile By Value:
#           0.05 to 0.0958904109589. Units: 142

# Mid Twentieth Percentile By Unit:
#           0.00289855072464 to 0.00882352941176. Mean: 0.0060595995142
# Mid 20th Percentile By Value:
#           0.103773584906 to 0.146341463415. Units: 4

# High Twentieth Percentile By Unit:
#           0.00882352941176 to 0.0164835164835. Mean: 0.0120944303858
# High 20th Percentile By Value:
#           0.153846153846 to 0.181818181818. Units: 3

# Top Twentieth Percentile By Unit:
#           0.0164835164835 to 0.25. Mean: 0.028780598562
# High 20th Percentile By Value:
#           0.25 to 0.25. Units: 1

# Top 10th Percentile By Unit:
#           0.0243902439024 to 0.25. Mean: 0.0378501149301
# Top 10th Percentile By Value:
#           0.25 to 0.25. Units: 1

# LL_MEAN:
# Standard Deviation: 149.957087309
# Bottom 10th Percentile By Unit:
#           4.27272727273 to 22.90625. Mean: 18.2702194054
# Bottom 10th Percentile By Value:
#           4.27272727273 to 218.0. Units: 10125

# Bottom 20th Percentile By Unit:
#           4.27272727273 to 27.3846153846. Mean: 21.8311424886
# Bottom 20th Percentile By Value:
#           259.5 to 490.0. Units: 31

# Low Twentieth Percentile By Unit:
#           27.3870967742 to 33.2272727273. Mean: 30.3955402825
# Low 20th Percentile By Value:
#           498.0 to 984.0. Units: 69

# Mid Twentieth Percentile By Unit:
#           33.2307692308 to 39.1333333333. Mean: 36.0199525147
# Mid 20th Percentile By Value:
#           997.0 to 1453.0. Units: 32

# High Twentieth Percentile By Unit:
#           39.1363636364 to 43.7142857143. Mean: 41.486481964
# High 20th Percentile By Value:
#           1489.0 to 1907.0. Units: 30

# Top Twentieth Percentile By Unit:
#           43.7142857143 to 2454.0. Mean: 137.643125411
# High 20th Percentile By Value:
#           2025.0 to 2454.0. Units: 14

# Top 10th Percentile By Unit:
#           49.1052631579 to 2454.0. Mean: 229.582390533
# Top 10th Percentile By Value:
#           2241.0 to 2454.0. Units: 9

# ABS_PERCENT:
# Standard Deviation: 0.0155043788776
# Bottom 10th Percentile By Unit:
#           0.0 to 0.00438596491228. Mean: 0.000345276307242
# Bottom 10th Percentile By Value:
#           0.0 to 0.0249433106576. Units: 6934

# Bottom 20th Percentile By Unit:
#           0.0 to 0.00943396226415. Mean: 0.00385551576891
# Bottom 20th Percentile By Value:
#           0.025 to 0.0497512437811. Units: 2891

# Low Twentieth Percentile By Unit:
#           0.00943396226415 to 0.0161290322581. Mean: 0.0129950851903
# Low 20th Percentile By Value:
#           0.05 to 0.0967741935484. Units: 457

# Mid Twentieth Percentile By Unit:
#           0.0161290322581 to 0.0224719101124. Mean: 0.019247069199
# Mid 20th Percentile By Value:
#           0.1 to 0.146341463415. Units: 12

# High Twentieth Percentile By Unit:
#           0.0224719101124 to 0.03125. Mean: 0.0263655260588
# High 20th Percentile By Value:
#           0.153846153846 to 0.176470588235. Units: 6

# Top Twentieth Percentile By Unit:
#           0.03125 to 0.25. Mean: 0.0443138106461
# High 20th Percentile By Value:
#           0.25 to 0.25. Units: 1

# Top 10th Percentile By Unit:
#           0.0397727272727 to 0.25. Mean: 0.0535867480352
# Top 10th Percentile By Value:
#           0.25 to 0.25. Units: 1

# PL_LINES:
# Standard Deviation: 47.5766775282
# Bottom 10th Percentile By Unit:
#           1.0 to 11.0. Mean: 6.32912621359
# Bottom 10th Percentile By Value:
#           1.0 to 62.0. Units: 8965

# Bottom 20th Percentile By Unit:
#           1.0 to 14.0. Mean: 9.61310679612
# Bottom 20th Percentile By Value:
#           63.0 to 124.0. Units: 908

# Low Twentieth Percentile By Unit:
#           14.0 to 20.0. Mean: 16.5330097087
# Low 20th Percentile By Value:
#           125.0 to 248.0. Units: 325

# Mid Twentieth Percentile By Unit:
#           20.0 to 29.0. Mean: 23.9393203883
# Mid 20th Percentile By Value:
#           249.0 to 371.0. Units: 56

# High Twentieth Percentile By Unit:
#           29.0 to 48.0. Mean: 36.6038834951
# High 20th Percentile By Value:
#           373.0 to 492.0. Units: 38

# Top Twentieth Percentile By Unit:
#           48.0 to 621.0. Mean: 101.123726346
# High 20th Percentile By Value:
#           510.0 to 621.0. Units: 9

# Top 10th Percentile By Unit:
#           74.0 to 621.0. Mean: 143.85631068
# Top 10th Percentile By Value:
#           567.0 to 621.0. Units: 4

# WL_MODE:
# Standard Deviation: 1.16082726581
# Bottom 10th Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# Bottom 10th Percentile By Value:
#           1.0 to 1.0. Units: 2324

# Bottom 20th Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile By Value:
#           2.0 to 2.0. Units: 523

# Low Twentieth Percentile By Unit:
#           1.0 to 3.0. Mean: 2.48980582524
# Low 20th Percentile By Value:
#           3.0 to 4.0. Units: 7141

# Mid Twentieth Percentile By Unit:
#           3.0 to 3.0. Mean: 3.0
# Mid 20th Percentile By Value:
#           5.0 to 5.0. Units: 271

# High Twentieth Percentile By Unit:
#           3.0 to 4.0. Mean: 3.48932038835
# High 20th Percentile By Value:
#           6.0 to 7.0. Units: 39

# Top Twentieth Percentile By Unit:
#           4.0 to 9.0. Mean: 4.18049490539
# High 20th Percentile By Value:
#           8.0 to 9.0. Units: 3

# Top 10th Percentile By Unit:
#           4.0 to 9.0. Mean: 4.36116504854
# Top 10th Percentile By Value:
#           9.0 to 9.0. Units: 2

# WL_RANGE:
# Standard Deviation: 1.97378856354
# Bottom 10th Percentile By Unit:
#           3.0 to 8.0. Mean: 7.29708737864
# Bottom 10th Percentile By Value:
#           3.0 to 6.0. Units: 150

# Bottom 20th Percentile By Unit:
#           3.0 to 9.0. Mean: 7.89368932039
# Bottom 20th Percentile By Value:
#           7.0 to 9.0. Units: 3402

# Low Twentieth Percentile By Unit:
#           9.0 to 10.0. Mean: 9.27572815534
# Low 20th Percentile By Value:
#           10.0 to 15.0. Units: 6630

# Mid Twentieth Percentile By Unit:
#           10.0 to 11.0. Mean: 10.209223301
# Mid 20th Percentile By Value:
#           16.0 to 21.0. Units: 108

# High Twentieth Percentile By Unit:
#           11.0 to 12.0. Mean: 11.2529126214
# High 20th Percentile By Value:
#           22.0 to 27.0. Units: 10

# Top Twentieth Percentile By Unit:
#           12.0 to 34.0. Mean: 13.0756914119
# High 20th Percentile By Value:
#           34.0 to 34.0. Units: 1

# Top 10th Percentile By Unit:
#           13.0 to 34.0. Mean: 14.027184466
# Top 10th Percentile By Value:
#           34.0 to 34.0. Units: 1

# WL_MEDIAN:
# Standard Deviation: 0.524867788695
# Bottom 10th Percentile By Unit:
#           1.0 to 3.0. Mean: 2.96213592233
# Bottom 10th Percentile By Value:
#           1.0 to 1.0. Units: 6

# Bottom 20th Percentile By Unit:
#           1.0 to 3.0. Mean: 2.98106796117
# Bottom 20th Percentile By Value:
#           2.0 to 2.0. Units: 27

# Low Twentieth Percentile By Unit:
#           3.0 to 3.0. Mean: 3.0
# Low 20th Percentile By Value:
#           3.0 to 3.0. Units: 4387

# Mid Twentieth Percentile By Unit:
#           3.0 to 4.0. Mean: 3.85436893204
# Mid 20th Percentile By Value:
#           4.0 to 4.0. Units: 5784

# High Twentieth Percentile By Unit:
#           4.0 to 4.0. Mean: 4.0
# High 20th Percentile By Value:
#           5.0 to 5.0. Units: 90

# Top Twentieth Percentile By Unit:
#           4.0 to 7.0. Mean: 4.05143134401
# High 20th Percentile By Value:
#           6.0 to 7.0. Units: 7

# Top 10th Percentile By Unit:
#           4.0 to 7.0. Mean: 4.10291262136
# Top 10th Percentile By Value:
#           7.0 to 7.0. Units: 2

# POSITIVE:
# Standard Deviation: 0.0247604142958
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0190476190476. Mean: 0.0107179176729
# Bottom 10th Percentile By Value:
#           0.0 to 0.0262172284644. Units: 2021

# Bottom 20th Percentile By Unit:
#           0.0 to 0.026402640264. Mean: 0.0169168440492
# Bottom 20th Percentile By Value:
#           0.0262295081967 to 0.0524412296564. Units: 4911

# Low Twentieth Percentile By Unit:
#           0.0264084507042 to 0.0373482726424. Mean: 0.0321406390265
# Low 20th Percentile By Value:
#           0.0524590163934 to 0.104895104895. Units: 3103

# Mid Twentieth Percentile By Unit:
#           0.0373532550694 to 0.047619047619. Mean: 0.0424590012761
# Mid 20th Percentile By Value:
#           0.104938271605 to 0.156626506024. Units: 245

# High Twentieth Percentile By Unit:
#           0.047619047619 to 0.0625. Mean: 0.0544822678548
# High 20th Percentile By Value:
#           0.157894736842 to 0.2. Units: 15

# Top Twentieth Percentile By Unit:
#           0.0625 to 0.262247838617. Mean: 0.0831658998622
# High 20th Percentile By Value:
#           0.214285714286 to 0.262247838617. Units: 6

# Top 10th Percentile By Unit:
#           0.0764705882353 to 0.262247838617. Mean: 0.0977787967257
# Top 10th Percentile By Value:
#           0.236842105263 to 0.262247838617. Units: 3

# PL_WORDS:
# Standard Deviation: 401.181562208
# Bottom 10th Percentile By Unit:
#           4.0 to 78.0. Mean: 51.359223301
# Bottom 10th Percentile By Value:
#           4.0 to 546.0. Units: 9177

# Bottom 20th Percentile By Unit:
#           4.0 to 109.0. Mean: 72.8334951456
# Bottom 20th Percentile By Value:
#           547.0 to 1088.0. Units: 761

# Low Twentieth Percentile By Unit:
#           109.0 to 151.0. Mean: 129.935436893
# Low 20th Percentile By Value:
#           1090.0 to 2166.0. Units: 266

# Mid Twentieth Percentile By Unit:
#           151.0 to 224.0. Mean: 184.748543689
# Mid 20th Percentile By Value:
#           2183.0 to 3224.0. Units: 59

# High Twentieth Percentile By Unit:
#           224.0 to 373.0. Mean: 287.177669903
# High 20th Percentile By Value:
#           3277.0 to 4295.0. Units: 23

# Top Twentieth Percentile By Unit:
#           374.0 to 5427.0. Mean: 814.865114022
# High 20th Percentile By Value:
#           4373.0 to 5427.0. Units: 15

# Top 10th Percentile By Unit:
#           576.0 to 5427.0. Mean: 1172.11262136
# Top 10th Percentile By Value:
#           4913.0 to 5427.0. Units: 6

# OBJECT_PERCENT:
# Standard Deviation: 0.0192117219235
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0106382978723. Mean: 0.00442741987828
# Bottom 10th Percentile By Value:
#           0.0 to 0.027266530334. Units: 4646

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0166666666667. Mean: 0.00921661862038
# Bottom 20th Percentile By Value:
#           0.0272727272727 to 0.0544217687075. Units: 4564

# Low Twentieth Percentile By Unit:
#           0.0166666666667 to 0.0252469813392. Mean: 0.0212209955545
# Low 20th Percentile By Value:
#           0.0545454545455 to 0.108108108108. Units: 1045

# Mid Twentieth Percentile By Unit:
#           0.0252491694352 to 0.0332103321033. Mean: 0.0291581774007
# Mid 20th Percentile By Value:
#           0.109375 to 0.158536585366. Units: 42

# High Twentieth Percentile By Unit:
#           0.0332103321033 to 0.044776119403. Mean: 0.0384526721686
# High 20th Percentile By Value:
#           0.16393442623 to 0.183908045977. Units: 3

# Top Twentieth Percentile By Unit:
#           0.044776119403 to 0.272727272727. Mean: 0.060617611381
# High 20th Percentile By Value:
#           0.272727272727 to 0.272727272727. Units: 1

# Top 10th Percentile By Unit:
#           0.0554156171285 to 0.272727272727. Mean: 0.0715714500081
# Top 10th Percentile By Value:
#           0.272727272727 to 0.272727272727. Units: 1

# YOU_FREQ:
# Standard Deviation: 0.0157765750851
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0236842105263. Units: 9063

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.0238095238095 to 0.0474308300395. Units: 861

# Low Twentieth Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Low 20th Percentile By Value:
#           0.047619047619 to 0.0945945945946. Units: 345

# Mid Twentieth Percentile By Unit:
#           0.0 to 0.00246913580247. Mean: 0.000176416236528
# Mid 20th Percentile By Value:
#           0.0952380952381 to 0.141304347826. Units: 28

# High Twentieth Percentile By Unit:
#           0.00246913580247 to 0.0139616055846. Mean: 0.00759444381159
# High 20th Percentile By Value:
#           0.142857142857 to 0.153846153846. Units: 3

# Top Twentieth Percentile By Unit:
#           0.0139720558882 to 0.238095238095. Mean: 0.0334065495943
# High 20th Percentile By Value:
#           0.238095238095 to 0.238095238095. Units: 1

# Top 10th Percentile By Unit:
#           0.0275862068966 to 0.238095238095. Mean: 0.0471219089432
# Top 10th Percentile By Value:
#           0.238095238095 to 0.238095238095. Units: 1

# WL_MEAN:
# Standard Deviation: 0.482608507982
# Bottom 10th Percentile By Unit:
#           2.0 to 3.0. Mean: 2.96699029126
# Bottom 10th Percentile By Value:
#           2.0 to 2.0. Units: 34

# Bottom 20th Percentile By Unit:
#           2.0 to 3.0. Mean: 2.98349514563
# Bottom 20th Percentile By Value:
#           2.5 to 3.0. Units: 0

# Low Twentieth Percentile By Unit:
#           3.0 to 3.0. Mean: 3.0
# Low 20th Percentile By Value:
#           3.0 to 3.0. Units: 7029

# Mid Twentieth Percentile By Unit:
#           3.0 to 3.0. Mean: 3.0
# Mid 20th Percentile By Value:
#           4.0 to 4.0. Units: 3196

# High Twentieth Percentile By Unit:
#           3.0 to 4.0. Mean: 3.5713592233
# High 20th Percentile By Value:
#           5.0 to 5.0. Units: 38

# Top Twentieth Percentile By Unit:
#           4.0 to 7.0. Mean: 4.02280446385
# High 20th Percentile By Value:
#           6.0 to 7.0. Units: 4

# Top 10th Percentile By Unit:
#           4.0 to 7.0. Mean: 4.04563106796
# Top 10th Percentile By Value:
#           7.0 to 7.0. Units: 1

# PASSIVE_PERCENT:
# Standard Deviation: 0.0234606025313
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0229132569558. Mean: 0.0135249599639
# Bottom 10th Percentile By Value:
#           0.0 to 0.0393700787402. Units: 3674

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0307692307692. Mean: 0.0203602821633
# Bottom 20th Percentile By Value:
#           0.0393939393939 to 0.0787401574803. Units: 5647

# Low Twentieth Percentile By Unit:
#           0.0308310991957 to 0.0414364640884. Mean: 0.0364210942529
# Low 20th Percentile By Value:
#           0.0787878787879 to 0.157142857143. Units: 967

# Mid Twentieth Percentile By Unit:
#           0.0414364640884 to 0.0513833992095. Mean: 0.046327425862
# Mid 20th Percentile By Value:
#           0.16 to 0.222222222222. Units: 11

# High Twentieth Percentile By Unit:
#           0.0513833992095 to 0.0652173913043. Mean: 0.0575249466844
# High 20th Percentile By Value:
#           0.25 to 0.25. Units: 1

# Top Twentieth Percentile By Unit:
#           0.0652173913043 to 0.393939393939. Mean: 0.0835821047405
# High 20th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1

# Top 10th Percentile By Unit:
#           0.0778443113772 to 0.393939393939. Mean: 0.0963448170227
# Top 10th Percentile By Value:
#           0.393939393939 to 0.393939393939. Units: 1

# STANZAS:
# Standard Deviation: 30.7131102815
# Bottom 10th Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# Bottom 10th Percentile By Value:
#           1.0 to 75.0. Units: 10008

# Bottom 20th Percentile By Unit:
#           1.0 to 1.0. Mean: 1.0
# Bottom 20th Percentile By Value:
#           76.0 to 150.0. Units: 203

# Low Twentieth Percentile By Unit:
#           1.0 to 4.0. Mean: 2.55436893204
# Low 20th Percentile By Value:
#           152.0 to 290.0. Units: 65

# Mid Twentieth Percentile By Unit:
#           4.0 to 7.0. Mean: 5.31747572816
# Mid 20th Percentile By Value:
#           310.0 to 436.0. Units: 22

# High Twentieth Percentile By Unit:
#           7.0 to 17.0. Mean: 11.1509708738
# High 20th Percentile By Value:
#           549.0 to 595.0. Units: 2

# Top Twentieth Percentile By Unit:
#           17.0 to 747.0. Mean: 49.5977680738
# High 20th Percentile By Value:
#           747.0 to 747.0. Units: 1

# Top 10th Percentile By Unit:
#           32.0 to 747.0. Mean: 76.0834951456
# Top 10th Percentile By Value:
#           747.0 to 747.0. Units: 1

# SL_MODE:
# Standard Deviation: 15.8500430053
# Bottom 10th Percentile By Unit:
#           0.0 to 1.0. Mean: 0.854368932039
# Bottom 10th Percentile By Value:
#           0.0 to 38.0. Units: 9932

# Bottom 20th Percentile By Unit:
#           0.0 to 1.0. Mean: 0.927184466019
# Bottom 20th Percentile By Value:
#           39.0 to 76.0. Units: 292

# Low Twentieth Percentile By Unit:
#           1.0 to 4.0. Mean: 2.19417475728
# Low 20th Percentile By Value:
#           78.0 to 152.0. Units: 57

# Mid Twentieth Percentile By Unit:
#           4.0 to 6.0. Mean: 4.51893203883
# Mid 20th Percentile By Value:
#           154.0 to 210.0. Units: 13

# High Twentieth Percentile By Unit:
#           6.0 to 14.0. Mean: 9.66796116505
# High 20th Percentile By Value:
#           238.0 to 301.0. Units: 5

# Top Twentieth Percentile By Unit:
#           14.0 to 383.0. Mean: 29.864628821
# High 20th Percentile By Value:
#           347.0 to 383.0. Units: 2

# Top 10th Percentile By Unit:
#           23.0 to 383.0. Mean: 42.3582524272
# Top 10th Percentile By Value:
#           347.0 to 383.0. Units: 2

# LEX_DIV:
# Standard Deviation: 0.111424203061
# Bottom 10th Percentile By Unit:
#           0.1 to 0.46332046332. Mean: 0.402260481338
# Bottom 10th Percentile By Value:
#           0.1 to 0.179316888046. Units: 7

# Bottom 20th Percentile By Unit:
#           0.1 to 0.513422818792. Mean: 0.446994456469
# Bottom 20th Percentile By Value:
#           0.193396226415 to 0.279245283019. Units: 24

# Low Twentieth Percentile By Unit:
#           0.513432835821 to 0.580357142857. Mean: 0.549052457934
# Low 20th Percentile By Value:
#           0.280343007916 to 0.459770114943. Units: 960

# Mid Twentieth Percentile By Unit:
#           0.58041958042 to 0.632850241546. Mean: 0.606809203679
# Mid 20th Percentile By Value:
#           0.460035523979 to 0.63981042654. Units: 5456

# High Twentieth Percentile By Unit:
#           0.632911392405 to 0.690789473684. Mean: 0.660124219574
# High 20th Percentile By Value:
#           0.64 to 0.819672131148. Units: 3563

# Top Twentieth Percentile By Unit:
#           0.690789473684 to 1.0. Mean: 0.755405696516
# High 20th Percentile By Value:
#           0.82 to 1.0. Units: 291

# Top 10th Percentile By Unit:
#           0.734939759036 to 1.0. Mean: 0.800456413192
# Top 10th Percentile By Value:
#           0.910447761194 to 1.0. Units: 64

# I_FREQ:
# Standard Deviation: 0.0207942184043
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 0.0260586319218. Units: 7777

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           0.0260869565217 to 0.0520833333333. Units: 1862

# Low Twentieth Percentile By Unit:
#           0.0 to 0.00384615384615. Mean: 0.000402156117364
# Low 20th Percentile By Value:
#           0.0521739130435 to 0.103092783505. Units: 617

# Mid Twentieth Percentile By Unit:
#           0.00384615384615 to 0.0149253731343. Mean: 0.00928435611515
# Mid 20th Percentile By Value:
#           0.104761904762 to 0.151351351351. Units: 37

# High Twentieth Percentile By Unit:
#           0.0149253731343 to 0.030303030303. Mean: 0.0218916581308
# High 20th Percentile By Value:
#           0.161616161616 to 0.178571428571. Units: 6

# Top Twentieth Percentile By Unit:
#           0.030303030303 to 0.260869565217. Mean: 0.0497790400619
# High 20th Percentile By Value:
#           0.25 to 0.260869565217. Units: 2

# Top 10th Percentile By Unit:
#           0.0443458980044 to 0.260869565217. Mean: 0.0630971797115
# Top 10th Percentile By Value:
#           0.25 to 0.260869565217. Units: 2

# ALLITERATION:
# Standard Deviation: 0.137536862214
# Bottom 10th Percentile By Unit:
#           0.0 to 0.158273381295. Mean: 0.105050018437
# Bottom 10th Percentile By Value:
#           0.0 to 0.0995024875622. Units: 378

# Bottom 20th Percentile By Unit:
#           0.0 to 0.2. Mean: 0.142956243832
# Bottom 20th Percentile By Value:
#           0.1 to 0.199312714777. Units: 1634

# Low Twentieth Percentile By Unit:
#           0.2 to 0.256302521008. Mean: 0.229887457695
# Low 20th Percentile By Value:
#           0.2 to 0.399491094148. Units: 7007

# Mid Twentieth Percentile By Unit:
#           0.256310679612 to 0.303571428571. Mean: 0.279705652809
# Mid 20th Percentile By Value:
#           0.4 to 0.6. Units: 1011

# High Twentieth Percentile By Unit:
#           0.303571428571 to 0.361842105263. Mean: 0.330808483022
# High 20th Percentile By Value:
#           0.600554785021 to 0.79792746114. Units: 84

# Top Twentieth Percentile By Unit:
#           0.361904761905 to 1.0. Mean: 0.480467968475
# High 20th Percentile By Value:
#           0.8 to 1.0. Units: 187

# Top 10th Percentile By Unit:
#           0.41717791411 to 1.0. Mean: 0.575023504628
# Top 10th Percentile By Value:
#           0.901639344262 to 1.0. Units: 168

# SL_RANGE:
# Standard Deviation: 11.2830870618
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 10th Percentile By Value:
#           0.0 to 26.0. Units: 10002

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Bottom 20th Percentile By Value:
#           27.0 to 53.0. Units: 221

# Low Twentieth Percentile By Unit:
#           0.0 to 0.0. Mean: 0.0
# Low 20th Percentile By Value:
#           54.0 to 106.0. Units: 59

# Mid Twentieth Percentile By Unit:
#           0.0 to 1.0. Mean: 0.666990291262
# Mid 20th Percentile By Value:
#           109.0 to 159.0. Units: 10

# High Twentieth Percentile By Unit:
#           1.0 to 5.0. Mean: 2.71941747573
# High 20th Percentile By Value:
#           161.0 to 193.0. Units: 5

# Top Twentieth Percentile By Unit:
#           5.0 to 268.0. Mean: 17.4759825328
# High 20th Percentile By Value:
#           237.0 to 268.0. Units: 4

# Top 10th Percentile By Unit:
#           12.0 to 268.0. Mean: 26.9873786408
# Top 10th Percentile By Value:
#           242.0 to 268.0. Units: 3

# SL_MEAN:
# Standard Deviation: 13.8385774607
# Bottom 10th Percentile By Unit:
#           0.203883495146 to 0.913580246914. Mean: 0.803827973593
# Bottom 10th Percentile By Value:
#           0.203883495146 to 38.3333333333. Units: 10021

# Bottom 20th Percentile By Unit:
#           0.203883495146 to 1.17857142857. Mean: 0.894149956226
# Bottom 20th Percentile By Value:
#           39.0 to 76.0. Units: 217

# Low Twentieth Percentile By Unit:
#           1.18309859155 to 3.83333333333. Mean: 2.61373460769
# Low 20th Percentile By Value:
#           79.0 to 152.0. Units: 51

# Mid Twentieth Percentile By Unit:
#           3.83333333333 to 6.0. Mean: 4.56802013927
# Mid 20th Percentile By Value:
#           155.0 to 210.0. Units: 9

# High Twentieth Percentile By Unit:
#           6.0 to 13.0. Mean: 8.6766051491
# High 20th Percentile By Value:
#           301.0 to 301.0. Units: 1

# Top Twentieth Percentile By Unit:
#           13.0 to 383.0. Mean: 26.583687574
# High 20th Percentile By Value:
#           347.0 to 383.0. Units: 2

# Top 10th Percentile By Unit:
#           20.6 to 383.0. Mean: 37.5495689723
# Top 10th Percentile By Value:
#           347.0 to 383.0. Units: 2

# THE_FREQ:
# Standard Deviation: 0.0335245014576
# Bottom 10th Percentile By Unit:
#           0.0 to 0.0242914979757. Mean: 0.0119386118017
# Bottom 10th Percentile By Value:
#           0.0 to 0.0499390986602. Units: 3449

# Bottom 20th Percentile By Unit:
#           0.0 to 0.0373831775701. Mean: 0.0216590788245
# Bottom 20th Percentile By Value:
#           0.05 to 0.0996884735202. Units: 5443

# Low Twentieth Percentile By Unit:
#           0.0373831775701 to 0.0550458715596. Mean: 0.0466818837165
# Low 20th Percentile By Value:
#           0.1 to 0.197530864198. Units: 1382

# Mid Twentieth Percentile By Unit:
#           0.0550847457627 to 0.0701754385965. Mean: 0.0623966737135
# Mid 20th Percentile By Value:
#           0.2 to 0.272727272727. Units: 26

# High Twentieth Percentile By Unit:
#           0.0701754385965 to 0.0900900900901. Mean: 0.0794111641408
# High 20th Percentile By Value:
#           0.3 to 0.4. Units: 0

# Top Twentieth Percentile By Unit:
#           0.0900900900901 to 0.5. Mean: 0.113657778619
# High 20th Percentile By Value:
#           0.5 to 0.5. Units: 1

# Top 10th Percentile By Unit:
#           0.106617647059 to 0.5. Mean: 0.129718479397
# Top 10th Percentile By Value:
#           0.5 to 0.5. Units: 1

# LL_RANGE:
# Standard Deviation: 73.9389386028
# Bottom 10th Percentile By Unit:
#           0.0 to 12.0. Mean: 7.91844660194
# Bottom 10th Percentile By Value:
#           0.0 to 189.0. Units: 10128

# Bottom 20th Percentile By Unit:
#           0.0 to 15.0. Mean: 10.8917475728
# Bottom 20th Percentile By Value:
#           191.0 to 375.0. Units: 104

# Low Twentieth Percentile By Unit:
#           15.0 to 22.0. Mean: 18.6053398058
# Low 20th Percentile By Value:
#           379.0 to 751.0. Units: 42

# Mid Twentieth Percentile By Unit:
#           22.0 to 31.0. Mean: 26.5538834951
# Mid 20th Percentile By Value:
#           772.0 to 1071.0. Units: 15

# High Twentieth Percentile By Unit:
#           31.0 to 45.0. Mean: 37.4966019417
# High 20th Percentile By Value:
#           1176.0 to 1460.0. Units: 8

# Top Twentieth Percentile By Unit:
#           45.0 to 1891.0. Mean: 98.7210092188
# High 20th Percentile By Value:
#           1578.0 to 1891.0. Units: 4

# Top 10th Percentile By Unit:
#           58.0 to 1891.0. Mean: 147.072815534
# Top 10th Percentile By Value:
#           1719.0 to 1891.0. Units: 2

# COMMON_PERCENT:
# Standard Deviation: 0.076110957576
# Bottom 10th Percentile By Unit:
#           0.140221402214 to 0.358974358974. Mean: 0.317759430571
# Bottom 10th Percentile By Value:
#           0.140221402214 to 0.214285714286. Units: 31

# Bottom 20th Percentile By Unit:
#           0.140221402214 to 0.388516746411. Mean: 0.346594110853
# Bottom 20th Percentile By Value:
#           0.217391304348 to 0.289473684211. Units: 176

# Low Twentieth Percentile By Unit:
#           0.388535031847 to 0.428571428571. Mean: 0.409181444301
# Low 20th Percentile By Value:
#           0.289855072464 to 0.43908045977. Units: 4599

# Mid Twentieth Percentile By Unit:
#           0.428571428571 to 0.462962962963. Mean: 0.445083911455
# Mid 20th Percentile By Value:
#           0.439093484419 to 0.588235294118. Units: 5137

# High Twentieth Percentile By Unit:
#           0.462962962963 to 0.505154639175. Mean: 0.482373021098
# High 20th Percentile By Value:
#           0.588709677419 to 0.734375. Units: 331

# Top Twentieth Percentile By Unit:
#           0.505154639175 to 0.887372013652. Mean: 0.554560460105
# High 20th Percentile By Value:
#           0.738007380074 to 0.887372013652. Units: 27

# Top 10th Percentile By Unit:
#           0.5390625 to 0.887372013652. Mean: 0.58855798336
# Top 10th Percentile By Value:
#           0.821350762527 to 0.887372013652. Units: 7



if __name__ == "__main__" or __name__ == "__console__":

    connect_to_db(app)
    print "Connected to DB."
