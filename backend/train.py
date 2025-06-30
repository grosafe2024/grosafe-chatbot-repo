from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType, prepare_model_for_kbit_training
from datasets import load_dataset

# Need to login into Hugging Face account to access the model.
# `huggingface-cli login` in terminal.

# Load base model TinyLlama (open and fine-tuning friendly) and tokenizer.
model_name = "ibm-granite/granite-3.3-2b-instruct"  # Fallback to Mistral-2B
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Setup LoRA Adapter (no quantisation due to no GPU support).
peft_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    bias="none",
    target_modules=["q_proj", "v_proj"],  # <-- add this
    inference_mode=False
)

# Apply the LoRA adapter to the model.
model = get_peft_model(model, peft_config)

# Load and format GroSafe train dataset.
dataset = load_dataset("json", data_files="train_data.jsonl")
def format(example):
    if example.get("input"):
        prompt = f"<s>[INST] {example['instruction']}\n\nInput: {example['input']} [/INST] {example['output']}</s>"
    else:
        prompt = f"<s>[INST] {example['instruction']} [/INST] {example['output']}</s>"

    tokens = tokenizer(prompt, padding="max_length", truncation=True, max_length=512, return_tensors="pt")
    return {
        "input_ids": tokens["input_ids"][0],
        "labels": tokens["input_ids"][0]
    }

# Format the dataset.
dataset = dataset["train"].map(format)

# Prepare model for training.
training_args = TrainingArguments(
    output_dir="./grosafe_adapter",
    per_device_train_batch_size=1,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_steps=5,
    learning_rate=2e-4,
    bf16=False,  # CPU only
    fp16=False,
    optim="adamw_torch"
)

# Initialize the trainer.
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset
)

# Train the model.
trainer.train()

# Save the adapter(only).
model.save_pretrained("grosafe-lora")
tokenizer.save_pretrained("grosafe-lora")