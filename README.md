# Pathological Speech Enhancement with SepFormer Models

This project evaluates the performance of state-of-the-art speech separation models (SepFormer and RE-SepFormer) when processing pathological speech signals from speakers with Parkinson's Disease. The study addresses the "dinner party problem" in speech processing by analyzing how well these models perform on non-neurotypical speech patterns.

## Overview

Our human auditory system gives us the remarkable ability to navigate conversations even in chaotic environments. However, translating this skill into computer algorithms presents significant challenges. While performant speech separation algorithms have been developed for neurotypical speakers, pathological conditions can disrupt speech production mechanisms, complicating accurate processing by these algorithms.

This project specifically evaluates:
- **SepFormer**: A transformer-based speech separation model achieving 22.3 dB SI-SDRi on WSJ0-2mix
- **RE-SepFormer**: A resource-efficient version with reduced computational demands (18.6 dB SI-SDRi)

## Dataset

The project uses the **PC-GITA dataset** containing:
- 100 Spanish native speakers
- 50 Parkinson's Disease (PD) patients (age and gender-matched)
- 50 healthy control subjects
- 10 Spanish sentences per speaker
- Recordings in noise-controlled, soundproof conditions

## Methodology (further information in the report)

### Scenarios Tested
The analysis covers **10 different scenarios** based on health status and gender:

**Healthy Speaker Mixtures:**
- Healthy male + Healthy male (54,000 pairs)
- Healthy female + Healthy female (54,000 pairs)
- Healthy male + Healthy female (56,250 pairs)

**Parkinson's Disease Speaker Mixtures:**
- PD male + PD male (54,000 pairs)
- PD female + PD female (54,000 pairs)
- PD male + PD female (56,250 pairs)

**Mixed Health Condition Scenarios:**
- Healthy male + PD male (56,250 pairs)
- Healthy male + PD female (56,250 pairs)
- Healthy female + PD male (56,250 pairs)
- Healthy female + PD female (56,250 pairs)

**Total: 553,500 audio signal mixtures**

### Signal Processing
- Audio resampled to 8 kHz (required by models)
- Random SNR between 0-5 dB for each mixture
- Mixed signals: `y = αx₁ + βx₂`
- Performance evaluated using Scale-Invariant SDR (SI-SDR) metric

## Key Findings

### Performance Patterns
1. **Gender Influence**: Models perform better on male voices; mixed-gender scenarios show highest performance
2. **Health Factor Impact**: Both models perform better with healthy speakers
3. **Language Effect**: Significant performance drop from English (training) to Spanish (testing):
   - SepFormer: 22.4 dB → 10.66 dB average
   - RE-SepFormer: 18.6 dB → 7.98 dB average

### Statistical Results
- **Kruskal-Wallis test**: Significant differences between scenarios (p ≈ 0)
- **Dunn's test**: Confirms scenario-specific performance variations
- SepFormer consistently outperforms RE-SepFormer across all scenarios
- Notable performance decline with pathological speech, especially female PD speakers

## Project Structure

```text
Master-Semester-Project_Dana/
├── PC-GITA_per_task_16000Hz/
│   ├── text_files/                  # Scenario metadata (combinations, SNR, duration)
│   ├── processed_audio/             # SI-SDR results per scenario
│   ├── processed_audio_example/     # Example separations (3 pairs per scenario)
│   ├── Generate_txt_files.ipynb     # Data preprocessing and setup
│   ├── Code.py                      # Main processing and metric computation
│   ├── Analysis.ipynb               # Results analysis and visualization
│   └── Idiap_Dana_Report.pdf        # Complete project report
└── README.md
```

## Installation & Setup

### Prerequisites
- Python 3.7+
- PyTorch
- SpeechBrain framework

### Installation Steps
```bash
# Clone the repository
git clone https://github.com/danaKalaaji/Master-Semester-Project_Dana.git
cd Master-Semester-Project_Dana

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install speechbrain torch torchaudio
pip install pandas numpy matplotlib seaborn scipy librosa
```

### Download Models
The project uses pre-trained models from SpeechBrain:
```python
# Models will be automatically downloaded when running the code
# SepFormer: speechbrain/sepformer-wsj02mix
# RE-SepFormer: speechbrain/sepformer-wsj02mix-efficient
```

## Usage

### 1. Data Preparation
```bash
# Run the data preprocessing notebook
jupyter notebook Generate_txt_files.ipynb
```

### 2. Model Evaluation
```bash
# Process all scenarios and compute metrics
python Code.py
```

### 3. Results Analysis
```bash
# Analyze results and generate visualizations
jupyter notebook Analysis.ipynb
```

## Results Summary

| Scenario | SepFormer SI-SDR (dB) | RE-SepFormer SI-SDR (dB) |
|----------|----------------------|--------------------------|
| Healthy M + Healthy F | 11.2 | 8.4 |
| Healthy M + Healthy M | 10.8 | 8.1 |
| Healthy F + PD M | 10.6 | 7.9 |
| Healthy M + PD M | 10.4 | 7.8 |
| Healthy M + PD F | 10.2 | 7.6 |
| Healthy F + Healthy F | 10.1 | 7.5 |
| PD M + PD M | 9.8 | 7.3 |
| Healthy F + PD F | 9.6 | 7.2 |
| PD M + PD F | 9.4 | 7.0 |
| PD F + PD F | 9.1 | 6.8 |

## Limitations & Considerations

1. **Cross-language generalization**: Models trained on English show reduced performance on Spanish
2. **Dataset specificity**: Performance drops are documented when WSJ0-2Mix trained models are tested on other datasets
3. **Gender bias**: Consistent lower performance on female voices, particularly with pathological speech
4. **No warranty**: SpeechBrain team provides no performance guarantees on alternative datasets
