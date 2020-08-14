declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"
mkdir -p "$DIR/build"

declare addon_id='persitent_editor'

cd "$DIR"

"$DIR/bin/compile.sh"

zip -r "$DIR/build/$addon_id.ankiaddon" \
  "manifest.json" \
  "__init__.py" \
  "src/"*".py" \
  "gui/"*".py" \
  "gui/forms/"*".py" \
  "web/"* \
