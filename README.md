
# Evaluating Performance of Pathological Speech Detection 

Our human auditory gives us the remarkable ability to navigate conversations even when in the middle of chaotic environments with other conversations and ambient noises around. However, translating this natural skill into the realm of computers presents a significant challenge known as the ”dinner party problem” within the speech processing field. While performant speech separation algorithm have been developed, they have been devised for neurotypical speakers, i.e., speakers without any speech impairments. However, this poses a problem as pathological conditions can disrupt the speech production mechanism, complicating the accurate processing by algorithm. This project aims to evaluate the performance of the state-of-the-art the speech separators models SepFormer and RE-SepFormer when handling such pathological signals in order to address these challenges.

## Project Structure
```text
PC-GITA_per_task_16000Hz/
├── text_files/                  # Per-scenario text files with audio combinations and metadata (alpha, beta, SNR, duration)
├── processed_audio/             # Per-scenario text files with SI-SDR before/after Sepformer and ReSepformer
├── processed_audio_example/     # Example data for 3 audio pairs per scenario with signals before/after separation
├── Generate.txt.files.ipynb     # Creates folders, downsamples data, assigns SNR, alpha, beta, duration
├── Code.py                      # Processes files and computes performance metrics
├── Analysis.ipynb               # Analyzes and visualizes results
└── Idiap_Dana_Report.pdf        # Final project report with methods and results
```


## Installation

To use this repository, you'll need Python and PyTorch pre-installed. Ensure other dependencies are installed from `pytorch.yaml`.
```bash
# Clone the repository
git clone https://github.com/danaKalaaji/speech_separation_models_pathological_speech.git
cd speech_separation_models_pathological_speech

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install required packages
pip install -r pytorch.yaml
