import statistics as Statistics

def iqr(data_list: list = [0]):
    if(len(data_list) == 0):
        return None

    data_list.sort()

    if(len(data_list) % 2 == 1):
        data = data_list[:Statistics.median(data_list)-1] + data_list[Statistics.median(data_list):]

    lower_bound = Statistics.median_low(data)-1
    higher_bound = Statistics.median_high(data)

    return data_list[lower_bound:higher_bound]

# @todo
# [1,2,3,4,5,6], 2
def quantile_indices(data_list, tiles):
    if(len(list) == 0):
        return data_list
    elif(tiles <= 0):
        raise ValueError(tiles)
    
    data_list = data_list.sort()
    
    tiles = int(tiles)

    indices = tiles + 1





    












