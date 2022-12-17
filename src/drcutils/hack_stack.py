import numpy
import pandas
import datasets
import keras
import matplotlib.pyplot
import sklearn
import gradio

def visualize_network(path: str, height: int = 500, port: int = 8000):
    from netron import serve
    from IPython.display import Javascript
    # url = eval_js("google.colab.kernel.proxyPort(8000)")
    if is_notebook():
        serve("mobilenet.h5", None, ("localhost", port), False, 0)
        display(Javascript("""
        (async ()=>{
            fm = document.createElement('iframe')
            fm.src = await google.colab.kernel.proxyPort(%s)
            fm.width = '95%%'
            fm.height = '%d'
            fm.frameBorder = 0
            document.body.append(fm)
        })();
        """ % (port, height) ))
    else:
        serve("mobilenet.h5", None, ("localhost", port), True, 0)
    
