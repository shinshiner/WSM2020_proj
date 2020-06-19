# WSM2020_proj

Code for WSM 2020 Project: Chinese WestLaw system

![demo](https://www.mdeditor.com/images/logos/markdown.png "markdown")

## Requirements

* Python3
* numpy
* Django 3.0.6 (For web interface)
* pkuseg
* nltk

## Data Preparation

Download the original data from the [course website](https://adapt.seiee.sjtu.edu.cn/wsm2020/wsm_proj1_data/).

### Data1 & Data2

1. Put the scripts `utils/index_for_data1.py` and `utils/index_for_data2.py` into the data folder, on the same position with `zxgk/` for data1, `info/` for data2.

2. Remove the duplicated files, rename the `.json` files with successive integer and build inverted index:

		python index_for_data1.py
		python index_for_data2.py

### Instrument
1. Build inverted index and tf-idf dictionary:

		# build inverted index
		python utils.py
		# build tf-idf dictionary
		python utils.py

2. Put the generated indexes and original data into folder `/xxx/`.

We also provide the [processed data](https://github.com/pandao/editor.md "Editor.md").

## Usage

1. Change to the root of the project, run `python manage.py runserver [port]` to start the server.

2. Search legal case records with boolean search, we also provide fuzzy search for wrongly inputs.
![boolean](https://www.mdeditor.com/images/logos/markdown.png "markdown")

3. Query instruments with a sentence.
![query sentence](https://www.mdeditor.com/images/logos/markdown.png "markdown")

4. Sort the results according to your needs.
![sort](https://www.mdeditor.com/images/logos/markdown.png "markdown")

## Contributor

* [Zelin Ye](https://github.com/shinshiner)
* [Ruolan Yang](https://github.com/MARCAXIAO)
* [Ruixiao Ma](https://github.com/ruolanyang)