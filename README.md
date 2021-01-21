# arXiv-dl 

Download paper from arXiv

## Installation 

```bash
pip install --upgrade arxiv-dl
```

## Configuration (Optional)

Default Download Destination: 

```bash
"{$HOME}/Downloads/ArXiv_Papers"
```

Set Custom Download Destination via Environment Variable

```bash
source ARXIV_DOWNLOAD_FOLDER="{$HOME}/Documents/papers"
```

## Usage

```bash
add-paper "URL"
```
`add-paper` will do

- Download paper `{paper_id}_{title}.pdf` into `ARXIV_DOWNLOAD_FOLDER`.
- Maintain a paper list containing metadata in json at `ARXIV_DOWNLOAD_FOLDER/000_Paper_List.json`.
- Create a new MarkDown document named `{paper_id}_Notes.md` in the same directory. (for you to add reading notes)

```bash
dl-paper "URL"
```
`dl-paper` will do

- Download paper `{paper_id}_{title}.pdf` into `ARXIV_DOWNLOAD_FOLDER`.

## Currently supported URLs

- URLs from `arXiv.org`
    - Paper's abstract page `https://arxiv.org/abs/xxxx.xxxxx` 
    - or Paper's PDF URL `https://arxiv.org/pdf/xxxx.xxxxx.pdf`

## License

[MIT License](LICENSE) Copyright (c) 2021 Mark Huang