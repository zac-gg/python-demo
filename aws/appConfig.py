import boto3

# 创建 AppConfig 客户端
appconfig = boto3.client('appconfig', region_name='ap-northeast-1')

# 定义 AppConfig 资源的相关参数
application = 'iblowy1'  # 您的应用程序 ID
environment = '8htx3jo'  # 您的环境 ID
configuration = 'profile'  # 您的配置配置文件 ID
client_id = 'your-client-id'  # 一个用于区分不同客户端实例的唯一字符串

try:
    # 从 AWS AppConfig 获取配置
    response = appconfig.get_configuration(
        Application=application,
        Environment=environment,
        Configuration=configuration,
        ClientId=client_id
    )

    # 读取并打印配置内容
    configuration_content = response['Content'].read()
    print(configuration_content.decode('utf-8'))

except Exception as e:
    print(f"Error getting configuration from AWS AppConfig: {e}")
