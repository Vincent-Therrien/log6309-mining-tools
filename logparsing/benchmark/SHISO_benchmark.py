#!/usr/bin/env python

import sys
sys.path.append('../')
from logparser import SHISO, evaluator
import os
import pandas as pd


input_dir = '../logs/' # The input directory of log file
output_dir = 'SHISO_result/' # The output directory of parsing results

benchmark_settings = {
    'HDFS': {
        'log_file': 'HDFS/HDFS_2k.log',
        'log_format': '<Date> <Time> <Pid> <Level> <Component>: <Content>',
        'regex': [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'],
        'maxChildNum': 4,
        'mergeThreshold': 0.1,
        'formatLookupThreshold': 0.3,
        'superFormatThreshold': 0.85
        },

    'BGL': {
        'log_file': 'BGL/BGL_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>',
        'regex': [r'core\.\d+'],
        'maxChildNum': 4,
        'mergeThreshold': 0.005,
        'formatLookupThreshold': 0.3,
        'superFormatThreshold': 0.85
        },

}

bechmark_result = []
for dataset, setting in benchmark_settings.iteritems():
    print('\n=== Evaluation on %s ==='%dataset)
    indir = os.path.join(input_dir, os.path.dirname(setting['log_file']))
    log_file = os.path.basename(setting['log_file'])

    parser = SHISO.LogParser(log_format=setting['log_format'], indir=indir, outdir=output_dir, rex=setting['regex'],
                            maxChildNum=setting['maxChildNum'], mergeThreshold=setting['mergeThreshold'],
                            formatLookupThreshold=setting['formatLookupThreshold'], superFormatThreshold=setting['superFormatThreshold'])
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
df_result.T.to_csv('SHISO_bechmark_result.csv')
