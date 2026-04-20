# Source global definitions
if [ -f /etc/bashrc ]; then
  . /etc/bashrc
fi

_set_aws_region() {
  local curl_opts="--retry 5 -f --silent --connect-timeout 2"
  local token=$(curl ${curl_opts} -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 15")
  export AWS_DEFAULT_REGION=$(curl ${curl_opts} -H "X-aws-ec2-metadata-token: ${token}" http://169.254.169.254/latest/dynamic/instance-identity/document | grep region | awk -F\" '{print $4}')

  unset -f $FUNCNAME
}

# set the default region for the AWS CLI
_set_aws_region
export JAVA_HOME=/etc/alternatives/jre
export HOME=/home/hadoop
