"""Setup script to create project structure and files"""

import os

directories = ['ui', 'services', 'models', 'config']
for directory in directories:
    os.makedirs(directory, exist_ok=True)
    print(f"✓ Created directory: {directory}")

init_files = [
    'ui/__init__.py',
    'services/__init__.py',
    'models/__init__.py',
    'config/__init__.py'
]

for init_file in init_files:
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            package_name = os.path.dirname(init_file)
            f.write(f'"""{package_name.capitalize()} package"""\n')
        print(f"✓ Created: {init_file}")

print("\n✓ Project structure created successfully!")
print("\nNow copy your Python files into the appropriate directories:")
print("  - UI files → ui/")
print("  - Service files → services/")
print("  - Model files → models/")