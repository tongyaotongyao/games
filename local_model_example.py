import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

def setup_model(model_name="deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct"):
    """
    配置4-bit量化模型加载
    适合RTX 4060 8GB显存
    """
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    
    return model, tokenizer

def generate_code(model, tokenizer, prompt, max_new_tokens=512):
    """
    生成代码
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=0.7,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    print("正在加载模型...")
    model, tokenizer = setup_model()
    
    print("模型加载完成！")
    print("="*50)
    
    # 测试示例
    test_prompt = "请用Python写一个快速排序算法，包含注释"
    
    print(f"\n提示词: {test_prompt}")
    print("\n生成中...\n")
    
    result = generate_code(model, tokenizer, test_prompt)
    print(result)
