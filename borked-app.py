import os
import csv
from pathlib import Path
from glob import glob
import copy
import gradio as gr
import re
import secrets
import tempfile
from modelscope import (AutoModelForCausalLM, AutoTokenizer, GenerationConfig)
from huggingface_hub import snapshot_download
from argparse import ArgumentParser

DEFAULT_CKPT_PATH = '4bit/Qwen-VL-Chat-Int4'
REVISION = 'v1.0.0'
BOX_TAG_PATTERN = r"<box>([\s\S]*?)</box>"
PUNCTUATION = "！？。＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏."

def _get_args():
    parser = ArgumentParser()
    parser.add_argument("-c", "--checkpoint-path", type=str, default=DEFAULT_CKPT_PATH, help="Checkpoint name or path, default to %(default)r")
    parser.add_argument("--revision", type=str, default=REVISION)
    parser.add_argument("--cpu-only", action="store_true", help="Run demo with CPU only")
    parser.add_argument("--share", action="store_true", default=False, help="Create a publicly shareable link for the interface.")
    parser.add_argument("--inbrowser", action="store_true", default=False, help="Automatically launch the interface in a new tab on the default browser.")
    parser.add_argument("--server-port", type=int, default=8000, help="Demo server port.")
    parser.add_argument("--server-name", type=str, default="127.0.0.1", help="Demo server name.")
    args = parser.parse_args()
    return args

def _load_model_tokenizer(args):
    model_id = args.checkpoint_path
    model_dir = snapshot_download(model_id)
    tokenizer = AutoTokenizer.from_pretrained(
        model_dir, trust_remote_code=True, resume_download=True,
    )
    if args.cpu_only:
        device_map = "cpu"
    else:
        device_map = "auto"
    model = AutoModelForCausalLM.from_pretrained(
        model_dir, device_map=device_map, trust_remote_code=True, resume_download=True,
    ).eval()
    model.generation_config = GenerationConfig.from_pretrained(
        model_dir, trust_remote_code=True, resume_download=True,
    )
    return model, tokenizer

def _parse_text(text):
    lines = text.split("\n")
    lines = [line for line in lines if line != ""]
    count = 0
    for i, line in enumerate(lines):
        if "```" in line:
            count += 1
            items = line.split("`")
            if count % 2 == 1:
                lines[i] = f'<pre><code class="language-{items[-1]}">'
            else:
                lines[i] = f"<br></code></pre>"
        else:
            if i > 0:
                if count % 2 == 1:
                    line = line.replace("`", r"\`")
                line = line.replace("<", "&lt;")
                line = line.replace(">", "&gt;")
                line = line.replace(" ", "&nbsp;")
                line = line.replace("*", "&ast;")
                line = line.replace("_", "&lowbar;")
                line = line.replace("-", "&#45;")
                line = line.replace(".", "&#46;")
                line = line.replace("!", "&#33;")
                line = line.replace("(", "&#40;")
                line = line.replace(")", "&#41;")
                line = line.replace("$", "&#36;")
            lines[i] = "<br>" + line
    text = "".join(lines)
    return text

def process_images_in_folder(folder_path, task_history, model, tokenizer):
    """Process all images in a given folder."""
    results = []
    image_files = glob(os.path.join(folder_path, '*'))
    
    for image_file in image_files:
        input_text = f"Processing {os.path.basename(image_file)}"
        task_history = task_history + [((image_file,), None)]
        history_copy = []
        chatbot = [(input_text, None)]
        add_file(history_copy, task_history, Path(image_file))
        predict(chatbot, task_history)
        response_text = chatbot[-1][1]
        results.append((os.path.basename(image_file), response_text))

    return results

def save_results_to_csv(results, output_file):
    """Save the results to a CSV file."""
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Image", "Response"])
        for result in results:
            writer.writerow(result)

def predict(_chatbot, task_history):
    # Implementation to predict response based on model
    ...

def add_file(history, task_history, file):
    history = history + [((file.name,), None)]
    task_history = task_history + [((file.name,), None)]
    return history, task_history

def _launch_demo(args, model, tokenizer):
    def folder_button_click(folder_path, task_history):
        # Get the results
        results = process_images_in_folder(folder_path, task_history, model, tokenizer)
        # Define the output file
        output_csv = 'results.csv'
        # Save the results to CSV
        save_results_to_csv(results, output_csv)
        return f"Processing completed, results saved to {output_csv}"

    with gr.Blocks() as demo:
        gr.Markdown("### Batch Process Images from Folder and Save Results")

        folder_input = gr.Textbox(placeholder="Enter path to folder with images", label="Folder Path")
        process_button = gr.Button("Process Images")

        result_text = gr.Textbox(label="Result", interactive=False)

        process_button.click(folder_button_click, [folder_input, gr.State([])], result_text)

        demo.launch(
            share=args.share,
            inbrowser=args.inbrowser,
            server_port=args.server_port,
            server_name=args.server_name,
        )

def main():
    args = _get_args()
    model, tokenizer = _load_model_tokenizer(args)
    _launch_demo(args, model, tokenizer)

if __name__ == '__main__':
    main()
