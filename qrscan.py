import os
try:
    from PIL import Image
    _HAS_PIL = True
except Exception:
    Image = None
    _HAS_PIL = False
import hashlib

def _load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k not in os.environ:
                        os.environ[k] = v


def _avg_hash(image, hash_size=8):
    image = image.convert('L').resize((hash_size, hash_size), Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    bits = ''.join('1' if p > avg else '0' for p in pixels)
    return bits


def _hamming(a, b):
    return sum(ch1 != ch2 for ch1, ch2 in zip(a, b))


def compare_images(uploaded_path, threshold=10):
    _load_env()
    ref_path = os.environ.get('IMG_PATH')
    if not ref_path:
        raise RuntimeError('IMG_PATH not set in environment or .env')
    if not os.path.isabs(ref_path):
        ref_path = os.path.join(os.path.dirname(__file__), ref_path)
    if not os.path.exists(ref_path):
        raise FileNotFoundError(f'Reference image not found: {ref_path}')
    if not os.path.exists(uploaded_path):
        raise FileNotFoundError(f'Uploaded image not found: {uploaded_path}')

    if _HAS_PIL:
        ref = Image.open(ref_path)
        up = Image.open(uploaded_path)
        ref_hash = _avg_hash(ref)
        up_hash = _avg_hash(up)
        dist = _hamming(ref_hash, up_hash)
        return dist <= threshold
    else:
        def _sha256(path):
            h = hashlib.sha256()
            with open(path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b''):
                    h.update(chunk)
            return h.hexdigest()
        return _sha256(ref_path) == _sha256(uploaded_path)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python qrscan.py <uploaded_image_path>')
        sys.exit(2)
    ok = compare_images(sys.argv[1])
    print('MATCH' if ok else 'NO MATCH')

