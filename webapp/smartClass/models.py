#encoding=utf-8
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import datetime
import time
import json
# Create your models here.
from django.db.models.fields.files import FieldFile
#自定义用户类，增加了utype和头像
class MyUser(AbstractUser):
	utype = models.CharField(max_length=30)#用户类型，可为student or teacher
	avatar = models.ImageField(upload_to='images',max_length=1000)
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			elif attr=='password':
				print 'password attr exclude'
				continue
			else:
				d[attr] = getattr(self, attr)
		return d

#未使用
class Student(models.Model):
	stud_id = models.IntegerField()
	name = models.CharField(max_length=30)
	password = models.CharField(max_length=20)
	def __unicode__(self):
		return self.name
#未使用
class Teacher(models.Model):
	teach_id = models.IntegerField()
	name = models.CharField(max_length=30)
	password=models.CharField(max_length=20)
	def __unicode__(self):
		return self.name
#课程类
class Course(models.Model):
	course_id = models.IntegerField(default=1401)#课程id
	name = models.CharField(max_length=30,unique=True)#课程名
	teacher = models.IntegerField()#教师id
	number_student = models.IntegerField(default=0)#加入课程的学生数目
	number_project = models.IntegerField(default=0)#课程项目数
	number_test = models.IntegerField(default=0)#课程测试数
	status = models.IntegerField(default=-1)#课程状态0开始1结束
	description = models.CharField(max_length=1000,default="欢迎加入本课程")
	term = models.CharField(max_length=20,default="PKU Spring 2015")
	notificationNumber = models.IntegerField(default=0)
	mainDate = models.CharField(max_length=100,default="")
	def __unicode__(self):
		return self.name
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d

	def toJSON(self):
		fields = []
		for field in self._meta.fields:
			fields.append(field.name)
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return json.dumps(d)

#学生、课程关联表
class stud_course_entry(models.Model):
	course = models.IntegerField()#课程id
	student = models.IntegerField()#学生id

class Student_Course_Rela(models.Model):
	"""docstring for Student_Course_Rela"""
	courseId = models.IntegerField(default=-1)
	studentId = models.IntegerField(default=-1)
	def __init__(self, arg):
		super(Student_Course_Rela, self).__init__()
		self.arg = arg
		
#未使用
class Group(models.Model):
	group_id = models.IntegerField()
	group_name = models.CharField(max_length=30)
	group_student = models.IntegerField()
	group_course = models.IntegerField()

#签到表，未使用
class Sign(models.Model):
	student = models.IntegerField()
	course = models.IntegerField()
	time = models.DateTimeField(auto_now_add=True)

#答案表，未使用
class Answer(models.Model):
	ans_id = models.IntegerField()
	ans_student_id = models.IntegerField()
	ans_question_id = models.IntegerField()
	ans_course_id = models.IntegerField()
	ans_test_id = models.IntegerField()
	ans_text = models.CharField(max_length=100)

#提问表，未使用
class Question(models.Model):
	qst_id = models.IntegerField()
	qst_code = models.IntegerField()
	qst_content = models.CharField(max_length=100)
	qst_student = models.IntegerField()
	qst_course = models.IntegerField()

#测试表
class Test(models.Model):
	id = models.AutoField(primary_key=True)#测试id
	tid = models.IntegerField(default=1)#未使用
	name = models.CharField(max_length=30)#测试名
	question_number= models.IntegerField(default=1)#测试问题数目
	course = models.IntegerField(default=-1)#测试所在课程
	status = models.IntegerField(default=-1)#测试状态  0未添加答案 1未添加题目 
						 #2未开始 3未结束 4已结束
	files = models.FileField(upload_to='static/files/test/')#题目文件
	file_url = models.CharField(max_length=100)#题目文件url
	number_student = models.IntegerField(default=0)
	btime = models.DateTimeField(default=datetime.datetime.now)
	etime = models.DateTimeField(default=datetime.datetime.now)
	ctime = models.DateTimeField(default=datetime.datetime.now)
	mtime = models.DateTimeField(default=datetime.datetime.now)
	def __unicode__(self):
	   return self.name
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			# if isinstance(getattr(self, attr),datetime.datetime):
			# 	d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
			# elif isinstance(getattr(self, attr),datetime.date):
			# 	d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =str(time.mktime( getattr(self,attr).timetuple()))
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = str(time.mktime( getattr(self,attr).timetuple()))
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d

	def toJSON(self):
		fields = []
		for field in self._meta.fields:
			fields.append(field.name)
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =str(time.mktime( getattr(self,attr).timetuple()))
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = str(time.mktime( getattr(self,attr).timetuple()))
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d

