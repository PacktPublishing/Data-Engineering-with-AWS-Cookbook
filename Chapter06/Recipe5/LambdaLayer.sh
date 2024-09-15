sudo amazon-linux-extras install python3.8
curl -O https://bootstrap.pypa.io/get-pip.py
python3.8 get-pip.py --user

mkdir python
python3.8 -m pip install pyffx -t python/

zip -r layer.zip python

aws lambda publish-layer-version \
  --layer-name pyffx-layer \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.8 \
  --region <aws_region>