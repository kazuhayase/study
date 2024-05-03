#https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF

from ctransformers import AutoModelForCausalLM

mpath="/home/kazuyoshi/Downloads/"
model="codellama-7b-instruct.Q8_0.gguf"

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained("TheBloke/CodeLlama-7B-Instruct-GGUF",
#                                           model_file="codellama-7b-instruct.q4_K_M.gguf",
                                           model_file=mpath+model,
                                           model_type="llama",
                                           gpu_layers=0)

print(llm("AI is going to"))
