import os
import json
#mdir="./Output5/JDIQ"
#dir=os.listdir(mdir)
#volume_dict={}
#issue_dict={}
#for sub in dir:
def get_volume_dict(sub,volume_dict,mdir):
	issue_dict={}
	Volume=sub.split(" ")
	if not volume_dict.has_key(str(Volume[0]+Volume[1])):
		volume_dict[str(Volume[0]+Volume[1])]={}
	aritcles=os.listdir(mdir+"/"+sub)
	output={}
	for article in aritcles:
		fs=open((mdir+'/'+sub+'/'+article+'/citations.txt'),"r")
		citations=fs.readlines()
		fs.close()
		fs=open((mdir+'/'+sub+'/'+article+'/references.txt'),"r")
		references=fs.readlines()
		fs.close()
		fs=open((mdir+'/'+sub+'/'+article+'/title.txt'),"r")
		title=fs.read()
		fs.close()
		fs=open((mdir+'/'+sub+'/'+article+'/doi.txt'),"r")
		doi=fs.read()
		fs.close()
		fs=open((mdir+'/'+sub+'/'+article+"/authors.txt"),"r")
		authors=fs.readlines()#strip("\n")
		author_names = [author.split(" ")[0] for author in authors]
		links = [author.split(" ")[1] for author in authors]
		links = [('http://dl.acm.org/'+link.split("&")[0]) for link in links]
		author_names = [name.replace('_',' ') for name in author_names]
		fs.close()
		fs = open((mdir+'/'+sub+'/'+article+"/stats.txt"),"r")
		stats = fs.readlines()
		if len(stats) == 0:
			stats = [0,0,0,0]
		stat = {}
		stat['Downloads (6 weeks) '] = stats[0]
		stat['Downloads (12 months)'] = stats[1]
		stat['Downloads (cumulative)'] = stats[2]
		stat['Citation Count'] = stats[3]
		fs.close()
		fs=open((mdir+'/'+sub+'/'+article+"/abstract.txt"),"r")
		abstract=(fs.read()).strip("\n")
		fs.close() 
		output[str(article)] = {"title" : title, "authors" : [{'link':link,'name':name} for link,name in zip(links,author_names)] , "Metrics": stat, "abstract" : abstract , "doi":doi , "references":references , "citations" : citations}
	if len(Volume)<6:
		Volume.append(Volume[4])
		Volume[4] = 0
	issue_dict[str(Volume[2]+Volume[3].strip(','))] = {"issn":" ","date":{"month":Volume[4], "year":Volume[5]}, "articles":output}
	volume_dict[str(Volume[0]+Volume[1])].update(issue_dict)
	return volume_dict
#mdir="./Output5/JDIQ"
Jdir = "../data/Journal_data"
jlist = os.listdir(Jdir)
jdic = {}
for Journal in jlist:
	vdir  = Jdir + '/' + Journal + '/' + 'Volumes'
	idir = os.listdir(vdir)
	volume_dict = {}
	for sub in idir:
		volume_dict = get_volume_dict(sub,volume_dict,vdir)
	jdic[Journal] = {"Volumes":volume_dict, "ISSN":""}
final_dict = {'ACM':jdic}
with open("../output/Journal_data.json",'w') as outfile:
	json.dump(final_dict,outfile)
# dir=os.listdir(mdir)
# volume_dict = {}
# for  sub in dir:
# 	volume_dict=get_volume_dict(sub,volume_dict)
# output_dict2= volume_dict
# mdir="./Output5/CSUR"
# dir=os.listdir(mdir)
# volume_dict = {}
# for  sub in dir:
# 	volume_dict=get_volume_dict(sub,volume_dict)	
# output_dict1 = volume_dict
#final_dict = {'ACM' : {'CSUR' : output_dict1, 'JDIQ' : output_dict2}}
# with open('V1I13.json','w') as outfile:
#     json.dump(final_dict,outfile)