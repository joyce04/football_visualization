# -*- mode: python -*-
import sys
sys.setrecursionlimit(10000)

block_cipher = None

a = Analysis(['../py_source/run_app_package_ver.py'], # relative to the location of the spec file
             pathex=['.'],
             binaries=[],
             datas=[], 
             hiddenimports=[
                'umap',
                'pkg_resources',
                'cymem.cymem',
                'cytoolz._signatures',
                'cytoolz.utils',
                'dill',
                'murmurhash.mrmr',
                'spacy',
                'spacy.attrs',
                'spacy.compat',
                'spacy.errors',
                'spacy.glossary',
                'spacy.gold',
                'spacy.language',
                'spacy.lemmatizer',
                'spacy.lexeme',
                'spacy.matcher',
                'spacy.morphology',
                'spacy.parts_of_speech',
                'spacy.pipeline',
                'spacy.scorer',
                'spacy.strings',
                'spacy.structs',
                'spacy.symbols',
                'spacy.syntax',
                'spacy.syntax._beam_utils',
                'spacy.syntax.arc_eager',
                'spacy.syntax.ner',
                'spacy.syntax.nn_parser',
                'spacy.syntax.nonproj',
                'spacy.syntax.stateclass',
                'spacy.syntax.transition_system',
                'spacy.tokenizer',
                'spacy.tokens',
                'spacy.tokens._retokenize',
                'spacy.tokens.printers',
                'spacy.tokens.underscore',
                'spacy.typedefs',
                'spacy.util',
                'spacy.vectors',
                'spacy.vocab',
                'thinc.extra.search',
                'thinc.linalg',
                'thinc.neural._classes.difference',
                'cython', 'sklearn', 'sklearn.neighbors.typedefs',
                'sklearn.neighbors.quad_tree', 'sklearn.tree',
                'sklearn.tree._utils'
             ],
             hookspath=['./packaging_task'], # relative to the location executed pyinstaller
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='run_flask',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )