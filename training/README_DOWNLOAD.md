# ASL Dataset Download Guide

## 📥 Quick Download Steps:

### Option 1: Roboflow (Recommended)

1. **Create Account**: Go to https://roboflow.com and sign up (free)

2. **Get Dataset**: Visit https://universe.roboflow.com/brad-dwyer/american-sign-language-letters

3. **Download**: 
   - Click "Download Dataset" 
   - Choose "YOLOv5 PyTorch" format
   - Select latest version
   - Get your API key from https://app.roboflow.com/settings/api

4. **Use Our Script**: 
   ```bash
   cd training
   python download_asl_dataset.py
   ```
   (Make sure to replace API_KEY in the script!)

### Option 2: Manual Download

If automatic download doesn't work:

1. Go to https://universe.roboflow.com/brad-dwyer/american-sign-language-letters
2. Click "Download Dataset"
3. Choose "YOLOv5 PyTorch" 
4. Download the ZIP file
5. Extract to: `training/datasets/asl/`

Expected structure:
```
training/
├── datasets/
│   └── asl/
│       ├── train/
│       │   ├── images/
│       │   └── labels/
│       ├── valid/
│       │   ├── images/
│       │   └── labels/
│       ├── test/
│       │   ├── images/
│       │   └── labels/
│       └── data.yaml
├── models/
├── runs/
└── configs/
```

## 🎯 What You'll Get:

- **26 ASL alphabet classes** (A-Z)
- **1000+ images** per class
- **Pre-annotated** in YOLO format
- **Ready to train** immediately

## 🚀 Next Steps:

After download:
1. Run training script: `python training/train_asl_model.py`
2. Wait 2-4 hours for training
3. Replace your model: `weights/yolov5_v0.pt`
4. Update app config for 26 classes
5. Test with new ASL detection!

## 🔧 Alternative Datasets:

If you want more data:
- **Kaggle ASL**: https://www.kaggle.com/datasets/grassknoted/asl-alphabet (87K images!)
- **GitHub ASL**: https://github.com/harshbg/Sign-Language-Interpreter-using-Deep-Learning
- **Custom Collection**: Use our data collection tool (coming next!)
