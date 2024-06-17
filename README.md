# FortKnock - Fortnite Knockdown Detection with YOLOv5

## Overview

FortKnock is a machine learning project that uses the YOLOv5 object detection model to identify if a player has been knocked down in the game Fortnite. This model is designed to run fast inference with high throughput.

## Repository Structure

- `data/`: Submodule containing training data (private repository).
- `notebooks/`: Jupyter notebooks for data exploration, model training, and evaluation.
- `saves/models/`: Train model and weights.
- `tests/`: Test scripts and test data.
- `.gitmodules`: Configuration file for the submodule.
- `Dockerfile`: Docker configuration for setting up the project environment.
- `requirements.txt`: List of dependencies required for the project.

## Getting Started

### Prerequisites

- Python 3.8+
- Git
- Docker (optional, for using Docker)

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

3. **Set up a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install the required dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Prepare the data**:
   - Ensure you have access to the `data/` submodule which contains the training data.
   - Follow the instructions in the `data/README.md` for any additional steps to prepare the data.

### Training the Model

To train the YOLOv5 model, follow the steps in the provided Jupyter notebooks in the `notebooks/` directory. Typically, this involves:

1. Exploring the dataset.
2. Configuring the YOLOv5 training parameters.
3. Running the training script to train the model on the labeled data.
4. Evaluating the model's performance.

### Using Docker

You can also use Docker to set up the project environment:

1. **Build the Docker image**:
    ```sh
    docker build -t fortknock .
    ```

2. **Run a Docker container**:
    ```sh
    docker run -it --rm -v $(pwd):/app fortknock
    ```

## Inference

To run inference using the trained YOLOv5 model, use the provided scripts or notebooks in the `notebooks/` directory. This will allow you to input new gameplay footage and get predictions on whether a player has been knocked down.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [YOLOv5](https://github.com/ultralytics/yolov5) by Ultralytics
- The Fortnite community for gameplay footage

## Contact

For any questions or inquiries, please contact [your name] at [your email].

