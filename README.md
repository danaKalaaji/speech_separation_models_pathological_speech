
# Evaluating Performance of Pathological Speech Detection 

Our human auditory gives us the remarkable ability to navigate conversations even when in the middle of chaotic environments with other conversations and ambient noises around. However, translating this natural skill into the realm of computers presents a significant challenge known as the ”dinner party problem” within the speech processing field. While performant speech separation algorithm have been developed, they have been devised for neurotypical speakers, i.e., speakers without any speech impairments. However, this poses a problem as pathological conditions can disrupt the speech production mechanism, complicating the accurate processing by algorithm. This project aims to evaluate the performance of the state-of-the-art the speech separators models SepFormer and RE-SepFormer when handling such pathological signals in order to address these challenges.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)

## Project Structure
├── Code.py ├── Idiap_Dana_Report.pdf ├── PC-GITA_per_task_16000Hz │ ├── processed_audio │ ├── processed_audio_example │ └── text_files ├── README.md └── pytorch.yaml


### Key Files and Directories
PC-GITA_per_task_16000Hz/
├── text_files/                  # Per-scenario text files with all audio combinations and corresponding alpha, beta, SNR, and duration values
├── processed_audio/             # Per-scenario text files where each line corresponds to the two audio processed along with the SI-SDR of the the mix audio before and after going through Sepformer and through ReSepformer
├── processed_audio_example/     # Example files for 3 audio pairs per scenario, with corresponding audio signals before/after separation
├── Generate.txt.files.ipynb                # The code for creating the directories and text files, downsampling the dataset, and updating the text files with random values of SNR for each audio combination and the corresponding values of alpha, beta and duration
├── Code.py # Code for processing the files and computing the performance
├── Analysis.ipynb # Code for analyzing the results
├── Idiap_Dana_Report.pdf # Project's report with details and results

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




### Relevant folders:
- PC-GITA_per_task_16000Hz: folder containing
  - The subfolder **text_files** containing a subfolder per scenario, each containing all the possible combination of audio along with the values of alpha, beta, SNR, and duration
  - The subfolder processed_audio containing a subfolder per scenario, each containing a text file where each line corresponds to the two audio processed along with the SI-SDR of the the mix audio before and after going through Sepformer and through ReSepformer
  - The subfolder processed_audio_example containing a subfolder per scenario, each containing the processed data text files for three audios pairs per scenarios along with the audio signals before and after separation

### Relevant files:
- Generate.txt.files.ipynb: The code for creating the directories and text files, downsampling the dataset, and updating the text files with random values of SNR for each audio combination and the corresponding values of alpha, beta and duration
- Code.py : The code for processing the files and computing the performance
- Analysis.ipynb : The code for analyzing the results
- Idiap_Dana_Report.pdf: Project's report, containing all the details of the process
