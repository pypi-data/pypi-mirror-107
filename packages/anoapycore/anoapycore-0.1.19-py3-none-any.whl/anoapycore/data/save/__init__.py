import pandas as __pd


def csv (a_data,a_file,b_separator='~',b_index=False) :
    a_data.to_csv(a_file,sep=b_separator,index=b_index)

def xls (a_data,a_filename) :
    # create excel writer object
    loc_writer = __pd.ExcelWriter(a_filename)
    # write dataframe to excel
    a_data.to_excel(loc_writer)
    # save the excel
    loc_writer.save()
