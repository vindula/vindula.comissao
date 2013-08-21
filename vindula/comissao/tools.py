# coding: utf-8

from decimal import Decimal, InvalidOperation
from datetime import date


def convert_csv2list_dict(rows_csv):
    #PARTE GENERICA QUE RETORNA LISTA DE DICTS
    columns = rows_csv[:1]
    rows = rows_csv[1:]
    data = []

    if columns:
        columns = columns[0].replace('\n','').split(';')

    for row in rows:
        row_dict = {}
        for number, column in enumerate(columns):
            row_fields = row.replace('\n','').split(';')
            row_dict[column] = row_fields[number]

        data.append(row_dict)
    
    return data


def convert_str2int(str):
	if str:
		try:
			return int(str)
		except ValueError:
			return 0
	return 0



def convert_str2decimal(str):
	if str:
		str = str.replace('.','')
		str = str.replace(',','.')
		try:
			return Decimal(str)
		except InvalidOperation:
			return Decimal(0.0)
	return Decimal(0.0)

def convert_str2unicode(str):
	if str:
		try:
			return unicode(str)
		except:
			return u''
	return u''


def convert_str2date(str):
	if str:
		split_date = str.split('/')
		try:
			return date(int(split_date[2]),
						int(split_date[1]),
						int(split_date[0]))
		except ValueError:
			return date.today()
	
	return date.today()