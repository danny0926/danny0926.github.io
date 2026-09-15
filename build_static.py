"""Copy only the static website into the Sites deployment directory."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
out = root / 'dist'
out.mkdir(exist_ok=True)
for pattern in ('*.html', '*.css', '*.js'):
    for source in root.glob(pattern):
        shutil.copy2(source, out / source.name)
shutil.copytree(root / 'assets', out / 'assets', dirs_exist_ok=True)
print('Static website prepared: dist/')
