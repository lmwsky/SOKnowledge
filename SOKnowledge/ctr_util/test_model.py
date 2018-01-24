from jpype import *
import os.path

jarpath = os.path.join(os.path.abspath('.'), 'model/jar/')
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (jarpath + 'SOmodel.jar'))
JDClass = JClass("Invoke")
jd = JDClass()
# jd = JPackage("jpype").JpypeDemo() # two way
feature_file_path = os.path.join(os.path.abspath('.'), 'model/feature_words.txt')
model_file_path = os.path.join(os.path.abspath('.'), 'model/trainModel.txt')


text="""
I want to use a track-bar to change a form 's opacity .
This is my code : <code>print "Hello world!" </code>
When I try to build it , I get this error : Can not implicitly convert type 'decimal ' to 'double ' .
"""
jd.init(feature_file_path,model_file_path)
tags=jd.tag(text)
for t in tags:
    print 'code type=',t
shutdownJVM()
