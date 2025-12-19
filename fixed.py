import os

# Apps papkasi joylashuvi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APPS_DIR = os.path.join(BASE_DIR, 'apps')


def fix_app_configs():
    # apps papkasi ichidagi barcha papkalarni olamiz
    if not os.path.exists(APPS_DIR):
        print("❌ 'apps' papkasi topilmadi!")
        return

    apps_list = [d for d in os.listdir(APPS_DIR) if os.path.isdir(os.path.join(APPS_DIR, d))]

    for app_name in apps_list:
        if app_name == '__pycache__':
            continue

        apps_py_path = os.path.join(APPS_DIR, app_name, 'apps.py')

        # Class nomini yaratish (masalan: users -> UsersConfig)
        class_name = app_name.capitalize() + 'Config'
        if '_' in app_name:
            # masalan: order_items -> OrderItemsConfig
            class_name = ''.join(x.capitalize() for x in app_name.split('_')) + 'Config'

        # Faylga yoziladigan kod
        content = f"""from django.apps import AppConfig

class {class_name}(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.{app_name}'
"""

        # Faylga yozish
        with open(apps_py_path, 'w') as f:
            f.write(content)

        print(f"✅ To'g'irlandi: apps/{app_name}/apps.py -> name='apps.{app_name}'")


if __name__ == "__main__":
    fix_app_configs()
    print("\n🎉 Barcha apps.py fayllari muvaffaqiyatli yangilandi!")