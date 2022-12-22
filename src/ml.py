def visualize_network(path: str, height: int = 500, port: int = 8000) -> None:
    """Visualize a neural network with a path to its saved architecture. 
       You can also set the height of visualization (default 500px) and 
       which port it is served on (default 8000). The heavy lifting is 
       done by netron, which support Netron supports a huge array of file:
       formats ONNX, TensorFlow Lite, Caffe, Keras, Darknet, PaddlePaddle, 
       ncnn, MNN, Core ML, RKNN, MXNet, MindSpore Lite, TNN, Barracuda, 
       Tengine, CNTK, TensorFlow.js, Caffe2 and UFF."""
    from netron import serve
    from IPython.display import Javascript
    # from IPython.core.display.display_functions import di
    from .env import is_notebook

    if is_notebook():
        serve(path, None, ("localhost", port), False, 0)
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
        serve(path, None, ("localhost", port), True, 0)
    
