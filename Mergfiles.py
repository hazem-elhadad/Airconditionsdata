import pandas as pd
def mergingfiles():
    df1 = pd.read_excel('swsg_excel_data.xlsx')
    df2 = pd.read_excel('xcite_excel_data.xlsx')
    df3=df1.merge(df2, how='outer')
    df4=pd.read_excel('almanea_excel_data.xlsx')
    df5=df3.merge(df4, how='outer')
    df6=pd.read_excel('alkhunaizan_excel_data.xlsx')
    df7=df5.merge(df6, how='outer')
    df8=pd.read_excel('blackbox_excel_data.xlsx')
    df9= df7.merge(df8, how='outer')
    df9.to_excel('AllMergeddata.xlsx' , index = False)

#mergingfiles()