# Contributing to PyKubeSlurm

We appreciate your interest in contributing to PyKubeSlurm! By contributing, you can help improve and grow this project. Please take a moment to review the following guidelines on how to contribute effectively.

## Code of Conduct

We expect all contributors to follow our [Code of Conduct](./CODE_OF_CONDUCT.md). By participating in this project, you are agreeing to abide by its rules to ensure a welcoming and inclusive environment.

## How to Contribute

To contribute to PyKubeSlurm, follow these steps:

1. Fork the repository to your GitHub account.
2. Clone your fork to your local machine.

    ```bash
    git clone https://github.com/matheushent/PyKubeSlurm.git
    ```
3. Create a new branch to work on your feature or bug fix.

    ```bash
    git checkout -b feature-name
    ```
4. Make your changes and commit them with clear and concise commit messages.

    ```bash
    git add <files>
    git commit -m "Your commit message here"
    ```
5. Push your changes to your fork on GitHub.

    ```bash
    git push origin feature-name
    ```
6. Create a pull request (PR) to the `main` branch of the PyKubeSlurm repository.
    - Provide a clear and detailed description of your changes in the PR.
    - Follow the PR template for guidance.
    - Ensure your code passes all tests.
7. Participate in the discussion and make any requested changes to your PR.
8. Once your PR is approved and merged, it will become part of the project.

## Development Setup

If you're interested in setting up the development environment for PyKubeSlurm, make sure you have the following software installed:

* Python >= 3.10
* Poetry >= 1.5.1
* Make >= 3.81

### Installing Python Dependencies

To install the Python dependencies, run the following command at the root of the repository:

```bash
make install
```

### Run the Quality Assurance Locally

When developing, it is essential to run the quality assurance to avoid slow development and/or bad code. The repository comes with a suite of tools for doing such a thing.

#### Unit Tests

PyKubeSlurm uses [pytest](https://pytest.org) for running unit tests. To run the suite of tests, run the following command:

```bash
make test
```

#### Mypy

PyKubeSlurm uses [Mypy](https://www.mypy-lang.org) for type checking analysis. To run the type analysis, run the following command:

```bash
make mypy
```

#### Code Formatting

As previously mentioned, it is essential to keep a standard in the code base. For it, PyKubeSlurm uses [Black](https://github.com/psf/black) and [isort](https://pycqa.github.io/isort/). To format the code, run the following command:

```bash
make format
```

#### Full QA

You can also run the full quality assurance check in a single command:

```bash
make qa
```

## Reporting Issues

If you encounter a bug, have a question, or want to suggest an improvement, please open an issue on our [Issue Tracker](https://github.com/matheushent/PyKubeSlurm/issues). Be sure to provide detailed information, including your environment and the steps to reproduce the issue.

We look forward to your contributions and appreciate your support in making PyKubeSlurm even better!

Your contributions are valuable, and together, we can make this project thrive.
