"""Copy the static website to a local output directory; never upload or deploy."""
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent
out = root / 'dist'
out.mkdir(exist_ok=True)
for pattern in ('*.html', '*.css', '*.js', '*.jsx'):
    for source in root.glob(pattern):
        shutil.copy2(source, out / source.name)
shutil.copytree(root / 'assets', out / 'assets', dirs_exist_ok=True)
print('Static website prepared: dist/')
