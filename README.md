### More SG Modifications

Ok, the 'app.py' works (or at least, the version previous to me messing with it.) You can run it on collab with:

```
%cd /content
#!wget https://raw.githubusercontent.com/camenduru/Qwen-VL-Chat-colab/main/app.py -O /content/app.py
!wget https://raw.githubusercontent.com/shawngraham/Qwen2-VL-jupyter/refs/heads/main/app.py -O /content/app.py 

!pip install -q tiktoken transformers_stream_generator gradio==3.50.2 optimum auto-gptq huggingface_hub
!pip install -q modelscope -f https://pypi.org/project/modelscope

!python app.py --share
```
in a cell. Source of app.py: [camenduru/Qwen-VL-Chat-colab](https://github.com/camenduru/Qwen-VL-Chat-colab)

### SG modifications

I have slightly modified the Qwen2_VL_7b_Instruct notebook to accept a folder of images as input, and to write the result to dataframe/export to csv. A default prompt ("Extract text") is pre-populated.

Try it out at [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/shawngraham/Qwen2-VL-jupyter/blob/main/Qwen2-VL-ocr.ipynb) | Qwen for OCR!


### Original README.md

🐣 Please follow me for new updates https://twitter.com/camenduru <br />
🔥 Please join our discord server https://discord.gg/k5BwmmvJJU <br />
🥳 Please join my patreon community https://patreon.com/camenduru <br />

### 🍊 Jupyter Notebook

| Notebook | Info
| --- | --- |
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/camenduru/Qwen2-VL-jupyter/blob/main/Qwen2_VL_2B_Instruct.ipynb) | Qwen2_VL_2B_Instruct (8bit)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/camenduru/Qwen2-VL-jupyter/blob/main/Qwen2_VL_7B_Instruct.ipynb) | Qwen2_VL_7B_Instruct (8bit)

### 🧬 Code
https://github.com/QwenLM/Qwen-VL <br />
https://github.com/QwenLM/Qwen2-VL <br />

### 📄 Paper
https://arxiv.org/abs/2308.12966

### 🌐 Page
https://qwenlm.github.io/blog/qwen2-vl/

### 🖼 Output
![Screenshot 2024-08-30 065333](https://github.com/user-attachments/assets/fbfaf82a-d801-46d2-9bf3-2a8ebb6f3f6b)
