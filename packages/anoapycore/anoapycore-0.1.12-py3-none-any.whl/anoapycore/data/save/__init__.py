import pandas as __pd

def xls (a_data,a_filename) :
    # create excel writer object
    loc_writer = __pd.ExcelWriter(a_filename)
    # write dataframe to excel
    a_data.to_excel(loc_writer)
    # save the excel
    loc_writer.save()
