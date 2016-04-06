import json
import sys
import traceback

class jsonObject:
	
	class_define_array = []
	
	class_array = []
	
	file_name = ''

	root_class = ''
	
	new_line 	 = "\n\n"
	
	protocol	 = "@protocol "
	
	end 		 = "@end "
	
	interface    = "@interface "
	
	implementation = "@implementation "
	
	object_prefix = "@property (nonatomic, strong) "
	
	primitive_prefix = "@property (nonatomic, assign) "
	 
	number_prefix =  " NSNumber <Optional> "
	
	number = " NSNumber "
	
	integer_prefix =  " NSInteger <Optional> "
	
	bool_prefix =  " BOOL <Optional> "
	
	float_prefix =  " float <Optional> "
	
	long_prefix =  " long <Optional> "
	
	string_prefix = " NSString <Optional> "
	
	string = " NSString "
	
	pointer = " * "
	
	class_seperator = ""
	
	line_end = ";"
	
	base_class = "JSONModel"
	
	inherit_operator = " : "
	
	def printError(self, message):
		print "Error : " + message
		
		
	def __init__(self,file_name,root_class):
	
		self.file_name = file_name
		self.root_class = root_class
		
		try:
			obj = json.loads(self.readFile(self.file_name) )
			self.parseJson(obj,root_class,False)
		except:
			self.printError("invalid json string !")

			traceback.print_exc()
        	
		
		
	def write2File(self):
		
		self.writeHeader2File();
		self.writeImpl2File();
	
	def writeHeader2File(self):
	
		text_file = open(self.root_class + ".h", "w")
		for  k in self.class_define_array:
			text_file.write(k)
		text_file.close()
		
	def writeImpl2File(self):
	
		text_file = open(self.root_class + ".m", "w")
		text_file.write(self.new_line + "#import \"" + self.root_class + ".h\"" + self.new_line)
		for  k in self.class_array:
			text_file.write(self.new_line + self.implementation + k+ self.new_line + self.end+self.new_line)
		text_file.close()
		
	def readFile (self, file_name ):
        	file_handler = open(file_name)
        	file_text = file_handler.read()
		return file_text

	def firstLower(self, s):
		if len(s) == 0:
			return s
		else:
			return s[0].lower() + s[1:]

	def convert(self, word):
		res = "".join(x.capitalize() or '_' for x in word.split('_'))
		return self.firstLower(res)

	def parseJson (self, decoded_json_string, class_name,isprotocol ):
		if isprotocol == True :
			self.class_define_array.append(self.protocol+ class_name +" "+self.new_line+self.end+self.new_line)
		self.class_array.append(class_name)
		str =  self.new_line + self.interface +  class_name + self.inherit_operator + self.base_class
		for  k in decoded_json_string.keys():
			class_name = self.root_class
			v = decoded_json_string[k]
			if isinstance(v,float) or isinstance(v,int) or isinstance(v,long) or isinstance(v,bool):
				str += self.new_line + self.object_prefix + self.number_prefix + self.pointer+ k + self.line_end
			elif isinstance(v,basestring) :
				str += self.new_line + self.object_prefix +  self.string_prefix + self.pointer + k + self.line_end
			elif isinstance(v,dict):
				class_name = class_name + self.class_seperator + self.convert(k).capitalize()
				str += self.new_line + self.object_prefix + class_name + self.pointer + k + self.line_end
				self.parseJson(v,class_name,False)
			elif isinstance(v,list) or isinstance(v,tuple) :
				if len(v) == 0 :
					self.printError( "key '" + k + "' can not be empty!");
				value = v[0]
				if isinstance(value,float) or isinstance(value,int) or isinstance(value,long) or isinstance(value,bool) or isinstance(value,basestring):
					str += self.new_line + self.object_prefix + " NSMutableArray < Optional> * " + k + self.line_end
				else:
					class_name = class_name + self.class_seperator + self.convert(k).capitalize()
					str += self.new_line + self.object_prefix + " NSMutableArray <" + class_name + ",Optional> * " + k + self.line_end
					self.parseJson(v[0],class_name,True)
		str += self.new_line+self.end+self.new_line
		self.class_define_array.append(str)
		
	
object = jsonObject(sys.argv[1],sys.argv[2])
object.write2File();
