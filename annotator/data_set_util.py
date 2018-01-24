RADIO_TRAIN = 8
RADIO_TEST = 1
RADIO_DEV = 1
SUM_RADIO = RADIO_TRAIN + RADIO_TEST + RADIO_DEV
RADIO_DATA_SET = [RADIO_TRAIN, RADIO_TRAIN + RADIO_TEST, SUM_RADIO]


def get_data_set_group(index):
    t = index % SUM_RADIO
    for i in range(0, 3):
        if t < RADIO_DATA_SET[i]:
            return i
    return 0


