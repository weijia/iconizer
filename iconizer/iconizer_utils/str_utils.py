

def decode_str(read_data):
    try:
        read_data = read_data.decode("gbk")
    except:
        try:
            read_data = read_data.decode("utf8")
        except:
            pass
            # print 'after readline'
    return read_data
