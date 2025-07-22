# 🖼️ AI Image Caption Generator

Generate smart and descriptive captions for any image using the **BLIP (Bootstrapping Language-Image Pre-training)** model from Hugging Face! This project includes a fully functional and styled **Streamlit app** powered by **Transformers**, **PyTorch**, and **PIL**, offering a seamless experience from upload to download.

---

## 🚀 Live Demo

🔗 Try it now on [Hugging Face Spaces](https://huggingface.co/spaces/saadtoorx/ai-image-caption-generator)

---

## 📌 Features

- 📷 Upload PNG, JPG, or JPEG images
- 🤖 Generates captions using Hugging Face’s BLIP model
- 🎛 Adjustable caption length slider (20 to 100 tokens)
- 💾 Download the generated caption as a `.txt` file
- 🔁 One-click regeneration for varied results
- 🧠 Efficient model caching to prevent lags
- ✨ Responsive and visually enhanced UI with custom CSS

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** – for the interactive user interface
- **Transformers** – for loading the BLIP model
- **PyTorch** – backend deep learning framework
- **Pillow (PIL)** – image handling
- **Hugging Face** – pretrained model repository
- **io**, **hashlib** – for efficient in-memory file operations

---

## 🧪 Example Output

| 📸 Uploaded Image | 📝 Generated Caption |
|------------------|----------------------|
| `sample_image.jpg` | *"A dog sitting on a grassy field with trees in the background."* |

---

## 📁 Project Structure

```
📦 ai-image-caption-generator
├── .github             #Git Repo Files
├── app.py              # Streamlit App
├── app.ipynb           # Jupyter Notebook
├── utils.py            # Utility File
├── requirements.txt    #Requirements File
├── README.md           # Readme
├── images/             #Images Folde
│   └── output1.png
    └── output2.png
    └── output3.png
```

---

## 🧠 How It Works

- Upload an image file.
- BLIP processor converts it to tensor input.
- BLIP model generates a caption using beam search.
- Output is decoded and presented with styling.
- You can adjust the caption length or regenerate for new variations.

---

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/saadtoorx/ai-image-caption-generator.git
cd ai-image-caption-generator
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the Streamlit app

```bash
streamlit run app.py
```

---

## 🤖 Model Used

- **Model Name:** [Salesforce/blip-image-captioning-base](https://huggingface.co/Salesforce/blip-image-captioning-base)
- **Framework:** PyTorch
- **Hosted via:** Hugging Face Transformers

---

## ☁️ Hugging Face Deployment Setup

### Space Configuration (`README.md` and `app.py` required)

```yaml
title: AI Image Caption Generator
sdk: streamlit
app_file: app.py
python_version: 3.10
```

### GitHub Actions (`.github/workflows/push_to_hf.yml`)

```yaml
name: Deploy to Hugging Face Spaces

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Git identity
        run: |
          git config --global user.email "saadtoorx@example.com"
          git config --global user.name "saadtoorx"

      - name: Push to Hugging Face
        run: |
          git remote remove hf || true
          git remote add hf https://saadtoorx:${{ secrets.HF_TOKEN }}@huggingface.co/spaces/saadtoorx/ai-image-caption-generator
          git push hf HEAD:main --force
```

---

## 📜 License

This project is licensed under the **MIT License**.  
See the [LICENSE](./LICENSE) file for full details.

---

## 🙋‍♂️ Author

**Saad Toor**  
🔗 [GitHub](https://github.com/saadtoorx) • [LinkedIn](https://linkedin.com/in/saadtoorx)

If you found this project helpful, don't forget to ⭐ star the repository and share it!

---
