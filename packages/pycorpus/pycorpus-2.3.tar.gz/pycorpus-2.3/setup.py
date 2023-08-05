# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycorpus']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.3,<5.0.0']

setup_kwargs = {
    'name': 'pycorpus',
    'version': '2.3',
    'description': 'Easy concurrent launch of series of file based experiments.',
    'long_description': 'This module provide a easy, non intrusive way to process a big list of files in a parallel way. Also provides the\noption to process theses files with a different packs of options, evaluate and generate reports.\n\n# Requirements:\n\nYou need the PPSS script in same dir of this file.\n\n# Instructions:\n\n1. Import this module from your main file\n\n    ```python\n    import pyCorpus\n    ```\n    \n2. Create the function that process the file\n\n    ```python\n    def my_process(file_name, config):\n        # Some science stuff with the file\n    ```\n\n3. (Optional) Create a function that return a argument parser that capture all the configs that you need.\n\n    ```python\n    def my_parser():\n        # Set up your argparse parser\n        # Return the parser\n        return my_parser_instance\n    ```\n    \n4. Add at the end of the file something like this:\n\n    ```python\n    if __name__ == "__main__":\n        corpus_processor = pyCorpus.CorpusProcessor(parse_cmd_arguments, process_file)\n        corpus_processor.run_corpus()\n   ```\n   \n# NOTES:\n\n * Dot not ADD the () to my_parser and my_process arguments.\n\n * If you don\'t need options you can ignore step 3 and the config file come as None. But never use the --config parameter.\n\n * The files are processed in a concurrent way so if you might store any results don\'t use the sys.out use a file.\n',
    'author': 'Josu Bermudez',
    'author_email': 'josubg@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/josubg/pycorpus/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
