from vllm import LLM
llm = LLM(model='mistralai/Mistral-7B-Instruct-v0.1', tokenizer='hf-internal-testing/llama-tokenizer', tensor_parallel_size=2,dtype='float16')
output = llm.generate("San Franciso is a")
print(output)
