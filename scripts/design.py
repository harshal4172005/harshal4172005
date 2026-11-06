"""Rebuild the middle sections. Original supplied hero and footer stay intact.
Requires fonttools and the Windows fonts configured in common.py.
"""
from sections import heading, model_card
from stack import forward_pass, inference_graph
import runpy
from pathlib import Path

if __name__=='__main__':
    for args in [('01','Model card','about.md',"who is behind the weights"),('02','Forward pass','stack/','the tools, connected'),('03','Inference graph','production/','NexAI Labs in production'),('04','Detections','projects/',"things I have shipped"),('05','Live signal','activity/','generated from GitHub')]:heading(*args)
    model_card();forward_pass();inference_graph()
    runpy.run_path(str(Path(__file__).with_name('cards.py')))
    print('Rebuilt all profile sections.')
