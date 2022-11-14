# README

Compare between two pip freeze output text

usage

```bash
usage: compare two pip freeze output [-h] [--output-format {csv,markdown}] [--sort] file1 file2

positional arguments:
  file1
  file2

optional arguments:
  -h, --help            show this help message and exit
  --output-format {csv,markdown}
  --sort                sort alpha
```

example

```bash
# pip freeze > freeze1.txt
# pip freeze > freeze2.txt
python -m main freeze1.txt freeze2.txt  --sort
```