#课程项目表
class Project(models.Model):
	pid = models.IntegerField(default=0)#未使用的id
	name = models.CharField(max_length=30)#项目名
	course = models.IntegerField()#所在课程id
	group_number = models.IntegerField(default=0)#所分组数
	is_grouped = models.BooleanField(default=False)#是否分组 0 未分组 1已分组
	status = models.IntegerField(default=-1)#状态 0未添加题目 1未开始分组 2分组已开始 3分组借宿
	files = models.FileField(upload_to='static/files/project')#项目上传文件
	file_url = models.CharField(max_length=30)#文件url
	number_student = models.IntegerField(default=0)#已提交组队信息的学生名单
	btime = models.DateTimeField(default=datetime.datetime.now)
	etime = models.DateTimeField(default=datetime.datetime.now)
	ctime = models.DateTimeField(default=datetime.datetime.now)
	mtime = models.DateTimeField(default=datetime.datetime.now)
	def __unicode__(self):
	   return self.name
	# def toJson(self):
	#     import json
	#     return json.dumps(dict([(attr,getattr(self,attr)) for attr in [f.name for f in self._meta.fields]]))
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =str(time.mktime( getattr(self,attr).timetuple()))
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = str(time.mktime( getattr(self,attr).timetuple()))
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d
		#return dict([(attr,getattr(self,attr)) for attr in [f.name for f in self._meta.fields]])
	def toJSON(self):
		fields = []
		for field in self._meta.fields:
			fields.append(field.name)
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self, attr),datetime.datetime):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
			elif isinstance(getattr(self, attr),datetime.date):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return json.dumps(d)

	def printself(self):
		fields = []
		for field in self._meta.fields:
			fields.append(field.name)
		d = {}
		for attr in fields:
			if isinstance(getattr(self,attr),FieldFile):
				print 'here at files\n'
			print attr,',---,',getattr(self,attr),' ,',type(getattr(self,attr))


		

#项目的所有题目表
class Project_Question(models.Model):
	qid = models.IntegerField(default=-1)
	pid = models.IntegerField(default=-1)
	name=models.CharField(max_length=30)
	max_group=models.IntegerField(default=-1)
	number_per_group=models.IntegerField(default=-1)
	files = models.FileField(upload_to = 'static/files/project')
	file_url = models.CharField(max_length=30)
	first_number = models.IntegerField(default=0)
	second_number = models.IntegerField(default=0)
	third_number = models.IntegerField(default=0)
	def  toDict(self):
		d = {} 
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self, attr),datetime.datetime):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
			elif isinstance(getattr(self, attr),datetime.date):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d

	def toJSON(self):
		fields = []
		for field in self._meta.fields:
			fields.append(field.name)
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self, attr),datetime.datetime):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
			elif isinstance(getattr(self, attr),datetime.date):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return json.dumps(d)  
	# qid = models.IntegerField(default=-1)#未使用的题目id
	# pid = models.IntegerField(default=-1)#项目id
	# name=models.CharField(max_length=30)#题目名称
	# max_group=models.IntegerField(default=-1)#最大组数
	# number_per_group=models.IntegerField(default=-1)#每组人数
	# files = models.FileField(upload_to = 'static/files/project')#文件
	# file_url = models.CharField(max_length=30)
	# first_number = models.IntegerField(default=0)#已该题目为第一志愿的人数
	# second_number = models.IntegerField(default=0)#第二志愿人数
	# third_number = models.IntegerField(default=0)


#测试答案表
class Test_Answer(models.Model):
	tid = models.IntegerField(default = -1)#测试id
	aid = models.IntegerField(default = -1)#答案编号
	answer = models.CharField(max_length=20)#答案
	accuracy = models.DecimalField(max_digits=5,decimal_places=2,default = 0)#正确率

#学生测试表，记录学生提交的测试信息
class Student_Test(models.Model):
	tid = models.IntegerField(default=-1)#测试id
	sid = models.IntegerField(default=-1)#学生id
	accuracy = models.DecimalField(max_digits=5, decimal_places=2,default=0)#正确率

#学生测试答案，记录学生提交的答案
class Student_Test_Answer(models.Model):
	tid = models.IntegerField(default=-1)#测试id
	sid = models.IntegerField(default=-1)#学生id
	aid = models.IntegerField(default=-1)#答案的题目编号
	answer = models.CharField(max_length=10)#答案
	outcome = models.IntegerField(default=0)#结果 0错误 1正确

