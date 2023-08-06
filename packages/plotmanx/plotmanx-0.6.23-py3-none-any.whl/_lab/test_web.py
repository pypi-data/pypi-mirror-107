from source.plotmanx import configuration
from source.plotmanx.query.api import start_master_api_node

print("before __name__ guard")
if __name__ == '__main__':
    cfg = configuration.get_validated_configs()
    start_master_api_node(cfg)
print("after __name__ guard")
