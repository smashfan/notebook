![33a9971f0e42496bbc10c8b8429f9a1](llama3_Template.assets/33a9971f0e42496bbc10c8b8429f9a1.png)

![8b54362bc1e2a015195cabfed0cd0d4](llama3_Template.assets/8b54362bc1e2a015195cabfed0cd0d4.png)

![55ca2b0d9e4c07046f3d92adfec4531](llama3_Template.assets/55ca2b0d9e4c07046f3d92adfec4531.png)

```
input_text = """<|im_start|>system 
You are a helpful AI assistant.
<|im_end|> 
<|im_start|>user
What is the most interesting fact about kangaroos that you know?
<|im_end|> 
<|im_start|>assistant
```





设置template



```
template = tokenizer.chat_template
template = template.replace("SYS", "SYSTEM")  # Change the system token
tokenizer.chat_template = template  # Set the new template
tokenizer.push_to_hub("model_name")  # Upload your new template to the Hub!
```

![1716643856277](llama3_Template.assets/1716643856277.png)