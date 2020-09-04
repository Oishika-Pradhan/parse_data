from django.shortcuts import render
import openpyxl
import pandas as pd
from os import path
import xlwt
from django.http import HttpResponse
from io import BytesIO as IO
#from .forms import NameForm
#from pandas_djmodel import get_model_repr

df = pd.DataFrame()

def index(request):
	if "GET" == request.method:
		return render(request, 'myapp/index.html', {})
	else:
		excel_file = request.FILES["excel_file"]

		# you may put validations here to check extension or file size

		wb = openpyxl.load_workbook(excel_file)
		df=pd.read_excel(excel_file)
		df['Accepted Compound ID'].fillna("No value", inplace=True)
		df.to_pickle("./dummy.pkl")
		worksheet = wb["Raw Data"]
		#print(worksheet)

		# getting active sheet
		active_sheet = wb.active

		excel_data = list()
		# iterating over the rows and
		# getting value from each cell in row
		# for row in worksheet.iter_rows():
		# 	row_data = list()
		# 	for cell in row:
		# 		row_data.append(str(cell.value))
		# 		#print(cell.value)
		# 	excel_data.append(row_data)

		return render(request, 'myapp/index.html', {})


def compound(request):
	if path.exists('./dummy.pkl'):
		df1=pd.read_pickle('./dummy.pkl')
		plasma=df1[df1['Accepted Compound ID'].str.endswith('plasmalogen')]
		lpc=df1[df1['Accepted Compound ID'].str.endswith('LPC')]
		pc_temp=df1[df1['Accepted Compound ID'].str.endswith('PC')]
		pc=pc_temp[pc_temp['Accepted Compound ID'].str.endswith('LPC')==False]
		plasma.to_pickle('./plasma.pkl')
		lpc.to_pickle('./lpc.pkl')
		pc.to_pickle('./pc.pkl')
		return render(request, 'myapp/compound.html', {})
	
	else:
		return render(request, 'myapp/no_access.html', {})

def retention(request):
	if path.exists('./dummy.pkl'):
		df2=pd.read_pickle('./dummy.pkl')
		time=round(df2['Retention time (min)'])
		df2['Retention Time Roundoff (in mins)']=time
		df2.to_pickle('./ret.pkl')
		return render(request, 'myapp/retention.html', {})
	else:
		return render(request, 'myapp/no_access.html', {})
		

def mean(request):
	if path.exists('./dummy.pkl'):
		df3=pd.read_pickle('./dummy.pkl')
		time=round(df3['Retention time (min)'])
		df3['Retention Time Roundoff (in mins)']=time
		df3.sort_values(by=['Retention Time Roundoff (in mins)'], inplace=True)
		#ans=df3[~df3['Retention Time Roundoff (in mins)'] and ~df3['m/z'] and ~df3['Accepted Compound ID'] and ~df3['Retention time (min)']]
		ans=df3.drop(columns=['Retention Time Roundoff (in mins)', 'm/z', 'Accepted Compound ID', 'Retention time (min)'])
		df3['Mean']=ans.mean(axis = 1, skipna = True)
		final_ans=df3[['Mean', 'Retention Time Roundoff (in mins)']]
		final_ans.to_pickle('./mean.pkl')
		return render(request, 'myapp/mean.html', {})
		# g=df3.groupby('Retention Time Roundoff (in mins)')
		# for name, group in g:
		# 	print(group[0])
	else:
		return render(request, 'myapp/no_access.html', {})

def downloadexcel(request):
	if request.method=='POST':
		if 'retention' == request.POST.get('download'):
			df_output=pd.read_pickle('./ret.pkl')
			f='retention.xlsx'
		elif 'pc' == request.POST.get('download'):
			f='PC_Dataset.xlsx'
			df_output=pd.read_pickle('./pc.pkl')
		elif 'lpc' == request.POST.get('download'):
			f='LPC_Dataset.xlsx'
			df_output=pd.read_pickle('./lpc.pkl')
		elif 'plas' == request.POST.get('download'):
			f='Plasmalogen_Dataset.xlsx'
			df_output=pd.read_pickle('./plasma.pkl')
		elif 'mean' == request.POST.get('download'):
			f='Mean_Statistics.xlsx'
			df_output=pd.read_pickle('./mean.pkl')
		else:
			return render(request, 'myapp/no_access.html', {})

# my "Excel" file, which is an in-memory output file (buffer) 
# for the new workbook
	excel_file = IO()

	xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')

	df_output.to_excel(xlwriter, 'sheetname')

	xlwriter.save()
	xlwriter.close()

# Otherwise gives error if the excel file is empty
	excel_file.seek(0)

# set the mime type so that the browser knows what to do with the file
	response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Content-Disposition header to send file name
	response['Content-Disposition'] = f'attachment; filename={f}'

	return response