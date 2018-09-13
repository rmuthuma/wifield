import httplib2
import webapp2
from google.appengine.ext.webapp import template
from apiclient.discovery import build
from oauth2client.appengine import AppAssertionCredentials
import json

url = 'https://www.googleapis.com/auth/bigquery'
PROJECT_NUMBER = 'wifield-210400'

credentials = AppAssertionCredentials(scope=url)
httpss = credentials.authorize(httplib2.Http())
bigquery_service = build('bigquery','v2',http=httpss)

class ShowChartPage(webapp2.RequestHandler):
    def get(self):
	temp_data = {}
	temp_path = 'Templates/chart.html'
	queryData = {'query':'SELECT macaddress FROM [publicdata:wifield_bigquery.wifield_data] LIMIT 1000'}
	tableData = bigquery_service.jobs()
	response = tableData.query(projectId=PROJECT_NUMBER,body=queryData).execute()
	self.response.out.write(response)
	#jself.response.out.write(template.render(temp_path,temp_data))

class ShowHome(webapp2.RequestHandler):
    def get(self):
        template_data = {}
        template_path = 'Templates/index.html'
        self.response.out.write(template.render(template_path,template_data))

class getChartData(webapp2.RequestHandler):
    def get(self):
        inputData = self.request.get("inputData")
        queryData = {'query':'SELECT SUM(temps000, temps001, temps002, temps003, temps004, temps005, temps006, temps007, temps008, temps009, temps010, temps011) as WCount, vin as corpus_date,Rainmm as Work FROM '
        '[publicdata:wifield_bigquery.wifield_data] WHERE macaddress="0c2a6908a5a3"'}
        tableData = bigquery_service.jobs()
        dataList = tableData.query(projectId=PROJECT_NUMBER,body=queryData).execute()

    resp = []
    if 'rows' in dataList:
      for row in dataList['rows']:
        for key,dict_list in row.iteritems():
          count = dict_list[0]
          year = dict_list[1]
          corpus = dict_list[2]
          resp.append({'count': count['v'],'year':year['v'],'corpus':corpus['v']})
    else:
      resp.append({'count':'0','year':'0','corpus':'0'})


    self.response.headers['Content-Type'] = 'application/json'
    self.response.out.write(json.dumps(resp))

class DisplayChart(webapp2.RequestHandler):
    def get(self):
        template_data = {}
        template_path = 'Templates/displayChart.html'
        self.response.out.write(template.render(template_path,template_data))


class DisplayChart3(webapp2.RequestHandler):
    def get(self):
        template_data = {}
        template_path = 'Templates/displayChart_3.html'
        self.response.out.write(template.render(template_path,template_data))

class DisplayChart4(webapp2.RequestHandler):
    def get(self):
        template_data = {}
        template_path = 'Templates/displayChart_4.html'
        self.response.out.write(template.render(template_path,template_data))

application = webapp2.WSGIApplication([
    ('/chart',ShowChartPage),
    ('/displayChart',DisplayChart),
    ('/displayChart3',DisplayChart3),
    ('/displayChart4',DisplayChart4),
    ('/getChartData',GetChartData),
    ('/', ShowHome),
], debug=True)
