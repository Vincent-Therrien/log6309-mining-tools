#!/usr/bin/env python

import sys
sys.path.append('../')
from logparser import AEL, evaluator
import os
import pandas as pd


input_dir = '../logs/' # The input directory of log file
output_dir = 'AEL_result/' # The output directory of parsing results

benchmark_settings = {
    'HDFS': {
        'log_file': 'HDFS/HDFS_2k.log',
        'log_format': '<Date> <Time> <Pid> <Level> <Component>: <Content>',
        'regex': [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'],
        'minEventCount': 2,
        'merge_percent' : 0.5
        },

    'BGL': {
        'log_file': 'BGL/BGL_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>',
        'regex': [r'core\.\d+'],
        'minEventCount': 2,
        'merge_percent' : 0.5
        },
}

bechmark_result = []
for dataset, setting in benchmark_settings.iteritems():
    print('\n=== Evaluation on %s ==='%dataset)
    indir = os.path.join(input_dir, os.path.dirname(setting['log_file']))
    log_file = os.path.basename(setting['log_file'])

    parser = AEL.LogParser(log_format=setting['log_format'], indir=indir, outdir=output_dir,
                             minEventCount=setting['minEventCount'], merge_percent=setting['merge_percent'], rex=setting['regex'])
    parser.parse(log_file)
    
    F1_measure, accuracy = evaluator.evaluate(
                           groundtruth=os.path.join(indir, log_file + '_structured.csv'),
                           parsedresult=os.path.join(output_dir, log_file + '_structured.csv')
                           )
    bechmark_result.append([dataset, F1_measure, accuracy])


print('\n=== Overall evaluation results ===')
df_result = pd.DataFrame(bechmark_result, columns=['Dataset', 'F1_measure', 'Accuracy'])
df_result.set_index('Dataset', inplace=True)
print(df_result)
df_result.T.to_csv('AEL_bechmark_result.csv')
