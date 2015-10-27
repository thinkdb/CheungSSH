import sys
def get_linen_umber_function_name():
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    return (f.f_code.co_name, f.f_lineno)
if __name__ == '__main__':
	print get_linen_umber_function_name()