#分组信息表，记录学生提交的分组选题信息
class Groupinfo_Question(models.Model):
	pid = models.IntegerField(default=0)#项目id
	sid = models.IntegerField(default=0)#学生id
	qid = models.IntegerField(default=0)#题目id
	qname=models.CharField(max_length=30)#题目名称
	priority=models.IntegerField(default=-1)#优先级 1一志愿 2二志愿 3三志愿
	priority_bak = models.IntegerField(default=-1)#优先级备份

#分组信息，记录学生所选的搭档
class Groupinfo_Partner(models.Model):
	pid = models.IntegerField(default=0)#项目id
	sid = models.IntegerField(default=0)#学生id
	partner = models.IntegerField(default=0)#所选的同伴id

#分组结果记录表
class Group_Outcome(models.Model):
	pid = models.IntegerField(default=0)#项目id
	gid = models.IntegerField(default=0)#组编号
	qid = models.IntegerField(default=0)#问题id
	qname = models.CharField(max_length=30)#问题名称
	sid = models.IntegerField(default=0)#学生id


#分组结果，分组与所选题目表
class Group_Question_Outcome(models.Model):
	pid = models.IntegerField(default=0)#项目id
	gid = models.IntegerField(default=0)#组编号
	qid = models.IntegerField(default=0)#题目id
	qname = models.CharField(max_length=30)#题目名称


#分组结果，学生与所在组关联表
class Group_Student_Outcome(models.Model):
	sid = models.IntegerField(default=0)#学生id
	gid = models.IntegerField(default=0)#组编号
	pid = models.IntegerField(default=0)#项目id
	sname = models.CharField(max_length=30)#学生名称


#测试题目表
class Test_Question(models.Model):
	"""docstring for Test_Question"""
	testId = models.IntegerField(default=-1)
	questionId = models.IntegerField(default=-1)
	content = models.CharField(max_length=100)
	answer = models.CharField(max_length=10)
	choice = models.CharField(max_length=100)
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self, attr),datetime.datetime):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
			elif isinstance(getattr(self, attr),datetime.date):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d

	def toJSON(self):
		fields = []
		for field in self._meta.fields:
			fields.append(field.name)
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self, attr),datetime.datetime):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d %H:%M:%S')
			elif isinstance(getattr(self, attr),datetime.date):
				d[attr] = getattr(self, attr).strftime('%Y-%m-%d')
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return json.dumps(d)
		
class Project_Group(models.Model):
	"""docstring for Project_Group"""
	projectId = models.IntegerField(default = 0)
	groupId = models.IntegerField(default = 0)
	chosenQuestionId = models.IntegerField(default = 0)
	status = models.IntegerField(default = 0)
	leader = models.CharField(max_length = 30)
	member = models.CharField(max_length = 100)
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d


class ProjectQuestion(models.Model):
	projectId = models.IntegerField(default = 0)
	questionId = models.IntegerField(default = 0)
	maxGroup = models.IntegerField(default = 0)
	numberPerGroup = models.IntegerField(default = 0)
	fileUrl = models.CharField(max_length = 100)
	describe = models.CharField(max_length=100)
	name = models.CharField(max_length = 100)
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d

class Student_TestQuestion_Answer(models.Model):
	testId = models.IntegerField(default = 0)
	testQuestionId = models.IntegerField(default = 0)
	studentId = models.IntegerField(default = 0)
	studentAnswer = models.CharField(max_length=20)
	correct = models.IntegerField(default = 0)
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d
class Student_Sign(models.Model):
	studentId = models.IntegerField(default = 0)
	signId = models.IntegerField(default = 0)
	signDate = models.DateTimeField(default=datetime.datetime.now)
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d

class Course_Sign(models.Model):
	courseId = models.IntegerField(default=0)
	teacherId = models.IntegerField(default = 0)
	btime = models.DateTimeField(default = datetime.datetime.now)
	etime = models.DateTimeField(default = datetime.datetime.now)
	signNumber = models.IntegerField(default = 0)
	def  toDict(self):
		d = {}
		for field in self._meta.fields:
			attr = field.name
			if isinstance(getattr(self,attr),datetime.datetime):
				d[attr] =time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),datetime.date):
				d[attr] = time.mktime( getattr(self,attr).timetuple())
			elif isinstance(getattr(self,attr),FieldFile):
				d[attr] = None
				continue
			else:
				d[attr] = getattr(self, attr)
		return d
