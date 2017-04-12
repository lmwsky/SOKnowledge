import os

from jpype import *

from SOKnowledge.settings import BASE_DIR

__base_dir__ = os.path.join(BASE_DIR, 'SOKnowledge/ctr_util')
MODEL_FILE_PATH = os.path.join(__base_dir__, 'model/trainModel.txt')

FEATURE_FILE_PATH = os.path.join(__base_dir__, 'model/feature_words.txt')


class CodeBlockTypeTagger(object):
    """
    CodeBlock type tagger
    """
    MODEL_JAR_PATH = os.path.join(__base_dir__, 'model/jar/')
    MODEL_JAR_PATH_NAME = 'SOmodel.jar'

    def __init__(self):
        self.active_model = None

    def init_model_bays(self,
                        jar_path=MODEL_JAR_PATH,
                        jar_name=MODEL_JAR_PATH_NAME,
                        feature_file_path=FEATURE_FILE_PATH,
                        model_file_path=MODEL_FILE_PATH):
        startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (jar_path + jar_name))
        InvokeModelClass = JClass("Invoke")
        # jd = JPackage("jpype").JpypeDemo() # two way
        self.active_model = InvokeModelClass()

        self.active_model.init(feature_file_path, model_file_path)

    def tag(self, text):
        if self.active_model and text:
            tags = self.active_model.tag(text)
            return tags
        return None

    def deactive_model(self):
        shutdownJVM()

    def tagWithInit(self,
                    text,
                    jar_path=MODEL_JAR_PATH,
                    jar_name=MODEL_JAR_PATH_NAME,
                    feature_file_path=FEATURE_FILE_PATH,
                    model_file_path=MODEL_FILE_PATH):
        startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s" % (jar_path + jar_name))
        InvokeModelClass = JClass("Invoke")
        # jd = JPackage("jpype").JpypeDemo() # two way
        active_model = InvokeModelClass()

        active_model.init(feature_file_path, model_file_path)
        if active_model and text:
            tags = active_model.tag(text)
            shutdownJVM()
            return tags
        else:
            shutdownJVM()
            return None


if __name__ == "__main__":
    text = """I want to use a track-bar to change a form 's opacity .

This is my code : <code>var ts = new TimeSpan ( DateTime.UtcNow.Ticks - dt.Ticks ) ; double delta = Math.Abs ( ts.TotalSeconds ) ; if ( delta < 60 ) { return ts.Seconds</code> == 1 ?

`` one second ago '' : <code>ts.Seconds + `` seconds ago '' ; } if ( delta < 120 ) { return `` a minute ago '' ; } if ( delta < 2700 ) // 45 * 60 { return ts.Minutes + `` minutes ago '' ; } if ( delta < 5400 ) // 90 * 60 { return `` an hour ago '' ; } if ( delta < 86400 ) // 24 * 60 * 60 { return ts.Hours + `` hours ago '' ; } if ( delta < 172800 ) // 48 * 60 * 60 { return `` yesterday '' ; } if ( delta < 2592000 ) // 30 * 24 * 60 * 60 { return ts.Days + `` days ago '' ; } if ( delta < 31104000 ) // 12 * 30 * 24 * 60 * 60 { int months = Convert.ToInt32 ( Math.Floor ( ( double ) ts.Days / 30 ) ) ; return months < =</code> 1 ?

`` one month ago '' : <code>months + `` months ago '' ; } int years = Convert.ToInt32 ( Math.Floor ( ( double ) ts.Days / 365 ) ) ; return years < =</code> 1 ?

`` one year ago '' : years + `` years ago '' ; When I try to build it , I get this error : Can not implicitly convert type 'decimal ' to 'double ' .

I tried making _sc1_ a _sc2_ , but then the control does n't work .

This code has worked fine for me in VB.NET in the past .
"""
    tagger = CodeBlockTypeTagger()
    tagger.init_model_bays()

    typeIds=tagger.tag(text)
