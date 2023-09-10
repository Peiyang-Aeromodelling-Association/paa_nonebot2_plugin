# 纳新bot插件

基于[nonebot2](https://github.com/nonebot/nonebot2)框架。

> [!IMPORTANT] 
> 如果要在新的纳新群使用，请确保：
> 
> 1. 修改`__init__.py`中的`if event.group_id == 537857732:`为对应纳新群群号。
> 2. 在go-cqhttp的`config.yml`设置`allow-temp-session: true`，允许发起临时会话。
> 3. 群管理员设置QQ群允许发起临时会话。
> 4. 设置纳新bot为管理员。
