# mcp-weather-python-demo

#### 介绍
基于Python SDK MCP天气 Server开发

1、技术环境
■ Python 3.10或更高版本；
■ MCP Python SDK 1.6.0；
■ 推荐使用uv管理Python项目；
■ 如果需要，还可以创建PyPI账号，以发布Python包。

2、业务流程
（1）首先，用户向大模型提出天气查询请求，例如"北京今天天气如何？"。 
（2）大模型分析用户的问题，判断需要使用天气工具来回答。 
（3）大模型通过Client请求使用current_weather工具，并等待用户确认。 
（4）用户确认工具调用后，Client将请求发送到我们的MCP天气服务器。 
（5）MCP Server执行current_weather函数，向心知天气的Seniverse API发送请求，获取该地址的详细天气数据。 
（6）MCP Server将API返回的原始数据格式化为结构化的天气信息。 
（7）格式化后的天气数据通过Client返回给大模型。
（8）大模型根据天气数据生成自然语言回答。

3、时序图
![输入图片说明](%E6%96%B0%E5%AF%B9%E8%AF%9D.png)

4、项目是通过uv进行管理，进入根目录，需执行uv init 创建项目框架，并配置好pyproject.toml里的项目信息
