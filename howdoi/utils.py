import heapq


def get_top_n_key_val_pairs_from_dict(dict_, N):
    top_n_key_value_pairs = []
    if isinstance(dict_, dict):
        for key in dict_:
            heapq.heappush(top_n_key_value_pairs, (dict_[key], key))
            if len(top_n_key_value_pairs) > N:
                heapq.heappop(top_n_key_value_pairs)

    top_n_key_value_pairs.sort(reverse=True)
    return [(k, v) for v, k in top_n_key_value_pairs]


def safe_divide(numerator, denominator):
    return numerator/denominator if denominator != 0 else 0
