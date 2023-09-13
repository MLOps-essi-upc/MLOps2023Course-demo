# MLOps2023Course-demo
This is a demo project for the Advanced Topics in Data Engineering II (TAED-2) and the Machine Learning Systems in Production (MLOps) 2023-24 courses (Universitat Politècnica de Catalunya-BarcelonaTech (UPC), Spain).

This project follows the structure proposed by Lanubile et al. [1].

## Project milestones
<table>
    <thead>
        <tr>
            <th>Milestone</th>
            <th>Practice</th>
            <th>Tools</th>
            <th>Demo</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td rowspan="2"><b>Milestone 1 &mdash; Project Inception</b></td>
            <td>Selection of problem and requirements engineering for ML</td>
            <td>Model and dataset cards (by Hugging Face)</td>
            <td></td>
        </tr>
        <tr>
            <td>Project coordination and communication</td>
            <td>Taiga, Trello, Slack</td>
            <td></td>
        </tr>
        <tr>
            <td rowspan="3"><b>Milestone 2 &mdash; Model building: repoducibility</b></td>
            <td>Project structure</td>
            <td>Cookiecutter data science template</td>
            <td></td>
        </tr>
        <tr>
            <td>Code and data versioning</td>
            <td>Git with GitHub Flow, DVC</td>
            <td><a href="docs/git-demo.md">Git demo</a>, <a href="docs/dvc-demo.md">DVC demo</a></td>
        </tr>
        <tr>
            <td>Experiment tracking</td>
            <td>MLflow</td>
            <td><a href="docs/mlflow-demo.md">MLflow demo</a></td>
        </tr>
        <tr>
            <td rowspan="2"><b>Milestone 3 &mdash; Model building: QA</b></td>
            <td>Energy efficiency awareness</td>
            <td>CodeCarbon</td>
            <td><a href="docs/codecarbon-demo.md">CodeCarbon demo</a></td>
        </tr>
        <tr>
            <td>Quality assurance for ML (static analysis + testing data and model)</td>
            <td>Pynbilint (notebook + repository QA), Pylint or flake8, Pytest and Great Expectations</td>
            <td>
                <a href="docs/pytest-demo.md">Pytest demo</a>,
                <a href="docs/great-expectations-demo.md">Great Expectations demo</a>
            </td>
        </tr>
        <tr>
            <td rowspan="3"><b>Milestone 4 &mdash; Model deployment: API</b></td>
            <td>ML system design</td>
            <td>Cloud platform selected by the students (VMs, Heroku, DigitalOcean, etc.)</td>
            <td><a href="docs/deployment/">Deployment guides</a></td>
        </tr>
        <tr>
            <td>APIs for ML</td>
            <td>FastAPI and Pytest (to test the API endpoints)</td>
            <td><a href="docs/fastapi-demo.md">FastAPI demo</a></td>
        </tr>
    </tbody>
</table>

## References
[1] F. Lanubile, S. Martínez-Fernández, and L. Quaranta, "Teaching MLOps in Higher Education through Project-Based Learning." SEET@ICSE 2023: 95-100. doi: [10.1109/ICSE-SEET58685.2023.00015](https://doi.org/10.1109/ICSE-SEET58685.2023.00015).
[2] F. Lanubile, S. Martínez-Fernández, and L. Quaranta, "Training future ML engineers: a project-based course on MLOps." IEEE Software 2024. doi: [10.1109/MS.2023.3310768](https://doi.org/10.1109/MS.2023.3310768).
