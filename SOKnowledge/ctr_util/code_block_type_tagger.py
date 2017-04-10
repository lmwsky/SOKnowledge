import os

from jpype import *

MODEL_FILE_PATH = os.path.join(os.path.abspath('.'), 'model/trainModel.txt')

FEATURE_FILE_PATH = os.path.join(os.path.abspath('.'), 'model/feature_words.txt')


class CodeBlockTypeTagger(object):
    """
    CodeBlock type tagger
    """
    MODEL_JAR_PATH = os.path.join(os.path.abspath('.'), 'model/jar/')
    MODEL_JAR_PATH_NAME = 'SOmodel.jar'

    def __init__(self):
        self.active_model = None

    def init_model_bays(self,
                        jar_path=MODEL_JAR_PATH,
                        jar_name=MODEL_JAR_PATH_NAME,
                        feature_file_path=FEATURE_FILE_PATH,
                        model_file_path=MODEL_FILE_PATH):
        jar_full_path = os.path.join(jar_path, jar_name)
        startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=%s{0}".format(jar_full_path))
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
