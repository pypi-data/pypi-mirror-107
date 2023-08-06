# py-subwasm-bindings
Python bindings for subwasm utility: https://gitlab.com/chevdor/subwasm

## Installation

### Compile for local development

```
pip install -r requirements.txt
maturin develop
```
### Build wheelhouses
```
pip install -r requirements.txt

# Build local OS wheelhouse
maturin build

```

## Usage

```python
import json
import subwasm

# Show metadata from WASM file
metadata_str = subwasm.get_metadata("runtime_000.wasm")
metadata_json = json.loads(metadata_str)
print(json.dumps(metadata_json, indent=4))

# Show metadata from local Substrate node
metadata_str = subwasm.get_metadata("http://127.0.0.1:9933")
metadata_json = json.loads(metadata_str)
print(json.dumps(metadata_json, indent=4))

```

## License
https://github.com/polkascan/py-sr25519-bindings/blob/master/LICENSE
