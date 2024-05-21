# 部署

```shell
# 安装工具
pip install setuptools
pip install wheel
pip install twine    

# 打包
python setup.py sdist bdist_wheel  

# 上传
#twine upload -r nexus dist/*  

twine upload -r pypi dist/*  
```
