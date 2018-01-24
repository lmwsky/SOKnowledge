#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

__eval_path = "./evaluation"
__eval_temp = os.path.join(__eval_path, "temp")
__eval_script = os.path.join(__eval_path, "conlleval")

eval_id=1211079
output_path = os.path.join(__eval_temp, "eval.%i.output" % eval_id)
scores_path = os.path.join(__eval_temp, "eval.%i.scores" % eval_id)

print 'eval_script path=',__eval_script
print 'eval_output_path=',output_path
command="perl %s < %s > %s" % (__eval_script, output_path, scores_path)
print 'command=',command
os.system(command)
