# FortKnock - Fortnite Knockdown Detection with YOLOv5

<div align="center">
  <img src="https://github.com/barfieldjr/fortknock/assets/73442540/3bc0e1fd-c8b7-45a0-83d2-bca3fad67ca1" alt="fontbolt (1)" style="width: 70%; border: 2px solid black; border-radius: 15px;" />
</div>

## Overview

FortKnock is a machine learning project that uses the YOLOv5 object detection model to identify if a player has been knocked down in the game Fortnite. This model is designed to run fast inference with high throughput.

## Repository Structure

- `knockdata/`: Submodule containing training data (private repository).
- `notebooks/`: Jupyter notebooks for model training, and evaluation.
- `models/`: Object detection model and weights.
- `tests/`: (WIP) Test scripts and test data.
- `.gitmodules`: Configuration file for the YOLOv5 submodule.
- `requirements.txt`: List of dependencies required for the project.

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

1. **Clone the repository**:

   ```sh
   git clone https://github.com/barfieldjr/fortknock.git
   cd fortknock
   ```

2. **Initialize and update the submodule**:

   ```sh
   git submodule init
   git submodule update
   ```

3. **Set up a virtual environment and install dependencies** (optional but recommended):
   ```sh
   source ./setup.sh
   ```

## Inference

1. **Add video**:
   Place the video to be analyzed at `data/input`
2. **Run inference on video**:
   The start script takes two parameters, the filename of the video to run inference on, and the number of fps (recommended 5fps):

```sh
source ./start.sh your_filename.mp4 5
```

### Training the Model

To train the YOLOv5 model, follow the steps in the provided Jupyter notebook in the `notebooks/` directory. This model has a lot of room for improvement. Currently it works very well with the ability to detect knockdowns due to the static nature of the duration and popup of Fortnite's knockdown popup. Improving the confidence of this model would be helpful.

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
