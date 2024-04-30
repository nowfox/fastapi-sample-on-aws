English | [简体中文](README_zh.md)

<p align="center">
    <h3 align="center">FastAPI Sample on AWS</h3>
</p>
<p align="center">FastAPI provides services through ApiGateway.</p>

<p align="center">
  <a href="https://nowfox.github.io/fastapi-sample-on-aws/en/"><strong>Documentation</strong></a>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg" alt="Apache 2.0 License"></a>
  <a href="https://github.com/nowfox/fastapi-sample-on-aws/releases"><img src="https://img.shields.io/github/v/release/nowfox/fastapi-sample-on-aws?include_prereleases"></a>
</p>

Please make sure **docker** is installed and the CDK command is executed in the **same region** of the model files which are uploaded in previous step. 

## Deploy CDK Template
Please make sure **docker** and **cdk** ard installed. 

```bash
cd source/constructs
cdk deploy
```