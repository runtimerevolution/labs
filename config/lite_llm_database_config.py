from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Config
import yaml


configs= {}

def load_config_from_db():
  config_objs = Config.objects.all()

  for config in config_objs:
    configs[config.key] = config.value

  return configs

def rewrite_config_yaml():
  yaml_config = {}

  with open("litellm.yaml", "r") as file:
    yaml_config = yaml.safe_load(file)

  for model in yaml_config['model_list']:
    for key, value in model['litellm_params']:
      model['litellm_params'][key] = get_variable(value)

  with open("tmp_litellm.yaml", "w") as file:
    yaml.dump(yaml_config, file)

def get_variable(value):
  if 'os.environ/' in value:
    env_name = value.split('/')[1]
    return configs[env_name]
  else: 
    return value

@receiver(post_save, sender=Config)
def update_api_keys(sender, instance, **kwargs):
  global configs
  configs = load_config_from_db()
  rewrite_config_yaml()
  print(f"Configuration reloaded.")



