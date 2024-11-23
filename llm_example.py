import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load model and tokenizer directly instead of using pipeline
model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Prepare input
prompt = "What is the capital of France?"
inputs = tokenizer(prompt, return_tensors="pt")

# Generate
output_sequences = model.generate(
    **inputs,
    max_length=30,
    num_return_sequences=1,
    pad_token_id=tokenizer.eos_token_id
)

# Decode and print
generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
# print(f"Prompt: {prompt}")
print(f"Generated text: {generated_text}")