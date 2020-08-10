declare DIR="$(cd "$(dirname "$0")/.." && pwd -P)"

for filename in "$DIR/gui/"*'.ui'; do
  pyuic5 "$filename" > "${filename%.*}_ui.py"
done

echo 'Was successfully compiled!'
