#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

models_path = "./models"
eval_path = "./evaluation"
eval_temp = os.path.join(eval_path, "temp")
eval_script = os.path.join(eval_path, "conlleval")

eval_id=1211079
output_path = os.path.join(eval_temp, "eval.%i.output" % eval_id)
scores_path = os.path.join(eval_temp, "eval.%i.scores" % eval_id)

print 'eval_script path=',eval_script
print 'eval_output_path=',output_path
command="perl %s < %s > %s" % (eval_script, output_path, scores_path)
print 'command=',command
os.system(command)
