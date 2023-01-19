import pandas as pd
import numpy as np

if __name__ == '__main__':
    #WCZYANIE DANYCH Z PLIKU CSV I UTWORZENIE TABELI DO OBLICZEŃ:
    dane = pd.read_csv('ALL_COMBINE.csv', delimiter=",")
    tabela_start = pd.DataFrame(dane)
    tabela_start['OVR'] = (tabela_start['ST_OVR_22'] + tabela_start['MID_OVR_22'] + tabela_start['DEF_OVR_22']) / 3

    # SPRAWDZENIE, CZA TABELA NIE ZAWIERA BŁĘDÓW/PUSTYCH KOMÓREK:
    print('sprawdzenie czy tabela zaiwera puse komórki? \n', tabela_start.isna().any())
    print('-------------------------------------------------------------------')
    #UZUPEŁNIENIE BRAKUJĄCYCH KOMÓREK W TABELI Z DANYMI WEJŚCIOWYMI:
    tabela_start.replace(to_replace=np.nan, value=tabela_start['OVR'].min(), inplace=True)

    tabela_start.replace(to_replace='_', value=np.nan, inplace=True)
    GZ_AVG = (tabela_start['GZ_21'].astype(float) + tabela_start['GZ_20'].astype(float) + tabela_start['GZ_19'].astype(float)) / 3
    tabela_start.fillna(value=GZ_AVG.mean(), inplace = True)

    tabela_start.replace(to_replace='-', value=np.nan, inplace=True)
    GS_AVG = (tabela_start['GS_21'].astype(float) + tabela_start['GS_20'].astype(float) + tabela_start['GS_19'].astype(float)) / 3
    tabela_start.fillna(value=GS_AVG.mean(), inplace = True)

    tabela_start.replace(to_replace='*', value=np.nan, inplace=True)
    PKT_AVG = (tabela_start['PKT_21'].astype(float) + tabela_start['PKT_20'].astype(float) + tabela_start['PKT_19'].astype(float)) / 3
    tabela_start.fillna(value=PKT_AVG.min(), inplace=True)
    print('uaktualniona tabela z wszystkim danymi, uzupełniono pste komórki: \n', tabela_start)
    print('-------------------------------------------------------------------')

    print('sprawdzenie czy tabela nadal zaiwera puse komórki? \n', tabela_start.isna().any())
    print('-------------------------------------------------------------------')

    #AKTUALIZACJA ŚREDNICH WARTOŚCI GOLI I PUNKTÓW:
    GZ_AVG = (3*tabela_start['GZ_21'].astype(float) + 2*tabela_start['GZ_20'].astype(float) + tabela_start['GZ_19'].astype(float)) / 6
    GS_AVG = (3*tabela_start['GS_21'].astype(float) + 2*tabela_start['GS_20'].astype(float) + tabela_start['GS_19'].astype(float)) / 6
    PKT_AVG = (3*tabela_start['PKT_21'].astype(float) +2* tabela_start['PKT_20'].astype(float) + tabela_start['PKT_19'].astype(float)) / 6

    #TWORZENIE NOWEJ TABELI NA PODSTAWIE PODSTAWOWYCH DANYCH Z OBECNEGO SEZONU:
    nowa_tabela = pd.DataFrame(dane['CLUB'])
    nowa_tabela['ST_OVR'] = dane['ST_OVR_22'].astype(float)
    nowa_tabela['MID_OVR'] = dane['MID_OVR_22'].astype(float)
    nowa_tabela['DEF_OVR'] = dane['DEF_OVR_22'].astype(float)
    nowa_tabela['OVR'] = (nowa_tabela['ST_OVR'] + nowa_tabela['MID_OVR'] + nowa_tabela['DEF_OVR']) / 3

    #OBLICZENIE DANYCH POTRZEBNYCH DO PREDYKCJI FORMY ZESPOŁÓW W OBECNYM SEZONIE:
    nowa_tabela['ST_OVR_AVG'] = (tabela_start['ST_OVR_21'].astype(float) + tabela_start['ST_OVR_20'].astype(float) + tabela_start['ST_OVR_19'].astype(float)) / 3
    nowa_tabela['MID_OVR_AVG'] = (tabela_start['MID_OVR_21'].astype(float) + tabela_start['MID_OVR_20'].astype(float) + tabela_start['MID_OVR_19'].astype(float)) / 3
    nowa_tabela['DEF_OVR_AVG'] = (tabela_start['DEF_OVR_21'].astype(float) + tabela_start['DEF_OVR_20'].astype(float) + tabela_start['DEF_OVR_19'].astype(float)) / 3
    nowa_tabela['OVR_AVG'] = (nowa_tabela['ST_OVR_AVG'] + nowa_tabela['MID_OVR_AVG'] + nowa_tabela['DEF_OVR_AVG']) / 3

    #WSPÓŁCZYNNIK PRZYROSTU FORMY ZESPOŁÓW:
    nowa_tabela['POWER'] = nowa_tabela['OVR'] / nowa_tabela['OVR_AVG']
    nowa_tabela['ST_POWER'] = nowa_tabela['ST_OVR'] / nowa_tabela['ST_OVR_AVG']
    nowa_tabela['DEF_POWER'] = nowa_tabela['DEF_OVR'] / nowa_tabela['DEF_OVR_AVG']
    print('widok tabeli pomocniczej z danymi używanymi podczas obliczeń: \n' ,nowa_tabela)
    print('-------------------------------------------------------------------')
    print('sprawdzenie czy tabela zaiwera puse komórki? \n', nowa_tabela.isna().any())
    print('-------------------------------------------------------------------')

    #SZACOWANIE WYNIKÓW W NOWYM SEZONIE:
    koncowa_tabela = pd.DataFrame(dane['CLUB'])
    koncowa_tabela['GZ'] = round(nowa_tabela['ST_POWER'] * GZ_AVG)
    koncowa_tabela['GC'] = round(nowa_tabela['DEF_POWER'] * GS_AVG)
    koncowa_tabela['BG'] = koncowa_tabela['GZ'] - koncowa_tabela['GC']
    koncowa_tabela['PKT'] = round(nowa_tabela['POWER'] * PKT_AVG)
    koncowa_tabela = koncowa_tabela.sort_values(['PKT', 'BG', 'GZ'], ascending=False)
    print('przewidywana tabela na zakończenie sezonu: \n', koncowa_tabela)
    print('-------------------------------------------------------------------')